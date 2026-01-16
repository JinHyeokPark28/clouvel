# Clouvel Tools Package
# 모듈별로 도구 구현을 분리

from .core import (
    can_code,
    scan_docs,
    analyze_docs,
    init_docs,
    REQUIRED_DOCS,
)

from .docs import (
    get_prd_template,
    write_prd_section,
    get_prd_guide,
    get_verify_checklist,
    get_setup_guide,
)

from .setup import (
    init_clouvel,
    setup_cli,
)

from .rules import (
    init_rules,
    get_rule,
    add_rule,
)

from .verify import (
    verify,
    gate,
    handoff,
)

from .planning import (
    init_planning,
    save_finding,
    refresh_goals,
    update_progress,
)

from .agents import (
    spawn_explore,
    spawn_librarian,
)

from .hooks import (
    hook_design,
    hook_verify,
)

from .pro import (
    install_shovel,
    sync_commands,
    activate_license,
)

__all__ = [
    # core
    "can_code", "scan_docs", "analyze_docs", "init_docs", "REQUIRED_DOCS",
    # docs
    "get_prd_template", "write_prd_section", "get_prd_guide", "get_verify_checklist", "get_setup_guide",
    # setup
    "init_clouvel", "setup_cli",
    # rules (v0.5)
    "init_rules", "get_rule", "add_rule",
    # verify (v0.5)
    "verify", "gate", "handoff",
    # planning (v0.6)
    "init_planning", "save_finding", "refresh_goals", "update_progress",
    # agents (v0.7)
    "spawn_explore", "spawn_librarian",
    # hooks (v0.8)
    "hook_design", "hook_verify",
    # pro (v1.1)
    "install_shovel", "sync_commands", "activate_license",
]
