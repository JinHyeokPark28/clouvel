#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SessionStart Hook: 컨텍스트 압축 후 자동 복구"""

import json
import sys
import os
from pathlib import Path

# Windows UTF-8 stdout 설정
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stdin.reconfigure(encoding='utf-8')

def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        # 입력 없으면 빈 컨텍스트
        output = {"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": ""}}
        print(json.dumps(output))
        sys.exit(0)

    source = input_data.get("source", "startup")
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", ".")
    project_path = Path(project_dir)

    # startup이면 복구 불필요 (새 세션)
    if source == "startup":
        output = {"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": ""}}
        print(json.dumps(output))
        sys.exit(0)

    # compact, resume일 때만 복구
    state_file = project_path / ".claude" / "status" / "session-state.json"

    if not state_file.exists():
        output = {"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": ""}}
        print(json.dumps(output))
        sys.exit(0)

    try:
        state = json.loads(state_file.read_text(encoding="utf-8"))
    except:
        output = {"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": ""}}
        print(json.dumps(output))
        sys.exit(0)

    # 복구 컨텍스트 생성
    parts = []
    parts.append("# Context Recovery (Auto-injected)")
    parts.append("")
    parts.append(f"> **Source**: {source}")
    parts.append(f"> **Saved at**: {state.get('timestamp', 'unknown')}")

    if state.get("git_branch"):
        parts.append(f"> **Branch**: {state['git_branch']}")

    # 활성 계획
    if state.get("active_plan"):
        parts.append("")
        parts.append(f"## Active Plan: {state['active_plan']}")
        parts.append("")
        parts.append("```markdown")
        # 처음 50줄만
        plan_lines = state.get("plan_content", "").split("\n")[:50]
        parts.append("\n".join(plan_lines))
        parts.append("```")

    # 현재 상태 요약
    if state.get("current_md"):
        parts.append("")
        parts.append("## Current Status (from current.md)")
        parts.append("")
        # 처음 40줄만
        current_lines = state["current_md"].split("\n")[:40]
        parts.append("\n".join(current_lines))

    # 핵심 규칙
    if state.get("rules"):
        parts.append("")
        parts.append("## Key Rules")
        for rule in state["rules"]:
            parts.append(f"- {rule}")

    parts.append("")
    parts.append("---")
    parts.append("**Continue where you left off.**")

    context = "\n".join(parts)

    output = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": context
        }
    }

    print(json.dumps(output, ensure_ascii=False))
    sys.exit(0)

if __name__ == "__main__":
    main()
