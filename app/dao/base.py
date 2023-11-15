
from app.database import async_session_maker
from sqlalchemy import insert, select

class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls,model_id : int):
        async with async_session_maker() as session:
            quary = select(cls.model).filter_by(id=model_id)
            result = await session.execute(quary)
            return result.mappings().one_or_none()

    @classmethod
    async def find_one_or_none(cls,**filters):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filters)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def find_all(cls, **filters):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filters)
            result = await session.execute(query)
            return result.mappings().all()
        
    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data).returning(cls.model.id)
            await session.execute(query)
            await session.commit() # фиксируем результаты


    
