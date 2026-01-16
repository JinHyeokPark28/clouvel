# -*- coding: utf-8 -*-
"""
Clouvel Pro Tools (v1.1.0)
Shovel 자동 설치 + 라이선스 검증

유료 기능:
- install_shovel: Shovel .claude/ 구조 자동 설치
- sync_commands: Clouvel MCP와 Shovel 커맨드 통합
- verify_license: 라이선스 검증
"""

import os
import json
from pathlib import Path
from datetime import datetime
from mcp.types import TextContent


# ============================================================
# Shovel Structure Templates
# ============================================================

SHOVEL_SETTINGS = {
    "$schema": "https://json.schemastore.org/claude-code-settings.json",
    "permissions": {
        "allow": [
            "Bash(pnpm:*)", "Bash(npm:*)", "Bash(npx:*)", "Bash(node:*)",
            "Bash(tsc:*)", "Bash(vitest:*)", "Bash(jest:*)", "Bash(eslint:*)",
            "Bash(prettier:*)", "Bash(bash scripts/*)", "Bash(mkdir:*)",
            "Bash(cat:*)", "Bash(ls:*)", "Bash(head:*)", "Bash(tail:*)",
            "Bash(grep:*)", "Bash(find:*)", "Bash(wc:*)", "Bash(echo:*)",
            "Bash(pwd)", "Bash(cd:*)", "Bash(test:*)", "Bash(date:*)",
            "Bash(git diff:*)", "Bash(git status:*)", "Bash(git log:*)",
            "Bash(git add:*)", "Bash(git commit:*)", "Bash(git branch:*)",
            "Bash(git checkout:*)", "Bash(git rev-parse:*)",
            "Read", "Write", "Edit", "MultiEdit", "Grep", "LS"
        ],
        "deny": [
            "Bash(rm -rf /)", "Bash(rm -rf ~)", "Bash(rm -rf .)",
            "Bash(sudo:*)", "Bash(chmod 777:*)",
            "Bash(curl * | bash)", "Bash(wget * | bash)",
            "Read(.env)", "Read(.env.*)", "Read(**/secrets/**)",
            "Read(**/*.pem)", "Read(**/*.key)"
        ]
    },
    "hooks": {
        "PreToolUse": [
            {
                "matcher": "Write",
                "hooks": [{
                    "type": "command",
                    "command": "mkdir -p \"$CLAUDE_PROJECT_DIR/.claude/logs\" && echo \"[$(date '+%Y-%m-%d %H:%M:%S')] PreWrite: $CLAUDE_FILE_PATH\" >> \"$CLAUDE_PROJECT_DIR/.claude/logs/tool.log\" 2>/dev/null || true"
                }]
            }
        ],
        "PostToolUse": [
            {
                "matcher": "Write|Edit",
                "hooks": [
                    {"type": "command", "command": "pnpm format --if-present 2>/dev/null || npx prettier --write \"$CLAUDE_FILE_PATHS\" 2>/dev/null || true"},
                    {"type": "command", "command": "echo \"[$(date '+%Y-%m-%d %H:%M:%S')] PostWrite: formatted\" >> \"$CLAUDE_PROJECT_DIR/.claude/logs/tool.log\" 2>/dev/null || true"}
                ]
            }
        ],
        "SessionStart": [
            {"hooks": [{"type": "command", "command": "mkdir -p \"$CLAUDE_PROJECT_DIR/.claude/logs\" && echo \"\\n══════════════════════════════════════\" >> \"$CLAUDE_PROJECT_DIR/.claude/logs/sessions.log\" && echo \"Session Start: $(date '+%Y-%m-%d %H:%M:%S')\" >> \"$CLAUDE_PROJECT_DIR/.claude/logs/sessions.log\" 2>/dev/null || true"}]}
        ],
        "Stop": [
            {"hooks": [
                {"type": "command", "command": "echo \"[$(date '+%Y-%m-%d %H:%M:%S')] Session End\" >> \"$CLAUDE_PROJECT_DIR/.claude/logs/sessions.log\" 2>/dev/null || true"},
                {"type": "command", "command": "echo \"\\n⚠️  Remember: Run 'pnpm gate' before committing!\" 2>/dev/null || true"}
            ]}
        ]
    }
}


