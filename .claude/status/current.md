# Clouvel 현재 상태

> **마지막 업데이트**: 2026-01-18 (저녁)

---

## 지금 상태

| 항목 | 상태 |
|------|------|
| **clouvel (Free)** | PyPI v0.5.0 (3개 도구) |
| **clouvel-pro (Paid)** | PyPI v1.4.2 (23개 MCP 도구) |
| **랜딩 페이지** | 배포 완료 + 기술 문서 추가 |
| **라이선스 서버** | ✅ 동작 중 (`clouvel-license-webhook.vnddns999.workers.dev`) |
| **Lemon Squeezy** | ⏳ Identity 인증 심사 중 (24-48h) |
| **블로커** | Identity 인증 대기 → Store 활성화 → Email 활성화 |

---

## 완료된 기능 (v1.4.2)

### Free (clouvel)
- [x] can_code - 문서 강제
- [x] get_progress - 진행 상황
- [x] get_goal - 목표 리마인드

### Pro (clouvel-pro) - $49 (Early Bird)
- [x] activate_license - Lemon Squeezy 연동
- [x] check_license - 라이선스 상태
- [x] install_shovel - 24개 슬래시 커맨드
- [x] sync_commands - 커맨드 동기화
- [x] log_error - 에러 기록
- [x] analyze_error - 에러 분석
- [x] get_error_summary - 에러 요약
- [x] add_prevention_rule - NEVER/ALWAYS 규칙
- [x] watch_logs - 로그 감시
- [x] check_logs - 로그 상태
- [x] recover_context - 컨텍스트 복구 (핵심!)

### Team (clouvel-pro) - $149 (Early Bird)
- [x] team_invite - 팀원 초대
- [x] team_members - 팀원 목록
- [x] team_remove - 팀원 제거
- [x] team_settings - C-Level 설정
- [x] team_toggle_role - 역할 토글
- [x] sync_team_errors - 에러 팀 동기화
- [x] get_team_rules - 팀 규칙 조회
- [x] apply_team_rules - 팀 규칙 적용
- [x] sync_project_context - 컨텍스트 업로드
- [x] get_project_context - 컨텍스트 조회

---

## 오늘 완료 (2026-01-18)

- [x] 랜딩 페이지 인터랙티브 모달 추가
- [x] 기술 문서 페이지 (docs.html) 생성
- [x] DEV_MODE MCP 테스트 완료 (20개 도구)
- [x] recover_context 도구 구현 (컨텍스트 압축 후 자동 복구)
- [x] setup_auto_recovery 도구 구현 (Hook 자동 설치)
- [x] Claude Code Hook 연동 (PreCompact + SessionStart)
- [x] **/compact 실제 테스트 → 컨텍스트 복구 성공**
- [x] Windows UTF-8 인코딩 이슈 해결 (hooks)
- [x] Lemon Squeezy 상품 생성 + 가격 확정 (Personal $49, Team $149)
- [x] Lemon Squeezy 웹훅 URL 등록 완료
- [x] 실제 라이선스 키 E2E 테스트 완료
- [x] 어드민 대시보드 배포 (`clouvel-admin.pages.dev`)
- [x] 가격 전략 확정 (Early Bird until Feb 15)

---

## 개발 우선순위

```
1. ✅ 개인화 기능 (Pro 10개) - 완료
2. ✅ 팀 기능 (Team 10개) - 완료
3. ✅ 라이선스 서버 배포 - 완료
4. ✅ Lemon Squeezy 결제 연동 - 완료
5. ⏳ Lemon Squeezy Identity 인증 대기 중
6. ⏳ v1.5 Analytics Dashboard
```

---

## 로드맵

### v1.5 - 정식 출시 (Now)
| 항목 | 상태 |
|------|------|
| 라이선스 서버 | ✅ 완료 |
| Lemon Squeezy 연동 | ✅ 완료 |
| 가격 확정 | ✅ $49 / $149 (until Feb 15) |
| 가격 문구 확정 | ✅ After launch 방식 채택 |
| Identity 인증 | ⏳ 심사 중 (24-48h) |
| Store 활성화 | ⏳ 인증 후 |
| 랜딩 페이지 가격 업데이트 | ⏳ 진행 중 |

### v1.6 - 마케팅 (출시 후 1-2주)
- [ ] Twitter/X 계정 + 홍보
- [ ] 데모 영상 (컨텍스트 복구 전후 비교)
- [ ] ProductHunt 런칭
- [ ] 블로그 포스트 ("Claude Code 컨텍스트 문제 해결")

### v1.7 - Analytics (출시 후 1개월)
- [ ] 에러 패턴 시각화 대시보드
- [ ] 팀 생산성 메트릭
- [ ] 웹 대시보드 UI

### v2.0 - Enterprise (3-6개월)
- [ ] SSO 통합
- [ ] 감사 로그
- [ ] 온프레미스 배포
- [ ] 가격 인상: $79 / $249 (정가)

---

## 가격 전략

| 단계 | Personal | Team | 시점 |
|------|----------|------|------|
| Early Bird | **$49** | **$149** | ~ Feb 15, 2026 |
| After Launch | $79 | $249 | Feb 16~ |

### 랜딩 페이지 문구 (확정)
```
Early Bird Pricing (until Feb 15)

Personal: $49 (After launch: $79)
Team: $149 (After launch: $249)

✅ Early Bird includes priority support (30 days)
```

### 주의사항
- "First 100" 안 씀 (카운터 없으면 구라로 보임)
- "40% OFF" 안 씀 (계산 불일치 리스크)
- 날짜 박아서 신뢰 확보

---

## BACKLOG

→ `docs/BACKLOG.md` 참조

- api.clouvel.dev 커스텀 도메인 (유저 늘면)
- 문서 자동 생성 스크립트
