import datetime
import uuid

from app.models.tenders import TenderStatus
from app.repositories.unit_of_work import Uow
from app.schemas.tenders import CreateTenderSchema, TenderOutSchema
from app.services.exceptions import (
    TenderNotFoundError,
    UserNotFoundError,
)
from settings.db import async_session


class TenderService:
    @staticmethod
    async def list_tenders(
        limit: int, offset: int, service_types: list[str]
    ) -> list[TenderOutSchema]:
        async with Uow(async_session) as uow:
            tenders = await uow.tenders.list(limit, offset, service_types)
            tenders = [TenderOutSchema.model_validate(obj) for obj in tenders]
        return tenders

    @staticmethod
    async def create_tender(tender: CreateTenderSchema) -> TenderOutSchema:
        tender_data = {
            **tender.model_dump(),
            'created_at': datetime.datetime.now(),
        }

        async with Uow(async_session) as uow:
            related_user = await uow.users.get_by_username(
                tender_data.pop('creator_username')
            )
            if not related_user:
                raise UserNotFoundError("Пользователь не найден")
            tender_obj = await uow.tenders.create(
                tender_data | {"user_id": related_user.id}
            )
            await uow.commit()

        return TenderOutSchema.model_validate(tender_obj)

    @staticmethod
    async def list_my_tenders(
        limit: int, offset: int, username: str
    ) -> list[TenderOutSchema]:
        async with Uow(async_session) as uow:
            user = await uow.users.get_by_username(username)
            if not user:
                raise UserNotFoundError("Пользователь не найден")

            tenders = await uow.tenders.list_by_user(limit, offset, user.id)
            tenders = [TenderOutSchema.model_validate(obj) for obj in tenders]

        return tenders

    @staticmethod
    async def get_by_id(
        tender_id: uuid.UUID, username: str | None
    ) -> TenderOutSchema:
        async with Uow(async_session) as uow:
            if username is None:
                tender = await uow.tenders.get_by_filters(
                    {'id': tender_id, 'status': TenderStatus.PUBLISHED.value}
                )
            else:
                user = await uow.users.get_by_username(username)
                tender = await uow.tenders.get_by_filters(
                    {'id': tender_id, 'user_id': user.id}
                )
            if not tender:
                raise TenderNotFoundError("Tender does not exist")
            return TenderOutSchema.model_validate(tender[0])

    @staticmethod
    async def update_tender(
        tender_id: uuid.UUID, filters: dict, username: str
    ) -> TenderOutSchema:
        async with Uow(async_session) as uow:
            related_user = await uow.users.get_by_username(username)
            if not related_user:
                raise UserNotFoundError("Provide user")

            tender = await uow.tenders.get_by_filters(
                {'id': tender_id, 'user_id': related_user.id}
            )
            if not tender:
                raise TenderNotFoundError("Tender does not exist")
            values = {k: v for k, v in filters.items() if v is not None}
            updated_tender = await uow.tenders.update(
                tender_id, values | {"version": tender[0].version + 1}
            )
            await uow.commit()
        return TenderOutSchema.model_validate(updated_tender)

    @staticmethod
    async def rollback(
        tender_id: uuid.UUID, version: int, username: str
    ) -> TenderOutSchema:
        async with Uow(async_session) as uow:
            related_user = await uow.users.get_by_username(username)
            if not related_user:
                raise UserNotFoundError("User not found")

            tender = await uow.tenders.get_history_by_filters(
                {
                    'tender_id': tender_id,
                    'user_id': related_user.id,
                    "version": version,
                }
            )
            if not tender:
                raise TenderNotFoundError(
                    f"Tender with version {version} does not exist"
                )

            tender_data = tender[0].__dict__
            del tender_data['_sa_instance_state']
            del tender_data['id']
            tender_id = tender_data.pop('tender_id')
            rollbacked_tender = await uow.tenders.update(
                tender_id, tender_data
            )

            await uow.commit()
            return TenderOutSchema.model_validate(rollbacked_tender)