# 핵심 커맨드 (가장 많이 사용하는 것들)
SHOVEL_COMMANDS = {
    "gate.md": '''# /gate - Gate 검증

> **유일한 완료 정의**: lint → test → build 전부 PASS

## 실행

```bash
pnpm gate
# 또는
bash scripts/gate.sh
```

## Gate 단계

| 순서 | 단계 | 명령 | 실패 시 |
|------|------|------|---------|
| 1 | Lint | `pnpm lint` | 즉시 중단 |
| 2 | Test | `pnpm test` | 즉시 중단 |
| 3 | Build | `pnpm build` | 즉시 중단 |

## 결과

### PASS
```
✅ Gate PASS
EVIDENCE.md 생성됨
```

### FAIL
```
❌ Gate FAIL at [단계]
수정 후 다시 실행
```

## 규칙

- Gate PASS 없이 "완료" 선언 금지
- 모든 단계 통과해야 커밋 가능
- EVIDENCE.md가 증거
''',

    "verify.md": '''# /verify - Context Bias 제거 검증

> **Boris 방식**: /clear 후 검증해야 진짜 검증

## 사용

```
/verify [scope]
```

## Scope

| 값 | 설명 |
|-----|------|
| `file` | 현재 파일만 |
| `feature` | 현재 기능 전체 |
| `full` | 프로젝트 전체 |

## 검증 순서

```
1. /handoff (의도 기록)
2. /clear (컨텍스트 초기화)
3. /verify (새로운 눈으로 검증)
```

## 왜?

같은 세션에서 자기가 짠 코드 = 문제 못 봄
새 세션에서 검증 = 진짜 검증
''',

    "plan.md": '''# /plan - 태스크 계획

> PRD 기반 계획 수립

## 사용

```
/plan [태스크 설명]
```

## 플로우

```
1. PRD.md 확인
2. 태스크 분해 (Step 단위)
3. 실행 순서 정의
4. 예상 산출물 명시
```

## 출력

```markdown
## Plan: [태스크명]

### Steps
1. [ ] Step 1 - 설명
2. [ ] Step 2 - 설명

### 산출물
- 파일1.ts
- 파일2.ts

### 의존성
- 없음 / 있음 (상세)
```

## 규칙

- PRD에 없는 기능 = 계획 불가
- 스펙 밖 요청 = BACKLOG로 이동
''',

    "implement.md": '''# /implement - 계획 실행

> 승인된 계획 기반 구현

## 사용

```
/implement
```

## 전제조건

- `/plan` 실행 완료
- 사용자 승인 받음

## 실행 순서

```
1. Plan의 Step 1부터 순차 실행
2. 각 Step 완료 시 체크 (✅)
3. 모든 Step 완료 후 → /check-complete
```

## 완료 기준

```
✅ 모든 Step 완료
✅ 코드 lint 통과
✅ 타입 체크 통과
✅ 연결 확인됨
```

## 다음 액션

```
/implement 완료 → /check-complete → /gate → /handoff
```
''',

    "handoff.md": '''# /handoff - 의도 기록

> Step 완료 시 의도와 결정사항 기록

## 사용

```
/handoff
```

## 기록 내용

```markdown
## Handoff: [기능명]
- **완료**: 무엇을 했는지
- **왜**: 왜 이렇게 했는지
- **주의**: 주의할 점
- **다음**: 다음에 할 것
```

## 왜?

- Context 유실 방지
- 다른 세션에서 이어받기 가능
- 검증자가 의도 파악 가능

## 다음 액션

```
/handoff → /clear → /verify
```
''',

    "start.md": '''# /start - 프로젝트 온보딩

> 프로젝트 처음 시작 시 1회 실행

## 사용

```
/start
```

## 동작

```
1. 프로젝트 구조 분석
2. 기술 스택 감지 (Next.js, Express, etc.)
3. 적절한 템플릿 선택
4. CLAUDE.md 생성/업데이트
5. docs/ 폴더 확인
```

## 출력

```
✅ 프로젝트 타입: [Web/API/Desktop/Fullstack]
✅ 기술 스택: [감지된 스택]
✅ CLAUDE.md 생성됨
⚠️  docs/PRD.md 없음 → 작성 필요
```

## 다음 액션

```
/start 완료 → docs/PRD.md 작성 → /plan
```
''',

    "check-complete.md": '''# /check-complete - 껍데기/미연결 검사

> "완료" 전 필수 실행

## 사용

```
/check-complete
```

## 검사 항목

### 1. 껍데기 검사
- [ ] TODO, placeholder 없음
- [ ] console.log만 있는 함수 없음
- [ ] 하드코딩 더미 데이터 없음

### 2. 연결 검사
- [ ] import/export 체인 완성
- [ ] 라우팅 연결됨
- [ ] UI에서 호출됨

### 3. 동작 검사
- [ ] 앱 실행 시 기능 접근 가능
- [ ] 버튼/링크 동작
- [ ] E2E 플로우 완성

## 결과

```
✅ PASS - 진짜 완료
❌ FAIL - [문제점] 수정 필요
```
'''
}


