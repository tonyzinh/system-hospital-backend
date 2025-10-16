import os

# Allow selecting an environment via DJANGO_ENV (dev, prod). Default to dev.
_env = os.getenv("DJANGO_ENV", "dev").lower()
if _env == "prod":
	from .prod import *  # type: ignore
elif _env == "dev":
	from .dev import *  # type: ignore
else:
	# Fallback to base for any other value
	from .base import *  # type: ignore

