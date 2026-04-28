import logging
import psycopg2

from app.config import settings

logger = logging.getLogger(__name__)


def get_connection():
    """
    Creates a new PostgreSQL database connection.

    Flow:
    1. Read DB config from settings
    2. Establish connection
    3. Return connection object
    """

    try:
        logger.info("Creating database connection to host=%s db=%s",
                    settings.db_host,
                    settings.db_name)

        conn = psycopg2.connect(
            dbname=settings.db_name,
            user=settings.db_user,
            password=settings.db_password,
            host=settings.db_host,
            port=settings.db_port
        )

        logger.info("Database connection established successfully")
        return conn

    except Exception:
        logger.error("Failed to create database connection", exc_info=True)
        raise