# 템플릿
SHOVEL_TEMPLATES = {
    "PRD.template.md": '''# PRD: [프로젝트명]

> 작성일: YYYY-MM-DD
> 버전: 1.0

## 1. 요약

**한 줄 설명**: [이 프로젝트가 뭔지]
**대상 사용자**: [누가 쓰는지]
**핵심 가치**: [왜 써야 하는지]

## 2. 문제

- 현재 상황: [무엇이 문제인지]
- 고객 피드백: [실제 고객이 뭐라 했는지]

## 3. 솔루션

### 핵심 기능

| 기능 | 설명 | 우선순위 |
|------|------|----------|
| 기능1 | ... | P0 |
| 기능2 | ... | P1 |

### MVP 범위

- [ ] 필수 기능 1
- [ ] 필수 기능 2

### 스펙 밖 (BACKLOG)

- 추후 기능 1
- 추후 기능 2

## 4. 기술 스펙

### 입력
```
- 필드1: 타입, 제약조건
- 필드2: 타입, 제약조건
```

### 출력
```
- 필드1: 타입
- 필드2: 타입
```

### API
```
POST /api/endpoint
- Request: {...}
- Response: {...}
```

## 5. 성공 지표

- [ ] 지표1: 목표값
- [ ] 지표2: 목표값

## 6. 일정

| 마일스톤 | 예상 완료 |
|----------|-----------|
| MVP | YYYY-MM-DD |
| v1.0 | YYYY-MM-DD |
''',

    "findings.template.md": '''# Findings

> 조사 결과 기록 (2-Action Rule)

## 사용법

view/browser 작업 2개 후 → 여기에 기록

---

## [YYYY-MM-DD] 주제

**질문**: 무엇을 알고 싶었는지
**출처**: 어디서 찾았는지
**결과**: 무엇을 알았는지
**결론**: 어떻게 적용할지

---
'''
}


# Gate 스크립트
GATE_SCRIPT = '''#!/bin/bash
# Shovel Gate Script
# lint → test → build

set -e

echo "🚀 Gate 시작..."

# 1. Lint
echo "📝 Step 1: Lint"
if pnpm lint 2>/dev/null || npm run lint 2>/dev/null; then
    echo "✅ Lint PASS"
else
    echo "❌ Lint FAIL"
    exit 1
fi

# 2. Test
echo "🧪 Step 2: Test"
if pnpm test 2>/dev/null || npm run test 2>/dev/null; then
    echo "✅ Test PASS"
else
    echo "❌ Test FAIL"
    exit 1
fi

# 3. Build
echo "🏗️ Step 3: Build"
if pnpm build 2>/dev/null || npm run build 2>/dev/null; then
    echo "✅ Build PASS"
else
    echo "❌ Build FAIL"
    exit 1
fi

# Evidence 생성
echo ""
echo "✅ Gate PASS"
echo ""

EVIDENCE_FILE=".claude/evidence/$(date +%Y%m%d_%H%M%S).md"
mkdir -p .claude/evidence

cat > "$EVIDENCE_FILE" << EOF
# Gate Evidence Report

> Status: PASS
> Timestamp: $(date -Iseconds)
> Commit: $(git rev-parse --short HEAD 2>/dev/null || echo "no-git")

| Step | Result |
|------|--------|
| Lint | ✅ PASS |
| Test | ✅ PASS |
| Build | ✅ PASS |
EOF

echo "📄 Evidence: $EVIDENCE_FILE"
'''


# ============================================================
# License System
# ============================================================

LICENSE_FILE = ".clouvel-license"


