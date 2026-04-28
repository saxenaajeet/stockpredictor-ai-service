import logging
from app.config import settings


def setup_logging():
    # Convert string → logging level
    log_level = getattr(logging, settings.logging_level.upper(), logging.INFO)

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    logging.getLogger().info(f"Logging initialized with level={settings.logging_level}")