from pymongo.database import Database


class BaseModel:
    collection: str | None = None

    def __init__(self, uuid: str | None = None, **kwargs):
        self.uuid = uuid

    @property
    def dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, dct):
        return cls(**dct)

    def save(self, database: Database):
        if not self.collection:
            raise TypeError("Model does not support saving")

        database[self.collection].replace_one(
            {"uuid": self.uuid}, self.dict, upsert=True
        )

    @classmethod
    def from_uuid(cls, database: Database, uuid: str):
        if not cls.collection:
            raise TypeError("Model does not support loading from DB")

        result = database[cls.collection].find_one({"uuid": uuid})
        if result:
            return cls.from_dict(result)
        raise KeyError("Could not locate model with UUID")
