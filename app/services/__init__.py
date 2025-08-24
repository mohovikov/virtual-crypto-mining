from .clan import (
    create_clan,
    get_clan_info,
    get_clan_profile,
    save_clan_settings,
    join_clan,
    leave_clan
)
from .cryptocurrency import (
    get_all_cryptocurrencies,
    get_cryptocurrency,
    create_cryptocurrency,
    edit_cryptocurrency,
    update_price_cryptocurrency,
    add_crypto_price_history
)
from .jobs import (
    get_all_jobs,
    remove_job,
    pause_job,
    resume_job
)
from .privileges import (
    get_all_privileges,
    get_privilege_group,
    add_privilege_group
)
from .scheduler_log import (
    get_all_jobs_logs,
    get_job_logs_by_id,
    add_scheduler_log
)
from .settings import (
    update_avatar,
    update_profile,
    update_userpage
)
from .sponsor import (
    give_sponsor
)
from .users import (
    create_user,
    login_user,
    get_all_users,
    get_user_data
)

__all__ = [
    # Clans
    "create_clan",
    "get_clan_info",
    "get_clan_profile",
    "save_clan_settings",
    "join_clan",
    "leave_clan",

    # Cryptocurrency
    "get_all_cryptocurrencies",
    "get_cryptocurrency",
    "create_cryptocurrency",
    "edit_cryptocurrency",
    "update_price_cryptocurrency",
    "add_crypto_price_history",

    "get_all_jobs",
    "remove_job",
    "pause_job",
    "resume_job",

    # Privileges Groups
    "get_all_privileges",
    "get_privilege_group",
    "add_privilege_group",

    # Scheduler Logs
    "get_all_jobs_logs",
    "get_job_logs_by_id",
    "add_scheduler_log",

    # User Settings
    "update_avatar",
    "update_profile",
    "update_userpage",

    # Sponsor
    "give_sponsor",

    # Users
    "create_user",
    "login_user",
    "get_all_users",
    "get_user_data",
]