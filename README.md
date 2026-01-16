# Clouvel

> **PRD 없으면 코딩 없다.**

바이브코딩 프로세스를 강제하는 MCP 서버.
문서 없이 코딩 시작? 차단됩니다.

---

## 설치

```bash
pip install clouvel
```

또는

```bash
uvx clouvel
```

---

## Claude Code 연동

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

---

## 핵심 도구

| 도구 | 설명 |
|------|------|
| `can_code` | 문서 검사 후 코딩 허용/차단 |
| `get_progress` | 진행 상황 확인 |
| `get_goal` | 프로젝트 목표 리마인드 |

---

## 작동 방식

```
"로그인 기능 만들어줘"
        ↓
   can_code 검사
        ↓
   PRD.md 없음?
        ↓
   ❌ 코딩 차단
        ↓
   "먼저 PRD를 작성하세요"
```

---

## Pro 버전

더 강력한 기능이 필요하다면 **Clouvel Pro**를 확인하세요.

- Shovel 워크플로우 자동 설치
- Gate 시스템 (lint → test → build)
- 검증 프로토콜 (Boris 방식)
- 에러 학습 시스템
- Context 관리 도구

**[Clouvel Pro 보러가기](https://whitening-sinabro.github.io/clouvel/)**

---

## 링크

- [GitHub](https://github.com/Whitening-Sinabro/clouvel)
- [Landing Page](https://whitening-sinabro.github.io/clouvel/)
- [Issues](https://github.com/Whitening-Sinabro/clouvel/issues)

---

## 라이선스

MIT