def verify_license(license_key: str = None) -> dict:
    """라이선스 검증"""
    # 로컬 라이선스 파일 확인
    home = Path.home()
    license_path = home / LICENSE_FILE

    if license_key:
        # 새 라이선스 저장
        license_path.write_text(license_key)
    elif license_path.exists():
        license_key = license_path.read_text().strip()

    if not license_key:
        return {
            "valid": False,
            "tier": None,
            "message": "라이선스 키가 없습니다. clouvel.lemonsqueezy.com에서 구매하세요."
        }

    # 라이선스 키 형식: CLOUVEL-{TIER}-{RANDOM}
    # 예: CLOUVEL-PERSONAL-ABC123, CLOUVEL-TEAM-XYZ789
    if not license_key.startswith("CLOUVEL-"):
        return {"valid": False, "tier": None, "message": "잘못된 라이선스 키 형식"}

    parts = license_key.split("-")
    if len(parts) < 3:
        return {"valid": False, "tier": None, "message": "잘못된 라이선스 키 형식"}

    tier = parts[1].lower()
    if tier not in ["personal", "team", "enterprise"]:
        return {"valid": False, "tier": None, "message": "알 수 없는 티어"}

    return {
        "valid": True,
        "tier": tier,
        "message": f"✅ {tier.upper()} 라이선스 활성화됨"
    }


# ============================================================
# Pro Tool Implementations
# ============================================================

async def install_shovel(
    path: str,
    project_type: str = "web",
    license_key: str = None
) -> list[TextContent]:
    """
    Shovel .claude/ 구조 자동 설치

    Args:
        path: 프로젝트 루트 경로
        project_type: web, api, desktop, fullstack
        license_key: 라이선스 키 (선택)
    """
    # 라이선스 검증
    license_result = verify_license(license_key)
    if not license_result["valid"]:
        return [TextContent(type="text", text=f"""
❌ Clouvel Pro 라이선스 필요

{license_result['message']}

---

## 구매 링크
https://clouvel.lemonsqueezy.com

## 가격
- Personal: $29 (1명)
- Team: $79 (10명)
- Enterprise: $199 (무제한)
""")]

    project_path = Path(path)
    claude_dir = project_path / ".claude"

    created_files = []

    # 1. 디렉토리 구조 생성
    dirs = ["commands", "templates", "evidence", "logs", "plans"]
    for d in dirs:
        dir_path = claude_dir / d
        dir_path.mkdir(parents=True, exist_ok=True)
        created_files.append(f".claude/{d}/")

    # 2. settings.json 생성
    settings_path = claude_dir / "settings.json"
    with open(settings_path, "w", encoding="utf-8") as f:
        json.dump(SHOVEL_SETTINGS, f, indent=2, ensure_ascii=False)
    created_files.append(".claude/settings.json")

    # 3. 핵심 커맨드 생성
    for filename, content in SHOVEL_COMMANDS.items():
        cmd_path = claude_dir / "commands" / filename
        cmd_path.write_text(content, encoding="utf-8")
        created_files.append(f".claude/commands/{filename}")

    # 4. 템플릿 생성
    for filename, content in SHOVEL_TEMPLATES.items():
        tpl_path = claude_dir / "templates" / filename
        tpl_path.write_text(content, encoding="utf-8")
        created_files.append(f".claude/templates/{filename}")

    # 5. 프로젝트 타입별 CLAUDE.md 템플릿 추가
    project_templates = {
        "web": "web.claude.md",
        "api": "api.claude.md",
        "desktop": "desktop.claude.md",
        "fullstack": "fullstack.claude.md"
    }

    # 6. scripts/gate.sh 생성
    scripts_dir = project_path / "scripts"
    scripts_dir.mkdir(exist_ok=True)
    gate_path = scripts_dir / "gate.sh"
    gate_path.write_text(GATE_SCRIPT, encoding="utf-8")
    created_files.append("scripts/gate.sh")

    # 7. ERROR_LOG.md 생성
    error_log = project_path / "ERROR_LOG.md"
    if not error_log.exists():
        error_log.write_text("""# ERROR_LOG

> 에러 발생 시 자동 기록

---

""", encoding="utf-8")
        created_files.append("ERROR_LOG.md")

    return [TextContent(type="text", text=f"""
✅ Shovel 설치 완료!

## 라이선스
{license_result['message']}

## 생성된 파일
{chr(10).join(f"- {f}" for f in created_files)}

## 다음 단계

```bash
# 1. Gate 스크립트 실행 권한
chmod +x scripts/gate.sh

# 2. Claude Code에서 시작
/start
```

## 핵심 워크플로우

```
/start → /plan → /implement → /check-complete → /gate → /handoff → /verify
```

## 커맨드 목록

| 커맨드 | 설명 |
|--------|------|
| `/start` | 프로젝트 온보딩 |
| `/plan` | 태스크 계획 |
| `/implement` | 계획 실행 |
| `/check-complete` | 껍데기/미연결 검사 |
| `/gate` | lint → test → build |
| `/handoff` | 의도 기록 |
| `/verify` | Context Bias 제거 검증 |
""")]


