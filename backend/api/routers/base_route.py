import os

from fastapi import HTTPException


class BaseRoute:
    @staticmethod
    def get_all(session, model):
        return session.query(model).all()

    @staticmethod
    def add_new(session, model, **kwargs):
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance

    @staticmethod
    def get_items(session, model, id):
        instance = session.query(model).filter(model.id == id).first()
        instance_path = instance.path
        items = os.listdir(instance_path)
        results = [item for item in items if os.path.isfile(os.path.join(instance_path, item))]
        return results

    @staticmethod
    def get_by_id(session, model, id):
        return session.query(model).filter(model.id == id).first()

    @staticmethod
    def update(session, model, id, **kwargs):
        instance = session.query(model).filter(model.id == id).first()
        for key, value in kwargs.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        session.add(instance)
        session.commit()

    @staticmethod
    def delete(session, model, id):
        to_delete = session.query(model).filter(model.id == id).first()
        if to_delete is None:
            raise HTTPException(status_code=404, detail=f"{model} not found")
        session.delete(to_delete)
        session.commit()
