import typing
import uuid

from typing import Optional
from app.crm.models import User

if typing.TYPE_CHECKING:
    from app.web.app import Application


class CrmAccessor:
    def __init__(self):
        self.app: Optional["Application"] = None

    # На моменте, когда мы объявляем акссесоры, наше приложение еще не создано.
    # Поэтому мы должны вызвать асинхронные методы.

    # В этом методе происходит подключение к БД, АПИ...
    async def connect(self, app: "Application"):
        self.app = app
        # Блок ниже похож в принципе на
        # if not self.app.database.get("users"): self.app.database["users"] = []
        # но правильнее.
        try:
            self.app.database["users"]
        except KeyError:
            self.app.database["users"] = []
        print("\nconnect to database...\n")

    # В этом методе происходит чистка ресурсов
    # (безопасное отключение от БД, АПИ...)
    async def disconnect(self, _: "Application"):
        self.app = None
        print("\ndisconnect from database...\n")

    async def add_user(self, user: User):
        self.app.database['users'].append(user)

    async def list_users(self):
        return self.app.database['users']

    async def get_user(self, id_: uuid.UUID) -> Optional[User]:
        for user in self.app.database['users']:
            if user.id_ == id_:
                return user
        return None