async def sync_commands(
    path: str,
    mode: str = "merge"
) -> list[TextContent]:
    """
    Clouvel MCP와 Shovel 커맨드 동기화

    Args:
        path: 프로젝트 루트 경로
        mode: merge (병합) / overwrite (덮어쓰기) / skip (건너뛰기)
    """
    project_path = Path(path)
    claude_dir = project_path / ".claude"

    if not claude_dir.exists():
        return [TextContent(type="text", text="""
❌ .claude 폴더가 없습니다.

먼저 install_shovel을 실행하세요:
```
install_shovel로 Shovel 설치해줘
```
""")]

    # Clouvel MCP 도구와 Shovel 커맨드 매핑
    mapping = {
        "can_code": "/check-complete 전에 문서 확인",
        "gate": "/gate",
        "verify": "/verify",
        "handoff": "/handoff",
        "init_planning": "/plan 전 목표 설정",
        "save_finding": "2-Action Rule 자동 적용",
        "refresh_goals": "목표 망각 방지",
        "hook_design": "pre_code 훅",
        "hook_verify": "pre_commit 훅",
    }

    synced = []

    # 각 커맨드에 Clouvel 도구 연동 안내 추가
    for mcp_tool, shovel_cmd in mapping.items():
        synced.append(f"- {mcp_tool} ↔ {shovel_cmd}")

    # CLAUDE.md에 통합 섹션 추가
    claude_md = project_path / "CLAUDE.md"
    if claude_md.exists():
        content = claude_md.read_text(encoding="utf-8")

        if "## Clouvel Pro 통합" not in content:
            integration_section = """

## Clouvel Pro 통합

> MCP 도구와 Shovel 커맨드 자동 연동

### 자동 연동
- `can_code` 실패 시 → 코딩 차단
- `gate` 호출 시 → `/gate` 실행
- `verify` 호출 시 → `/clear` + `/verify` 권장
- `save_finding` → 2-Action Rule 자동 적용

### 워크플로우 (통합)
```
can_code → /plan → /implement → gate → handoff → verify
   MCP      Shovel    Shovel     MCP    MCP      MCP
```
"""
            content += integration_section
            claude_md.write_text(content, encoding="utf-8")

    return [TextContent(type="text", text=f"""
✅ Clouvel + Shovel 동기화 완료!

## 연동된 도구

{chr(10).join(synced)}

## 통합 워크플로우

```
1. can_code (MCP) - 문서 확인
2. /plan (Shovel) - 계획 수립
3. /implement (Shovel) - 구현
4. /check-complete (Shovel) - 껍데기 검사
5. gate (MCP) - 자동 검증
6. handoff (MCP) - 의도 기록
7. verify (MCP) - Context Bias 제거
```

## 자동 연동

| Clouvel MCP | → | Shovel |
|-------------|---|--------|
| can_code 실패 | → | 코딩 차단 |
| gate | → | lint→test→build |
| verify | → | /clear 권장 |
| save_finding | → | 2-Action Rule |
""")]


async def activate_license(
    license_key: str
) -> list[TextContent]:
    """라이선스 활성화"""
    result = verify_license(license_key)

    if result["valid"]:
        return [TextContent(type="text", text=f"""
✅ 라이선스 활성화 완료!

## 정보
- 티어: {result['tier'].upper()}
- 상태: 활성

## 사용 가능 기능
- install_shovel: Shovel 자동 설치
- sync_commands: MCP + Shovel 통합

## 시작하기
```
install_shovel로 Shovel 설치해줘
```
""")]
    else:
        return [TextContent(type="text", text=f"""
❌ 라이선스 활성화 실패

{result['message']}

## 구매
https://clouvel.lemonsqueezy.com
""")]
