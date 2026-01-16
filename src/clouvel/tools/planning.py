# -*- coding: utf-8 -*-
"""Planning tools (v0.6): init_planning, save_finding, refresh_goals, update_progress"""

from pathlib import Path
from datetime import datetime
from mcp.types import TextContent


async def init_planning(path: str, task: str, goals: list) -> list[TextContent]:
    """영속적 컨텍스트 초기화"""
    project_path = Path(path)

    if not project_path.exists():
        return [TextContent(type="text", text=f"❌ 경로가 존재하지 않습니다: {path}")]

    planning_dir = project_path / ".claude" / "planning"
    planning_dir.mkdir(parents=True, exist_ok=True)

    # task_plan.md 생성
    goals_md = "\n".join(f"- [ ] {g}" for g in goals) if goals else "- [ ] (목표 정의 필요)"

    task_plan_content = f"""# Task Plan

> 생성일: {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## 현재 작업

{task}

---

## 목표

{goals_md}

---

## 접근 방식

(작업 시작 전 계획 작성)

---

## 제약 조건

- PRD에 명시된 범위 내에서만 작업
- 테스트 없이 배포 금지

---

> 💡 `refresh_goals` 도구로 현재 목표를 리마인드할 수 있습니다.
"""

    # findings.md 생성
    findings_content = f"""# Findings

> 조사 결과 기록
> 생성일: {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## 2-Action Rule

> view/browser 작업 2개 후 반드시 여기에 기록!

---

(아직 기록 없음)
"""

    # progress.md 생성
    progress_content = f"""# Progress

> 마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## 완료 (Completed)

*(아직 없음)*

---

## 진행중 (In Progress)

*(없음)*

---

## 블로커 (Blockers)

*(없음)*

---

## 다음 할 일 (Next)

*(결정 필요)*

---

> 💡 업데이트: `update_progress` 도구 호출
"""

    # 파일 생성
    (planning_dir / "task_plan.md").write_text(task_plan_content, encoding='utf-8')
    (planning_dir / "findings.md").write_text(findings_content, encoding='utf-8')
    (planning_dir / "progress.md").write_text(progress_content, encoding='utf-8')

    return [TextContent(type="text", text=f"""# 영속적 컨텍스트 초기화 완료

## 생성된 파일

| 파일 | 용도 |
|------|------|
| `task_plan.md` | 작업 계획 + 목표 |
| `findings.md` | 조사 결과 기록 |
| `progress.md` | 진행 상황 추적 |

## 경로
`{planning_dir}`

## 다음 단계

1. 목표 확인: `refresh_goals`
2. 조사 기록: `save_finding`
3. 진행 업데이트: `update_progress`

**긴 세션에서도 목표를 잃지 마세요!**
""")]


async def save_finding(path: str, topic: str, question: str, findings: str, source: str, conclusion: str) -> list[TextContent]:
    """조사 결과 저장"""
    project_path = Path(path)
    findings_file = project_path / ".claude" / "planning" / "findings.md"

    if not findings_file.exists():
        return [TextContent(type="text", text="❌ findings.md가 없습니다. 먼저 `init_planning` 도구로 초기화하세요.")]

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    finding_entry = f"""
---

## [{timestamp}] {topic}

### 질문
{question if question else '(명시되지 않음)'}

### 발견
{findings}

### 소스
{source if source else '(없음)'}

### 결론
{conclusion if conclusion else '(추가 조사 필요)'}

"""

    existing = findings_file.read_text(encoding='utf-8')
    findings_file.write_text(existing + finding_entry, encoding='utf-8')

    return [TextContent(type="text", text=f"""# Finding 저장 완료

## 요약

| 항목 | 내용 |
|------|------|
| 주제 | {topic} |
| 질문 | {question or '없음'} |
| 소스 | {source or '없음'} |

## 저장 위치
`{findings_file}`

---

**2-Action Rule 준수!**
""")]


async def refresh_goals(path: str) -> list[TextContent]:
    """목표 리마인드"""
    project_path = Path(path)
    task_plan_file = project_path / ".claude" / "planning" / "task_plan.md"
    progress_file = project_path / ".claude" / "planning" / "progress.md"

    if not task_plan_file.exists():
        return [TextContent(type="text", text="❌ task_plan.md가 없습니다. 먼저 `init_planning` 도구로 초기화하세요.")]

    task_plan = task_plan_file.read_text(encoding='utf-8')
    progress = progress_file.read_text(encoding='utf-8') if progress_file.exists() else "(없음)"

    # 목표 추출
    goals = []
    in_goals_section = False
    for line in task_plan.split("\n"):
        if "## 목표" in line:
            in_goals_section = True
        elif line.startswith("## "):
            in_goals_section = False
        elif in_goals_section and line.strip().startswith("- "):
            goals.append(line.strip())

    goals_md = "\n".join(goals) if goals else "*(목표 없음)*"

    return [TextContent(type="text", text=f"""# 목표 리마인드

## 현재 작업

(task_plan.md 참조)

## 목표

{goals_md}

---

## 현재 진행 상황

{progress[:500]}{'...' if len(progress) > 500 else ''}

---

## 다음 액션

1. 위 목표 중 하나를 선택
2. 해당 목표에 집중
3. 완료되면 `update_progress`로 기록

**"지금 뭐하고 있었지?" → 위 목표를 확인하세요!**
""")]


async def update_progress(path: str, completed: list, in_progress: str, blockers: list, next_item: str) -> list[TextContent]:
    """진행 상황 업데이트"""
    project_path = Path(path)
    progress_file = project_path / ".claude" / "planning" / "progress.md"

    if not progress_file.exists():
        return [TextContent(type="text", text="❌ progress.md가 없습니다. 먼저 `init_planning` 도구로 초기화하세요.")]

    existing = progress_file.read_text(encoding='utf-8')

    # 기존 완료 항목 파싱
    existing_completed = []
    in_completed_section = False

    for line in existing.split("\n"):
        if "## 완료" in line:
            in_completed_section = True
        elif line.startswith("## "):
            in_completed_section = False
        elif in_completed_section and line.strip().startswith("- "):
            item = line.strip()[2:]
            if item and item != "*(아직 없음)*":
                existing_completed.append(item)

    # 새 완료 항목 추가
    all_completed = existing_completed + list(completed)
    completed_md = "\n".join(f"- {c}" for c in all_completed) if all_completed else "*(아직 없음)*"
    blockers_md = "\n".join(f"- {b}" for b in blockers) if blockers else "*(없음)*"

    # 새 progress.md 생성
    new_progress = f"""# Progress

> 마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## 완료 (Completed)

{completed_md}

---

## 진행중 (In Progress)

{f"- {in_progress}" if in_progress else "*(없음)*"}

---

## 블로커 (Blockers)

{blockers_md}

---

## 다음 할 일 (Next)

{next_item if next_item else "*(결정 필요)*"}

---

> 💡 업데이트: `update_progress` 도구 호출
"""

    progress_file.write_text(new_progress, encoding='utf-8')

    return [TextContent(type="text", text=f"""# Progress 업데이트 완료

## 요약

| 항목 | 개수/내용 |
|------|----------|
| 완료 | {len(all_completed)}개 |
| 진행중 | {in_progress if in_progress else '없음'} |
| 블로커 | {len(blockers)}개 |
| 다음 | {next_item if next_item else '미정'} |

## 저장 위치
`{progress_file}`

---

**진행 상황이 기록되었습니다!**
""")]
