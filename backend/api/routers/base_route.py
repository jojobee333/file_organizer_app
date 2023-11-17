import os

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRoute:

    @staticmethod
    async def is_session_running(session: AsyncSession):
        if not session.in_transaction():
            return False
        else:
            return True

    @staticmethod
    async def get_all(session, model):
        result = await session.execute(select(model))
        return result.scalars().all()

    @staticmethod
    async def add_new(session, model, **kwargs):
        # OK
        session_running = await BaseRoute.is_session_running(session)
        if not session_running:
            async with session.begin():
                instance = model(**kwargs)
                session.add(instance)
        await session.refresh(instance)
        return instance

    @staticmethod
    async def get_items(session, model, id):
        # OK
        query = select(model).where(model.id == id)
        result = await session.execute(query)
        instance = result.scalars().first()
        if instance:
            instance_path = instance.path
            items = os.listdir(instance_path)
            results = [item for item in items if os.path.isfile(os.path.join(instance_path, item))]
            return results
        else:
            return []

    @staticmethod
    async def get_by_id(session, model, id):
        # OK
        query = select(model).where(model.id == id)
        result = await session.execute(query)
        return result.scalars().first()

    @staticmethod
    async def get_by_name(session, model, name: str):
        query = select(model).where(model.name == name)
        result = await session.execute(query)
        return result.scalars().first()

    @staticmethod
    async def update(session, model, id, **kwargs):
        # OK
        query = select(model).where(model.id == id)
        result = await session.execute(query)
        instance = result.scalars().first()
        if instance is not None:
            for key, value in kwargs.items():
                if hasattr(instance, key):
                    setattr(instance, key, value)
            if not session.in_transaction():
                async with session.begin():
                    session.add(instance)
            else:
                session.add(instance)

            return instance
        else:
            raise NoResultFound(f"Instance of {model.__name__} with ID {id} not found.")

    @staticmethod
    async def delete(session, model, id):
        # OK
        query = select(model).where(model.id == id)
        result = await session.execute(query)
        instance = result.scalars().first()
        if instance is None:
            raise HTTPException(status_code=404, detail=f"{model} not found")
        await session.delete(instance)
        await session.commit()
