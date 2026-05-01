
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from Backend.DB.main import init_db, engine


async def main():
    """Create all database tables."""
    try:
        print("Initializing database tables...")
        await init_db()
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
