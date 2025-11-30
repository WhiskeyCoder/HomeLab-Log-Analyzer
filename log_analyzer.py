from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
import docker
import json
import requests
from typing import List, Dict, Optional
import re

app = FastAPI()

# Add container names here
MONITORED_CONTAINERS = [
    # "container_name_1",
    # "container_name_2",
]

class LogAnalysisRequest(BaseModel):
    containers: Optional[List[str]] = None
    hours: int = 24
    lm_studio_url: str = "http://localhost:1234/v1/completions"
    model: str = "qwen2.5-1.5b-instruct"


class LogAnalysisResponse(BaseModel):
    timestamp: str
    summary: Dict
    raw_insights: str
    containers_analyzed: int
    issues_found: int


class LogAnalyzer:
    def __init__(self):
        self.client = docker.from_env()

    def filter_noise(self, log_line: str) -> bool:
        noise_patterns = [
            r'^\s*$',
            r'GET /health.*200',
            r'HEAD /.*200',
            r'.*heartbeat.*',
            r'.*ping.*pong.*',
        ]
        return not any(re.search(pattern, log_line, re.IGNORECASE)
                       for pattern in noise_patterns)

    def is_monitored(self, container_name: str) -> bool:
        if not MONITORED_CONTAINERS:
            return True
        return container_name in MONITORED_CONTAINERS

    def get_container_logs(self, container_name: str, since_hours: int) -> str:
        try:
            container = self.client.containers.get(container_name)
            since_time = datetime.now() - timedelta(hours=since_hours)
            logs = container.logs(
                since=since_time,
                timestamps=True
            ).decode('utf-8', errors='ignore')
            filtered_logs = '\n'.join([
                line for line in logs.split('\n')
                if self.filter_noise(line)
            ])

            return filtered_logs

        except docker.errors.NotFound:
            return f"Container {container_name} not found"
        except Exception as e:
            return f"Error reading logs from {container_name}: {str(e)}"

    def get_all_containers_logs(self, since_hours: int) -> Dict[str, str]:
        containers = self.client.containers.list()
        logs_dict = {}

        for container in containers:
            name = container.name
            if not self.is_monitored(name):
                continue
            
            logs = self.get_container_logs(name, since_hours)
            if logs and len(logs.strip()) > 0:
                logs_dict[name] = logs

        return logs_dict

    def analyze_with_llm(self, logs_dict: Dict[str, str], lm_studio_url: str, model: str) -> Dict:
        prompt = self._build_analysis_prompt(logs_dict)
        payload = {
            "model": model,
            "prompt": prompt,
            "temperature": 0.3,
            "max_tokens": 2000,
            "stop": ["###"]
        }

        try:
            response = requests.post(lm_studio_url, json=payload, timeout=120)
            response.raise_for_status()

            result = response.json()
            analysis_text = result['choices'][0]['text'].strip()

            try:
                return json.loads(analysis_text)
            except json.JSONDecodeError:
                return {
                    "status": "partial_parse_failure",
                    "raw_output": analysis_text,
                    "containers_analyzed": len(logs_dict)
                }

        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"LLM API Error: {str(e)}")

    def _build_analysis_prompt(self, logs_dict: Dict[str, str]) -> str:
        logs_summary = ""
        for container_name, logs in logs_dict.items():
            truncated_logs = logs[:5000] if len(logs) > 5000 else logs
            logs_summary += f"\n### Container: {container_name}\n{truncated_logs}\n"

        prompt = f"""You are a Docker log analyzer. Analyze the following container logs and provide a structured summary.

Focus on:
1. Critical errors or failures
2. Warnings that need attention
3. Successful operations worth noting
4. Resource issues (memory, disk, network)
5. Security-relevant events
6. Performance anomalies

Return your analysis as valid JSON with this structure:
{{
    "critical_issues": ["list of critical problems"],
    "warnings": ["list of warnings"],
    "successes": ["list of successful operations"],
    "recommendations": ["list of actionable recommendations"],
    "container_status": {{"container_name": "status_summary"}},
    "overall_health": "healthy|degraded|critical"
}}

Container Logs:
{logs_summary}

JSON Response:"""

        return prompt


analyzer = LogAnalyzer()


@app.post("/analyze", response_model=LogAnalysisResponse)
async def analyze_logs(request: LogAnalysisRequest):
    if request.containers:
        logs_dict = {}
        for name in request.containers:
            if analyzer.is_monitored(name):
                logs_dict[name] = analyzer.get_container_logs(name, request.hours)
    else:
        logs_dict = analyzer.get_all_containers_logs(request.hours)

    if not logs_dict:
        raise HTTPException(status_code=404, detail="No logs found")

    analysis = analyzer.analyze_with_llm(
        logs_dict,
        request.lm_studio_url,
        request.model
    )

    issues_count = (
            len(analysis.get('critical_issues', [])) +
            len(analysis.get('warnings', []))
    )

    return LogAnalysisResponse(
        timestamp=datetime.now().isoformat(),
        summary=analysis,
        raw_insights=json.dumps(analysis, indent=2),
        containers_analyzed=len(logs_dict),
        issues_found=issues_count
    )


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "log-analyzer"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8765)
