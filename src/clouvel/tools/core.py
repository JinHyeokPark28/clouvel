# -*- coding: utf-8 -*-
"""Core tools: can_code, scan_docs, analyze_docs, init_docs"""

import re
from pathlib import Path
from datetime import datetime
from mcp.types import TextContent

# 필수 문서 정의
REQUIRED_DOCS = [
    {"type": "prd", "name": "PRD", "patterns": [r"prd", r"product.?requirement"], "priority": "critical"},
    {"type": "architecture", "name": "아키텍처", "patterns": [r"architect", r"module"], "priority": "critical"},
    {"type": "api_spec", "name": "API 스펙", "patterns": [r"api", r"swagger", r"openapi"], "priority": "critical"},
    {"type": "db_schema", "name": "DB 스키마", "patterns": [r"schema", r"database", r"db"], "priority": "critical"},
    {"type": "verification", "name": "검증 계획", "patterns": [r"verif", r"test.?plan"], "priority": "critical"},
]


async def can_code(path: str) -> list[TextContent]:
    """코딩 가능 여부 확인 - 핵심 기능"""
    docs_path = Path(path)

    if not docs_path.exists():
        return [TextContent(type="text", text=f"""
# ⛔ 코딩 금지

## 이유
docs 폴더가 없습니다: `{path}`

## 지금 해야 할 것
1. `docs` 폴더를 생성하세요
2. PRD(제품 요구사항 문서)를 먼저 작성하세요
3. `get_prd_template` 도구로 템플릿을 생성할 수 있습니다

## 왜?
PRD 없이 코딩하면:
- 요구사항 불명확 → 재작업
- 예외 케이스 누락 → 버그
- 팀원 간 인식 차이 → 충돌

**문서 먼저, 코딩은 나중에.**

사용자에게 PRD 작성을 도와주겠다고 말하세요.
""")]

    files = [f.name.lower() for f in docs_path.iterdir() if f.is_file()]
    detected = []
    missing = []

    for req in REQUIRED_DOCS:
        found = False
        for filename in files:
            for pattern in req["patterns"]:
                if re.search(pattern, filename, re.IGNORECASE):
                    detected.append(req["name"])
                    found = True
                    break
            if found:
                break
        if not found:
            missing.append(req["name"])

    if missing:
        missing_list = "\n".join(f"- {m}" for m in missing)
        detected_list = "\n".join(f"- {d}" for d in detected) if detected else "없음"

        return [TextContent(type="text", text=f"""
# ⛔ 코딩 금지

## 현재 상태
✅ 있음:
{detected_list}

❌ 없음 (필수):
{missing_list}

## 지금 해야 할 것
코드를 작성하지 마세요. 대신:

1. 누락된 문서를 먼저 작성하세요
2. 특히 **PRD**가 가장 중요합니다
3. `get_prd_guide` 도구로 작성법을 확인하세요
4. `get_prd_template` 도구로 템플릿을 생성하세요

## 사용자에게 전달할 메시지
"코드를 작성하기 전에 먼저 문서를 준비해야 합니다.
{len(missing)}개의 필수 문서가 없습니다: {', '.join(missing)}
제가 PRD 작성을 도와드릴까요?"

**절대 코드를 작성하지 마세요. 문서 작성을 도와주세요.**
""")]

    return [TextContent(type="text", text=f"""
# ✅ 코딩 가능

## 문서 상태
모든 필수 문서가 준비되어 있습니다:
{chr(10).join(f'- {d}' for d in detected)}

## 코딩 시작 전 확인사항
1. PRD에 명시된 요구사항을 따르세요
2. API 스펙에 맞게 구현하세요
3. DB 스키마를 참고하세요
4. 검증 계획에 따라 테스트하세요

이제 사용자의 요청에 따라 코드를 작성해도 됩니다.
""")]


async def scan_docs(path: str) -> list[TextContent]:
    """docs 폴더 스캔"""
    docs_path = Path(path)

    if not docs_path.exists():
        return [TextContent(type="text", text=f"경로 없음: {path}")]

    if not docs_path.is_dir():
        return [TextContent(type="text", text=f"디렉토리 아님: {path}")]

    files = []
    for f in sorted(docs_path.iterdir()):
        if f.is_file():
            stat = f.stat()
            files.append(f"{f.name} ({stat.st_size:,} bytes)")

    result = f"📁 {path}\n총 {len(files)}개 파일\n\n"
    result += "\n".join(files)

    return [TextContent(type="text", text=result)]


async def analyze_docs(path: str) -> list[TextContent]:
    """docs 폴더 분석"""
    docs_path = Path(path)

    if not docs_path.exists():
        return [TextContent(type="text", text=f"경로 없음: {path}")]

    files = [f.name.lower() for f in docs_path.iterdir() if f.is_file()]
    detected = []
    missing = []

    for req in REQUIRED_DOCS:
        found = False
        for filename in files:
            for pattern in req["patterns"]:
                if re.search(pattern, filename, re.IGNORECASE):
                    detected.append(req["name"])
                    found = True
                    break
            if found:
                break
        if not found:
            missing.append(req["name"])

    critical_total = len([r for r in REQUIRED_DOCS if r["priority"] == "critical"])
    critical_found = len([r for r in REQUIRED_DOCS if r["priority"] == "critical" and r["name"] in detected])
    coverage = critical_found / critical_total if critical_total > 0 else 1.0

    result = f"## 분석 결과: {path}\n\n"
    result += f"커버리지: {coverage:.0%}\n\n"

    if detected:
        result += "### 있음\n" + "\n".join(f"- {d}" for d in detected) + "\n\n"

    if missing:
        result += "### 없음 (작성 필요)\n" + "\n".join(f"- {m}" for m in missing) + "\n\n"

    if not missing:
        result += "✅ 필수 문서 다 있음. 바이브코딩 시작해도 됨.\n"
    else:
        result += f"⛔ {len(missing)}개 문서 먼저 작성하고 코딩 시작할 것.\n"

    return [TextContent(type="text", text=result)]


async def init_docs(path: str, project_name: str) -> list[TextContent]:
    """docs 폴더 초기화 + 템플릿 생성"""
    project_path = Path(path)
    docs_path = project_path / "docs"

    docs_path.mkdir(parents=True, exist_ok=True)

    templates = {
        "PRD.md": f"# {project_name} PRD\n\n> 작성일: {datetime.now().strftime('%Y-%m-%d')}\n\n## 한 줄 요약\n\n[작성 필요]\n",
        "ARCHITECTURE.md": f"# {project_name} 아키텍처\n\n## 시스템 구조\n\n[작성 필요]\n",
        "API.md": f"# {project_name} API 스펙\n\n## 엔드포인트\n\n[작성 필요]\n",
        "DATABASE.md": f"# {project_name} DB 스키마\n\n## 테이블\n\n[작성 필요]\n",
        "VERIFICATION.md": f"# {project_name} 검증 계획\n\n## 테스트 케이스\n\n[작성 필요]\n",
    }

    created = []
    for filename, content in templates.items():
        file_path = docs_path / filename
        if not file_path.exists():
            file_path.write_text(content, encoding='utf-8')
            created.append(filename)

    result = f"## docs 폴더 초기화 완료\n\n경로: `{docs_path}`\n\n"
    if created:
        result += "### 생성된 파일\n" + "\n".join(f"- {f}" for f in created) + "\n\n"
    else:
        result += "모든 파일이 이미 존재합니다.\n\n"

    result += "### 다음 단계\n1. PRD.md부터 작성하세요\n2. `get_prd_guide` 도구로 작성법을 확인하세요\n"

    return [TextContent(type="text", text=result)]
