import aiosqlite
import json
import time
from typing import Optional

class LocalCache:
    def __init__(self, db_path: str):
        self.db_path = db_path

    async def init_db(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS cache (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    timestamp REAL
                )
            """)
            await db.commit()

    async def get(self, key: str, ttl: int) -> Optional[dict]:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT value, timestamp FROM cache WHERE key = ?", (key,)) as cursor:
                row = await cursor.fetchone()
                if row:
                    value, timestamp = row
                    if time.time() - timestamp < ttl:
                        return json.loads(value)
        return None

    async def set(self, key: str, value: dict):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT OR REPLACE INTO cache (key, value, timestamp) VALUES (?, ?, ?)",
                (key, json.dumps(value), time.time())
            )
            await db.commit()
