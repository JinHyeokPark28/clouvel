"""
Clouvel Analytics - 도구 사용량 로컬 추적

저장 위치: .clouvel/analytics.json (프로젝트 로컬)
개인정보 없음, 순수 사용량 통계만 기록
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional


def get_analytics_path(project_path: Optional[str] = None) -> Path:
    """analytics.json 경로 반환"""
    if project_path:
        base = Path(project_path)
    else:
        base = Path.cwd()

    clouvel_dir = base / ".clouvel"
    clouvel_dir.mkdir(parents=True, exist_ok=True)
    return clouvel_dir / "analytics.json"


def load_analytics(project_path: Optional[str] = None) -> dict:
    """analytics 데이터 로드"""
    path = get_analytics_path(project_path)
    if path.exists():
        try:
            return json.loads(path.read_text(encoding='utf-8'))
        except (json.JSONDecodeError, IOError):
            return {"events": [], "version": "1.0"}
    return {"events": [], "version": "1.0"}


def save_analytics(data: dict, project_path: Optional[str] = None) -> None:
    """analytics 데이터 저장"""
    path = get_analytics_path(project_path)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def log_tool_call(tool_name: str, success: bool = True, project_path: Optional[str] = None) -> None:
    """도구 호출 기록"""
    data = load_analytics(project_path)

    event = {
        "tool": tool_name,
        "ts": datetime.now().isoformat(),
        "success": success
    }

    data["events"].append(event)

    # 최근 1000개만 유지 (메모리 관리)
    if len(data["events"]) > 1000:
        data["events"] = data["events"][-1000:]

    save_analytics(data, project_path)


def get_stats(project_path: Optional[str] = None, days: int = 30) -> dict:
    """사용량 통계 반환"""
    data = load_analytics(project_path)
    events = data.get("events", [])

    if not events:
        return {
            "total_calls": 0,
            "by_tool": {},
            "by_date": {},
            "success_rate": 0,
            "period_days": days
        }

    # 기간 필터
    cutoff = datetime.now() - timedelta(days=days)
    filtered = []
    for e in events:
        try:
            ts = datetime.fromisoformat(e["ts"])
            if ts >= cutoff:
                filtered.append(e)
        except (KeyError, ValueError):
            continue

    # 도구별 집계
    by_tool = {}
    by_date = {}
    success_count = 0

    for e in filtered:
        tool = e.get("tool", "unknown")
        by_tool[tool] = by_tool.get(tool, 0) + 1

        try:
            date = datetime.fromisoformat(e["ts"]).strftime("%Y-%m-%d")
            by_date[date] = by_date.get(date, 0) + 1
        except (KeyError, ValueError):
            pass

        if e.get("success", True):
            success_count += 1

    total = len(filtered)

    return {
        "total_calls": total,
        "by_tool": dict(sorted(by_tool.items(), key=lambda x: x[1], reverse=True)),
        "by_date": dict(sorted(by_date.items())),
        "success_rate": round(success_count / total * 100, 1) if total > 0 else 0,
        "period_days": days
    }


def format_stats(stats: dict) -> str:
    """통계를 읽기 좋은 문자열로 변환"""
    lines = [
        f"# Clouvel 사용량 통계 (최근 {stats['period_days']}일)",
        "",
        f"## 요약",
        f"- 총 호출: {stats['total_calls']}회",
        f"- 성공률: {stats['success_rate']}%",
        "",
    ]

    if stats["by_tool"]:
        lines.append("## 도구별 사용량")
        lines.append("")
        lines.append("| 도구 | 횟수 | 비율 |")
        lines.append("|------|------|------|")
        total = stats["total_calls"]
        for tool, count in stats["by_tool"].items():
            pct = round(count / total * 100, 1) if total > 0 else 0
            lines.append(f"| {tool} | {count} | {pct}% |")
        lines.append("")

    if stats["by_date"]:
        lines.append("## 일별 사용량")
        lines.append("")
        # 최근 7일만 표시
        recent_dates = list(stats["by_date"].items())[-7:]
        for date, count in recent_dates:
            bar = "█" * min(count, 20)
            lines.append(f"- {date}: {bar} {count}")
        lines.append("")

    if stats["total_calls"] == 0:
        lines.append("아직 기록된 사용량이 없습니다.")

    return "\n".join(lines)
