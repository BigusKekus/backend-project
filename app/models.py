from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class DataStore:
    users: dict[int, dict[str, Any]] = field(default_factory=dict)
    categories: dict[int, dict[str, Any]] = field(default_factory=dict)
    records: dict[int, dict[str, Any]] = field(default_factory=dict)

    user_seq: int = 1
    category_seq: int = 1
    record_seq: int = 1

    def seed(self) -> None:

        if not self.categories:
            self.create_category("Food")
            self.create_category("Transport")
            self.create_category("Subscriptions")

        if not self.users:
            u = self.create_user("Misha")

            self.create_record(user_id=u["id"], category_id=1, amount=120.5)
            self.create_record(user_id=u["id"], category_id=2, amount=60)


    def create_user(self, name: str) -> dict[str, Any]:
        user = {"id": self.user_seq, "name": name}
        self.users[self.user_seq] = user
        self.user_seq += 1
        return user

    def delete_user(self, user_id: int) -> bool:
        if user_id not in self.users:
            return False
        del self.users[user_id]

        to_delete = [rid for rid, r in self.records.items() if r["user_id"] == user_id]
        for rid in to_delete:
            del self.records[rid]
        return True

    def create_category(self, name: str) -> dict[str, Any]:
        cat = {"id": self.category_seq, "name": name}
        self.categories[self.category_seq] = cat
        self.category_seq += 1
        return cat

    def delete_category(self, category_id: int) -> bool:
        if category_id not in self.categories:
            return False
        del self.categories[category_id]

        to_delete = [
            rid for rid, r in self.records.items() if r["category_id"] == category_id
        ]
        for rid in to_delete:
            del self.records[rid]
        return True

    def create_record(
        self,
        user_id: int,
        category_id: int,
        amount: float,
        created_at: str | None = None,
    ) -> dict[str, Any]:
        rec = {
            "id": self.record_seq,
            "user_id": user_id,
            "category_id": category_id,
            "created_at": created_at or utc_now_iso(),
            "sum": amount,
        }
        self.records[self.record_seq] = rec
        self.record_seq += 1
        return rec

    def delete_record(self, record_id: int) -> bool:
        if record_id not in self.records:
            return False
        del self.records[record_id]
        return True


STORE = DataStore()
STORE.seed()
