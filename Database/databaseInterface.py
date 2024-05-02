from abc import ABC, abstractmethod
from API.unitInterface import UnitInterface
class Database(ABC):

    @abstractmethod
    def get_new_additions(self) -> list:
        """
        Return the units that are new to the database
        :returns list: List of new additions, i.e. ones not yet sent/ with sent being 0
        """
        pass

    @abstractmethod
    def add(self, unit: UnitInterface) -> None:
        """
        Adds a rental unit to the database
        :returns None: Returns Nothing
        """
        pass

    @abstractmethod
    def unit_exists(self, unit: UnitInterface) -> bool:
        """
        Asserts that a unit object exists in the database
        :returns bool: Returns True if title found in DB, else False
        """
        pass

    @abstractmethod
    def mark_sent_by_id(self, id_to_update: int) -> None:
        """
        Marks a rental, by ID, that the rental has been sent to the telegram bot
        :param id_to_update: The ID of the rental that has been sent
        :return:
        """
        pass

    @abstractmethod
    def has_been_sent(self, id_to_check: int) -> bool:
        """
        Checks if a rental has been sent given an ID
        :param id_to_check:  The ID of the rental that needs to be checked
        :return bool: Returns True if the rental has been sent, otherwise false
        """
        pass

    def close(self):
        """
        Properly close the SQL connection
        :return: None
        """