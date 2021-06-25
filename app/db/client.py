from app.db.models.challenge import Challenge
import os
import logging
from pymongo import MongoClient
from typing import Optional, TypeVar, Union
from app.exceptions.db import DbNotInitialized, ModelSchemaError, NullQueryResult

Model = Union[Challenge]
_T = TypeVar('_T', bound=Model)


class Client:

    # mongo container initialization
    MONGO_USER = os.getenv('MONGO_USER')
    MONGO_PASS = os.getenv('MONGO_PASS')
    MONGO_PORT = os.getenv('MONGO_PORT')
    MONGO_HOST = os.getenv('MONGO_HOST')
    MONGO_URI = 'mongodb://{}:{}/'.format(MONGO_HOST, MONGO_PORT)
    client: Optional[MongoClient] = None
    _log = logging.getLogger(__name__)

    @classmethod
    def init_db(cls) -> None:
        # create client instance
        cls.client = MongoClient(cls.MONGO_URI, username=cls.MONGO_USER,
                                 password=cls.MONGO_PASS)
        cls._log.info("Created mongo client as user %s @ %s", cls.MONGO_USER, cls.MONGO_URI)

    @classmethod
    def post(cls, model: Model) -> str:
        """
        Post a model of a specific schema to a target collection

        :param model: model schema to post
        :type model: Model
        :raises DbNotInitialized: if database client is not created
        :raises ModelSchemaError: if the schema is unsupported
        :return: uuid of posted element
        :rtype: str
        """
        if cls.client is None:
            raise DbNotInitialized
        db = cls.client.master
        collection = None
        if type(model) is Challenge:
            collection = db.challenges
        if collection is None:
            raise ModelSchemaError
        result = collection.insert_one(model.__dict__)
        cls._log.info("Db insert successful with result id: %s", result.inserted_id)
        _id = str(result.inserted_id)
        return _id

    @classmethod
    def get(cls, model: _T) -> _T:
        if cls.client is None:
            raise DbNotInitialized
        db = cls.client.master
        collection = None
        if isinstance(model, Challenge):
            collection = db.challenges
        if collection is None:
            raise ModelSchemaError
        result = collection.find_one()
        cls._log.info("Db query successful with result: %s", result)
        if result is None:
            raise NullQueryResult
        model.setattrs(**result)
        return model
