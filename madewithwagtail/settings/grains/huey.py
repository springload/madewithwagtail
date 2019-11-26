import dj_database_url
from madewithwagtail.settings import *

HUEY = {
    "huey_class": "huey.contrib.SqlHuey",
    "name": "-".join(["huey", PROJECT, ENVIRONMENT]),
    "results": True,  # Store return values of tasks.
    "store_none": False,  # If a task returns None, do not save to results.
    "immediate": False,  # run asynchronously.
    "blocking": False,  # Poll the queue rather than do blocking pop.
    "utc": True,  # Treat ETAs and schedules as UTC datetimes.
    "connection": {
        # huey-specific connection parameters.
        "read_timeout": 1,  # If not polling (blocking pop), use timeout.
        "url": DATABASE_URL,  # Allow Redis config via a DSN.
    },
    "consumer": {
        "workers": 3,
        "worker_type": "process",
        "initial_delay": 0.1,  # Smallest polling interval, same as -d.
        "backoff": 1.15,  # Exponential backoff using this rate, -b.
        "max_delay": 10.0,  # Max possible polling interval, -m.
        "scheduler_interval": 1,  # Check schedule every second, -s.
        "periodic": True,  # Enable crontab feature.
        "check_worker_health": True,  # Enable worker health checks.
        "health_check_interval": 1,  # Check worker health every second.
    },
}
