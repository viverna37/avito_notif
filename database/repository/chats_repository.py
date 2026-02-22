from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Chats


class ChatsRepository:
    """
    Репозиторий для работы с подписками
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
            self,
            chat_id: str,
    ) -> Chats:
        """Создать чат"""
        chat = Chats(
            chat_id=chat_id
        )
        self.session.add(chat)
        await self.session.commit()
        await self.session.refresh(chat)
        return chat

    async def get_chat(
            self,
            chat_id: str
    ) -> Chats | None:
        """Проверить существование чата. При отсутствии создать"""
        result = await self.session.execute(
            select(Chats).where(
                Chats.chat_id == str(chat_id)
            )
        )
        result = result.scalar_one_or_none()

        if result:
            return result
        else:
            await self.create(chat_id)
            return None
