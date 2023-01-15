from typing import List


class Repo:
    """Db abstraction layer"""

    def __init__(self, conn):
        self.conn = conn

    # users
    async def add_user(self, user_id, sorting_order) -> None:
        """Store user in DB, ignore duplicates"""
        await self.conn.execute(
            "INSERT INTO tg_users(user_id, sorting_order) VALUES ($1, $2) ON CONFLICT DO NOTHING",
            user_id,
            sorting_order,
        )
        return

    async def get_user_sort_order(self, user_id) -> str:
        order_record = await self.conn.fetchval(
            "SELECT sorting_order FROM tg_users WHERE user_id = $1", user_id
        )
        return order_record

    async def invert_user_sort_order(self, user_id, order):
        await self.conn.execute(
            "UPDATE tg_users SET sorting_order = $1 WHERE user_id = $2",
            order,
            user_id,
        )

    async def list_users(self) -> List[int]:
        """List all bot users"""
        users = await self.conn.fetch("SELECT * FROM tg_users")
        return users
