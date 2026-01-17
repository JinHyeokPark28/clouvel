# Clouvel 현재 상태

> **마지막 업데이트**: 2026-01-17

---

## 지금 상태

- **PyPI 배포**: v0.4.0 ✅
- **개발 버전**: dev (pyproject.toml)
- **단계**: 스케줄 배포 시스템 구축 완료
- **블로커**: 없음

---

## 배포 시스템

```
releases/
├── v0.5.0.toml  (1/17 배포)
├── v0.6.0.toml  (1/20 배포)
├── v0.7.0.toml  (1/23 배포)
└── v0.8.0.toml  (1/26 배포, 마지막 공개)

pyproject.toml → 개발용 (version = "dev")
scheduled-release.yml → 배포 시 releases/*.toml 복사
```

---

## 완료 목록

- [x] v0.4.0 PyPI 배포 완료
- [x] **배포 시스템 개선** (2026-01-17)
  - releases/ 폴더에 버전별 toml 분리
  - scheduled-release.yml 수정 (날짜→버전 매핑 + toml 복사)
  - pyproject.toml을 dev 버전으로 설정

---

## 배포 스케줄

| 버전 | 날짜 | 주요 기능 |
|------|------|----------|
| v0.5.0 | 1/17 | Rules + Verify |
| v0.6.0 | 1/20 | Planning |
| v0.7.0 | 1/23 | Agents |
| v0.8.0 | 1/26 | Hooks (마지막) |

---

## 다음 할 일

- [ ] v0.5.0 기능 구현 확인 (Rules, Verify)
- [ ] GitHub Actions 수동 실행으로 v0.5.0 배포 테스트
- [ ] 각 버전별 기능 구현 상태 점검

---

## 주의사항

- 개발 중 pyproject.toml 버전은 "dev" 유지
- 배포는 releases/*.toml 파일로 관리
- 수동 배포: GitHub Actions > scheduled-release > Run workflow
