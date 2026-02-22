# from datetime import date
#
# from marshmallow.fields import Decimal
#
# from api.services.exceptions import UserNotFoundError, CreatePaymentError
# from api.utils.yookassa import create_payment
# from database.models import Clients, Subscription
# from database.repository.clients_repository import ClientRepository
# from database.repository.subscription_repository import SubscriptionRepository
# from database.repository.payments_repository import PaymentsRepository
#
#
# class UserService:
#     def __init__(
#             self,
#             client_repo: ClientRepository,
#             sub_repo: SubscriptionRepository,
#             payments_repo: PaymentsRepository,
#     ):
#         self.client_repo = client_repo
#         self.sub_repo = sub_repo
#         self.payments_repo = payments_repo
#
#     async def handle_start(self, telegram_id: int) -> dict[str, str | dict[str, int | str] | dict[
#         str, int | None | date | str]] | dict[str, str]:
#         """
#         1. Проверяем существование клиента
#         2. Проверяем наличие телефона
#         3. Возвращаем либо REQUEST_PHONE, либо SHOW_CABINET
#         """
#
#         client = await self.client_repo.get_by_telegram_id(telegram_id)
#         if not client:
#             raise UserNotFoundError()
#
#         # телефон не заполнен
#         if not client.phone_number or client.phone_number == "0":
#             return {
#                 "action": "REQUEST_PHONE"
#             }
#
#         subscription = await self.sub_repo.get_subscription_by_client(client.telegram_id)
#
#         return {
#             "action": "SHOW_CABINET",
#             "client": {
#                 "id": client.id,
#                 "telegram_id": client.telegram_id,
#                 "full_name": client.full_name,
#                 "phone_number": client.phone_number,
#                 "status": client.status,
#             },
#             "subscription": {
#                 "id": subscription.id if subscription else None,
#                 "amount": subscription.amount if subscription else None,
#                 "due_date": subscription.due_date if subscription else None,
#                 "status": subscription.status if subscription else None,
#             }
#         }
#
#     async def save_phone(self, telegram_id: int, phone_number: str) -> None:
#         """
#         Сохраняем номер телефона пользователю.
#         Пользователь должен существовать.
#         """
#
#         client = await self.client_repo.get_by_telegram_id(telegram_id)
#         if not client:
#             raise UserNotFoundError()
#
#         await self.client_repo.update_phone_number(
#             telegram_id=telegram_id,
#             phone_number=phone_number,
#         )
#
#     async def get_cabinet(self, telegram_id: int) -> dict:
#         """
#         Возвращает данные ЛК.
#         Предполагается, что телефон уже заполнен.
#         """
#
#         client = await self.client_repo.get_by_telegram_id(telegram_id)
#         if not client:
#             raise UserNotFoundError()
#
#         subscription = await self.sub_repo.get_active_by_client(client.id)
#
#         return {
#             "client": {
#                 "id": client.id,
#                 "telegram_id": client.telegram_id,
#                 "full_name": client.full_name,
#                 "phone_number": client.phone_number,
#                 "status": client.status,
#             },
#             "subscription": {
#                 "id": subscription.id if subscription else None,
#                 "amount": subscription.amount if subscription else None,
#                 "due_date": subscription.due_date if subscription else None,
#                 "status": subscription.status if subscription else None,
#             },
#         }
#
#
