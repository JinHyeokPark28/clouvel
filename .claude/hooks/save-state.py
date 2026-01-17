#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PreCompact Hook: 컨텍스트 압축 전 상태 저장"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

# Windows UTF-8 설정
if sys.platform == "win32":
    sys.stdin.reconfigure(encoding='utf-8')

def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(1)

    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", ".")
    project_path = Path(project_dir)

    # 상태 수집
    state = {
        "timestamp": datetime.now().isoformat(),
        "trigger": input_data.get("trigger", "unknown"),
        "session_id": input_data.get("session_id", "")
    }

    # current.md 읽기
    current_md = project_path / ".claude" / "status" / "current.md"
    if current_md.exists():
        try:
            state["current_md"] = current_md.read_text(encoding="utf-8")[:3000]
        except:
            pass

    # 활성 PLAN 찾기
    plans_dir = project_path / ".claude" / "plans"
    if plans_dir.exists():
        for f in plans_dir.glob("PLAN-*.md"):
            try:
                content = f.read_text(encoding="utf-8")
                if "LOCKED" in content or "IN_PROGRESS" in content or "진행 중" in content:
                    state["active_plan"] = f.name
                    state["plan_content"] = content[:2000]
                    break
            except:
                continue

    # CLAUDE.md 핵심 규칙
    claude_md = project_path / "CLAUDE.md"
    if claude_md.exists():
        try:
            content = claude_md.read_text(encoding="utf-8")
            # NEVER/ALWAYS 추출
            import re
            rules = []
            for match in re.findall(r"NEVER[:\s]+([^\n]+)", content, re.IGNORECASE)[:5]:
                rules.append(f"NEVER: {match.strip()}")
            for match in re.findall(r"ALWAYS[:\s]+([^\n]+)", content, re.IGNORECASE)[:5]:
                rules.append(f"ALWAYS: {match.strip()}")
            if rules:
                state["rules"] = rules
        except:
            pass

    # Git 브랜치
    git_head = project_path / ".git" / "HEAD"
    if git_head.exists():
        try:
            head_content = git_head.read_text(encoding="utf-8").strip()
            if head_content.startswith("ref: refs/heads/"):
                state["git_branch"] = head_content.replace("ref: refs/heads/", "")
        except:
            pass

    # 저장
    state_dir = project_path / ".claude" / "status"
    state_dir.mkdir(parents=True, exist_ok=True)
    state_file = state_dir / "session-state.json"

    try:
        state_file.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    except:
        pass

    sys.exit(0)

if __name__ == "__main__":
    main()
