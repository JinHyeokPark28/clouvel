# Clouvel

바이브코딩 프로세스를 강제하는 MCP 서버.

**PRD 없으면 코딩 없다.**

---

An MCP server that enforces the vibe-coding process.

**No PRD, No Code.**

## 현재 버전

- MCP 서버: v1.1.0
- Clouvel Pro: v1.1.0 (Shovel 통합)
- VS Code 확장: v0.10.2
- Cursor 확장: v0.10.2

## 설치

### 방법 1: VS Code/Cursor 확장 (추천)

1. 확장 탭에서 "Clouvel" 검색 → 설치
2. `Ctrl+Shift+P` → "Clouvel: Claude Desktop 설정" 선택
3. 끝!

### 방법 2: 수동 설정

Claude Desktop 설정 (`%APPDATA%\Claude\claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "clouvel": {
      "command": "uvx",
      "args": ["clouvel"]
    }
  }
}
```

## 핵심 기능

### can_code - 코딩 차단

```
코딩해도 돼? (can_code로 docs 폴더 확인)
```

- docs 폴더 없음 → **코딩 금지**
- 필수 문서 부족 → **코딩 금지**
- 모든 문서 있음 → **코딩 허용**

### init_docs - 문서 초기화

```
init_docs로 docs 폴더 만들어줘
```

5개 템플릿 자동 생성:
- PRD.md
- ARCHITECTURE.md
- API.md
- DATABASE.md
- VERIFICATION.md

### init_clouvel - 온보딩 (v0.4.0 NEW)

```
clouvel 시작하고 싶어
```

플랫폼 선택 → 맞춤 설정 가이드:
- Claude Desktop → 바로 사용 가능
- VS Code/Cursor → 확장 설치 안내
- Claude Code (CLI) → 자동 설정

### setup_cli - CLI 강제 설정

```
setup_cli로 CLI 설정해줘 (level: strict)
```

Claude Code에서 "PRD 없으면 코딩 금지" 강제:
- `.claude/hooks.json` - Edit/Write 전 경고
- `CLAUDE.md` - 규칙 자동 추가
- `.git/hooks/pre-commit` - 커밋 차단

강제 수준:
| Level | 설명 |
|-------|------|
| `remind` | 경고만 출력 |
| `strict` | 커밋 차단 (추천) |
| `full` | Hooks + 커밋 차단 |

### init_rules - 규칙 모듈화 (v0.5.0 NEW)

```
init_rules로 규칙 구조 만들어줘 (template: api)
```

`.claude/rules/` 구조 생성:
- `global.md` - 전역 규칙
- `api.md` - API 규칙 (api/fullstack)
- `frontend.md` - 프론트엔드 규칙 (web/fullstack)
- `database.md` - DB 규칙
- `security.md` - 보안 규칙

**컨텍스트 절약 50%+** - 필요한 규칙만 로딩!

### get_rule - 경로별 규칙 (v0.5.0 NEW)

```
get_rule로 src/api/users.py 규칙 알려줘
```

파일 경로 기반으로 관련 규칙만 반환:
- `src/api/**` → global + security + api 규칙
- `src/components/**` → global + security + frontend 규칙

### verify - Context Bias 제거 (v0.5.0 NEW)

```
verify로 이 기능 검증해줘
```

Boris 방식 검증:
- 같은 세션에서 자기 코드 검증 → 문제 못 봄
- `/clear` 후 검증 권장

### gate - Gate 검증 (v0.5.0 NEW)

```
gate로 검증해줘
```

lint → test → build 순서로 실행:
- 모두 PASS해야 "완료"
- EVIDENCE.md 자동 생성

### handoff - 의도 기록 (v0.5.0 NEW)

```
handoff로 기록해줘 (feature: "로그인 기능")
```

Step 완료 시 기록:
- 왜 이렇게 했는지
- 주의할 점
- 다음에 해야 할 것

### init_planning - 작업 계획 (v0.6.0 NEW)

```
init_planning으로 계획 세워줘 (task: "로그인 기능", goals: ["API 구현", "UI 구현"])
```

`.claude/planning/` 구조 생성 (Manus 스타일):
- `task_plan.md` - 작업 계획 + 목표
- `findings.md` - 조사 결과 기록
- `progress.md` - 진행 상황 추적

**컨텍스트 유실 방지** - 긴 세션에서도 목표 유지!

### save_finding - 조사 결과 저장 (v0.6.0 NEW)

```
save_finding으로 저장해줘 (topic: "인증", question: "JWT vs Session?", findings: "JWT가 stateless", conclusion: "JWT 선택")
```

2-Action Rule 적용:
- view/browser 작업 2개 후 → 반드시 기록
- 조사 결과가 findings.md에 누적

### refresh_goals - 목표 리마인드 (v0.6.0 NEW)

```
refresh_goals로 목표 확인해줘
```

현재 목표와 진행 상황 출력:
- 긴 세션에서 목표 망각 방지
- task_plan.md + progress.md 요약

### update_progress - 진행 업데이트 (v0.6.0 NEW)

```
update_progress로 업데이트해줘 (completed: ["API 구현"], in_progress: "UI 구현")
```

실시간 진행 추적:
- 완료/진행중/블로커 기록
- progress.md 자동 업데이트

### spawn_explore - 탐색 에이전트 (v0.7.0 NEW)

```
spawn_explore로 탐색해줘 (query: "인증 로직 어디있지?", scope: "project")
```

코드베이스 탐색 전문 에이전트:
- 병렬 조사 + 2-Action Rule 자동 적용
- 탐색 결과를 findings.md에 저장
- 스코프: file / folder / project / deep

### spawn_librarian - 라이브러리언 에이전트 (v0.7.0 NEW)

```
spawn_librarian으로 조사해줘 (topic: "React Query v5 마이그레이션", type: "migration")
```

문서/의존성/API 조사 전문 에이전트:
- 조사 타입: library / api / migration / best_practice
- 조사 깊이: quick / standard / thorough
- 외부 문서 2개 확인 후 findings.md에 기록

### hook_design - 설계 훅 (v0.8.0 NEW)

```
hook_design으로 훅 설정해줘 (trigger: "pre_code", block_on_fail: true)
```

코드 작성 전 자동 체크포인트:
- 트리거: pre_code / pre_feature / pre_refactor / pre_api
- PRD 확인, 아키텍처 검토, 스코프 정의 체크
- 실패 시 코드 작성 차단 가능

### hook_verify - 검증 훅 (v0.8.0 NEW)

```
hook_verify로 검증 설정해줘 (trigger: "pre_commit", steps: ["lint", "test"])
```

코드 완료 후 자동 검증:
- 트리거: post_code / post_feature / pre_commit / pre_push
- lint → test → build → security_scan 순차/병렬 실행
- 에러 시 즉시 중단 또는 계속 진행 설정

## CLI 명령어 (v0.4.0 NEW)

```bash
# 인터랙티브 설정
clouvel init

# 바로 설정 (non-interactive)
clouvel init -p /path/to/project -l strict

# MCP 서버 실행 (Claude가 사용)
clouvel
```

## 전체 도구 목록

### 핵심 도구

| 도구 | 설명 |
|------|------|
| `can_code` | **코딩 가능 여부 확인** - 핵심 기능 |
| `init_clouvel` | **온보딩** - 플랫폼별 맞춤 설정 |
| `setup_cli` | **CLI 강제 설정** - hooks, pre-commit |

### v0.5.0 (규칙 모듈화 + 검증)

| 도구 | 설명 |
|------|------|
| `init_rules` | `.claude/rules/` 구조 생성 |
| `get_rule` | 경로 기반 규칙 로딩 |
| `add_rule` | 새 규칙 추가 (NEVER/ALWAYS) |
| `verify` | Context Bias 제거 검증 |
| `gate` | lint→test→build 자동화 |
| `handoff` | 의도 기록 + 저장 |

### v0.6.0 (영속적 컨텍스트)

| 도구 | 설명 |
|------|------|
| `init_planning` | `.claude/planning/` 구조 생성 |
| `save_finding` | 조사 결과 findings.md에 저장 |
| `refresh_goals` | 현재 목표 + 진행 리마인드 |
| `update_progress` | 진행 상황 업데이트 |

### v0.7.0 (전문화 에이전트)

| 도구 | 설명 |
|------|------|
| `spawn_explore` | 탐색 전문 에이전트 (코드베이스 탐색) |
| `spawn_librarian` | 라이브러리언 에이전트 (문서/API 조사) |

### v0.8.0 (자동화 훅 확장)

| 도구 | 설명 |
|------|------|
| `hook_design` | 설계 훅 (코드 작성 전 체크포인트) |
| `hook_verify` | 검증 훅 (코드 완료 후 자동 검증) |

### v1.1.0 Pro (Shovel 통합) 🆕

| 도구 | 설명 |
|------|------|
| `install_shovel` | 🆕 Shovel .claude/ 자동 설치 (라이선스 필요) |
| `sync_commands` | 🆕 Clouvel MCP + Shovel 커맨드 통합 |
| `activate_license` | 🆕 라이선스 활성화 |

### 문서 도구

| 도구 | 설명 |
|------|------|
| `init_docs` | docs 폴더 초기화 + 템플릿 생성 |
| `scan_docs` | docs 폴더 파일 목록 |
| `analyze_docs` | 필수 문서 체크, 빠진 거 알려줌 |
| `get_prd_template` | PRD 템플릿 생성 (11개 섹션) |
| `write_prd_section` | 섹션별 PRD 작성 가이드 |
| `get_prd_guide` | PRD 작성 가이드 |
| `get_verify_checklist` | 검증 체크리스트 |
| `get_setup_guide` | 설치/설정 가이드 |
| `get_analytics` | 도구 사용량 통계 (로컬 저장) |

## 사용 플로우

```
1. can_code → "코딩 금지" (문서 없음)
2. init_docs → 빈 템플릿 생성
3. Claude와 함께 PRD 작성
4. can_code → "코딩 허용"
5. 코딩 시작!
```

## 필수 문서

`can_code`가 체크하는 것들:

- **PRD** (제품 요구사항) - 가장 중요
- **아키텍처** 문서
- **API** 스펙
- **DB** 스키마
- **검증** 계획

다 있어야 코딩 허용.

## VS Code/Cursor 확장 기능

- 원클릭 MCP 서버 설정
- 사이드바에서 문서 상태 확인
- 코드 파일에 경고 표시 (Diagnostic)
- 프로젝트 유형별 PRD 템플릿 (수익화/개인/사내)

## 로드맵

> 피드백에 따라 변경/추가/삭제될 수 있습니다.

| 버전 | 목표 | 상태 |
|------|------|------|
| **v0.1.0** | MVP - can_code, scan_docs, init_docs 등 10개 도구 | ✅ |
| **v0.4.0** | CLI 온보딩 - init_clouvel, setup_cli, clouvel init | ✅ |
| **v0.5.0** | 규칙 모듈화 + 검증 프로토콜 - init_rules, get_rule, verify, gate, handoff | ✅ |
| **v0.6.0** | 영속적 컨텍스트 - init_planning, save_finding, refresh_goals, update_progress | ✅ |
| **v0.7.0** | 전문화된 에이전트 - spawn_explore, spawn_librarian | ✅ |
| **v0.8.0** | 자동화 훅 확장 - hook_design, hook_verify | ✅ |
| **v1.0.0** | 정식 출시 - 리팩토링 + 테스트 + 안정화 | ✅ |
| **v1.1.0** | Clouvel Pro - Shovel 자동 설치, 라이선스 시스템 | ✅ |

자세한 내용: [ROADMAP.md](https://github.com/JinHyeokPark28/clouvel/blob/main/ROADMAP.md)

## Clouvel Pro (유료)

Clouvel 무료 + Shovel 자동 통합

### 가격

| 티어 | 가격 | 라이선스 |
|------|------|----------|
| Personal | $29 | 1명 |
| Team | $79 | 10명 |
| Enterprise | $199 | 무제한 |

### 구매

https://clouvel.lemonsqueezy.com

### Pro 기능

```
activate_license로 라이선스 활성화해줘 (license_key: "CLOUVEL-PERSONAL-XXX")
```

```
install_shovel로 Shovel 설치해줘
```

설치 시 포함:
- `.claude/commands/` - 7개 핵심 커맨드 (/gate, /verify, /plan 등)
- `.claude/templates/` - PRD, findings 템플릿
- `.claude/settings.json` - 권한 + 훅 설정
- `scripts/gate.sh` - Gate 스크립트

## 왜?

바이브코딩 = AI가 코드 짬.
근데 PRD 없이 시작하면 = 나중에 다 뜯어고침.

**Clouvel = 문서 없으면 코딩 못 하게 강제.**

## 피드백 / 버그 리포트

[GitHub Issues](https://github.com/JinHyeokPark28/clouvel/issues)에 남겨주세요!

## License

MIT
