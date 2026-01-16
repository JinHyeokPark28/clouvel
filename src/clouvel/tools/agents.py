# -*- coding: utf-8 -*-
"""Agent tools (v0.7): spawn_explore, spawn_librarian"""

from pathlib import Path
from datetime import datetime
from mcp.types import TextContent


async def spawn_explore(path: str, query: str, scope: str, save_findings: bool) -> list[TextContent]:
    """탐색 전문 에이전트"""
    project_path = Path(path)

    if not project_path.exists():
        return [TextContent(type="text", text=f"❌ 경로가 존재하지 않습니다: {path}")]

    # 스코프별 탐색 전략
    scope_strategies = {
        "file": {
            "description": "단일 파일 분석",
            "actions": ["파일 내용 읽기", "함수/클래스 구조 파악", "의존성 확인"],
            "depth": 1
        },
        "folder": {
            "description": "폴더 내 파일들 분석",
            "actions": ["폴더 구조 스캔", "관련 파일 식별", "패턴 매칭"],
            "depth": 2
        },
        "project": {
            "description": "프로젝트 전체 탐색",
            "actions": ["디렉토리 구조 파악", "엔트리포인트 찾기", "모듈 관계 분석"],
            "depth": 3
        },
        "deep": {
            "description": "심층 분석 (병렬 조사)",
            "actions": ["전체 스캔", "크로스 레퍼런스", "의존성 그래프", "데드코드 탐지"],
            "depth": 5
        }
    }

    strategy = scope_strategies.get(scope, scope_strategies["project"])

    # 탐색 프롬프트 생성
    explore_prompt = f"""# 탐색 에이전트 활성화

## 목표
{query}

## 탐색 전략: {strategy['description']}

### 실행할 액션 (병렬 권장)
{chr(10).join(f"- [ ] {action}" for action in strategy['actions'])}

### 2-Action Rule 적용
> view/browser 작업 2개 후 반드시 결과 저장

탐색 중 발견한 내용은 즉시 기록하세요:
- 파일 위치: `파일경로:라인번호`
- 핵심 발견: 한 줄 요약
- 다음 액션: 추가 탐색 필요 여부

### 탐색 범위
- 경로: `{path}`
- 깊이: {strategy['depth']} 레벨
- 스코프: {scope}

---

## 체크리스트

1. [ ] 관련 파일 식별
2. [ ] 핵심 코드 위치 파악
3. [ ] 의존성/호출 관계 확인
4. [ ] 결과 정리

---

**탐색 시작!** 위 액션들을 병렬로 실행하세요.
"""

    # findings.md에 저장 (옵션)
    if save_findings:
        planning_dir = project_path / ".claude" / "planning"
        findings_file = planning_dir / "findings.md"

        if findings_file.exists():
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
            finding_entry = f"""
---

## [{timestamp}] 탐색: {query}

- **스코프**: {scope}
- **상태**: 진행중
- **결과**: *(탐색 후 업데이트)*

"""
            existing = findings_file.read_text(encoding='utf-8')
            findings_file.write_text(existing + finding_entry, encoding='utf-8')

    return [TextContent(type="text", text=explore_prompt)]


async def spawn_librarian(path: str, topic: str, research_type: str, depth: str) -> list[TextContent]:
    """라이브러리언 에이전트"""
    project_path = Path(path)

    if not project_path.exists():
        return [TextContent(type="text", text=f"❌ 경로가 존재하지 않습니다: {path}")]

    # 조사 타입별 전략
    type_strategies = {
        "library": {
            "focus": "라이브러리 사용법",
            "sources": ["공식 문서", "GitHub README", "npm/PyPI 페이지"],
            "questions": [
                "설치 방법은?",
                "기본 사용법은?",
                "주요 API는?",
                "버전별 차이는?"
            ]
        },
        "api": {
            "focus": "API 스펙 조사",
            "sources": ["API 문서", "Swagger/OpenAPI", "예제 코드"],
            "questions": [
                "엔드포인트 목록은?",
                "인증 방식은?",
                "요청/응답 형식은?",
                "에러 코드는?"
            ]
        },
        "migration": {
            "focus": "마이그레이션 가이드",
            "sources": ["마이그레이션 문서", "CHANGELOG", "Breaking Changes"],
            "questions": [
                "주요 변경사항은?",
                "호환성 이슈는?",
                "마이그레이션 단계는?",
                "롤백 방법은?"
            ]
        },
        "best_practice": {
            "focus": "베스트 프랙티스",
            "sources": ["공식 가이드", "커뮤니티 블로그", "Stack Overflow"],
            "questions": [
                "권장 패턴은?",
                "안티패턴은?",
                "성능 최적화는?",
                "보안 고려사항은?"
            ]
        }
    }

    # 깊이별 조사 수준
    depth_levels = {
        "quick": {"time": "5분", "detail": "핵심만", "sources_count": 1},
        "standard": {"time": "15분", "detail": "기본 + 예제", "sources_count": 2},
        "thorough": {"time": "30분+", "detail": "심층 분석", "sources_count": 3}
    }

    strategy = type_strategies.get(research_type, type_strategies["library"])
    level = depth_levels.get(depth, depth_levels["standard"])

    # 라이브러리언 프롬프트 생성
    librarian_prompt = f"""# 라이브러리언 에이전트 활성화

## 조사 주제
**{topic}**

## 조사 전략: {strategy['focus']}

### 참고할 소스 (우선순위 순)
{chr(10).join(f"{i+1}. {src}" for i, src in enumerate(strategy['sources'][:level['sources_count']]))}

### 답해야 할 질문
{chr(10).join(f"- [ ] {q}" for q in strategy['questions'])}

---

## 조사 깊이: {depth.upper()}

| 항목 | 값 |
|------|-----|
| 예상 시간 | {level['time']} |
| 상세도 | {level['detail']} |
| 소스 수 | {level['sources_count']}개 |

---

## 2-Action Rule

> 외부 문서 2개 확인 후 반드시 findings.md에 기록

### 기록 형식
```markdown
## [주제]

### 질문
(찾고 있던 것)

### 발견
(핵심 내용)

### 소스
(링크/문서명)

### 결론
(다음 액션)
```

---

## 체크리스트

1. [ ] 공식 문서 확인
2. [ ] 예제 코드 수집
3. [ ] 버전 호환성 확인
4. [ ] 결과 정리 및 저장

---

**조사 시작!** `save_finding` 도구로 결과를 저장하세요.
"""

    # findings.md에 조사 시작 기록
    planning_dir = project_path / ".claude" / "planning"
    findings_file = planning_dir / "findings.md"

    if findings_file.exists():
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        finding_entry = f"""
---

## [{timestamp}] 조사: {topic}

- **타입**: {research_type}
- **깊이**: {depth}
- **상태**: 진행중
- **결과**: *(조사 후 업데이트)*

"""
        existing = findings_file.read_text(encoding='utf-8')
        findings_file.write_text(existing + finding_entry, encoding='utf-8')

    return [TextContent(type="text", text=librarian_prompt)]
