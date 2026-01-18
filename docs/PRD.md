# Clouvel PRD

> PRD 없으면 코딩 없다.

## 한 줄 정의

바이브코딩 프로세스를 강제하는 MCP 서버

## 핵심 기능

- `can_code`: 문서 검사 후 코딩 허용/차단
- `get_progress`: 진행 상황 확인
- `get_goal`: 목표 리마인드

## 타겟

Claude Code 사용자 중 바이브코딩 초보자

## Acceptance (완료 기준)

- [ ] `can_code` 호출 시 PRD 없으면 BLOCK
- [ ] `can_code` 호출 시 acceptance 섹션 없으면 BLOCK
- [ ] `can_code` 호출 시 권장 문서 없으면 WARN (진행 가능)
- [ ] `clouvel setup` 실행 시 글로벌 CLAUDE.md에 규칙 추가
- [ ] `clouvel setup` 실행 시 MCP 서버 자동 등록
- [ ] Claude가 코드 작성 전 자동으로 `can_code` 호출
