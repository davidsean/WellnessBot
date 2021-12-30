
from typing import Any, Dict


class Challenge:

    def __repr__(self) -> str:
        return "Challenge: {}".format(self.getattrs())

    def getattrs(self) -> Dict[str, Any]:
        """
        Iteratively get all object properties and values
        :return: object attributes and values
        :rtype: Dict[str, Any]
        """
        attributes: Dict[str, Any] = {}
        for k, v in vars(self).items():
            attributes[k] = v
        return attributes

    def setattrs(self, **kwargs) -> None:
        """
        Iteratively set object properties
        """
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, uuid: str) -> None:
        self._id = uuid

    @property
    def author(self) -> str:
        return self._author

    @author.setter
    def author(self, author: str) -> None:
        self._author = author

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, description: str) -> None:
        self._description = description

    @property
    def timeout(self) -> int:
        return self._timeout

    @timeout.setter
    def timeout(self, timeout: int) -> None:
        self._timeout = timeout

    @property
    def created(self) -> str:
        return self._created

    @created.setter
    def created(self, iso_date: str) -> None:
        self._created = iso_date
