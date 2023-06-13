from os import getenv

from certifi import where
from dotenv import load_dotenv
from MonsterLab import Monster
from pandas import DataFrame
from pymongo import MongoClient

import random

class Database:
    """
    A class representing a database for storing Monster data.
    """

    load_dotenv()
    database = MongoClient(getenv("MONGO_DB"), tls=True, tlsCAFile=where())["Database"]

    def __init__(self, collection: str = "Monsters"):
        """
        Initialize a Database instance.

        Parameters:
        - collection (str): The name of the collection to use in the database. Defaults to "Monsters".
        """
        self.collection = self.database[collection]
        self.seed()

    def seed(self, amount: int = random.randint(1000, 2000)):
        """
        Seed the database with randomly generated Monster data.

        Parameters:
        - amount (int): The number of Monsters to generate and insert into the database.
            - Defaults to a random number between 1000 and 2000, inclusive.
        """
        if self.count() > 0:
            self.reset()
            self.seed()
        else:
            monsters = [Monster().to_dict() for _ in range(amount)]
            self.collection.insert_many(monsters)

    def reset(self):
        """
        Reset the database by dropping the collection.
        """
        self.collection.drop()

    def count(self) -> int:
        """
        Get the number of documents in the collection.

        Returns:
        - int: The number of documents in the collection.
        """
        return self.collection.count_documents({})

    def dataframe(self) -> DataFrame:
        """
        Retrieve the data from the collection as a pandas DataFrame.

        Returns:
        - DataFrame: A pandas DataFrame containing the data from the collection.
        """
        return DataFrame(self.collection.find())

    def html_table(self) -> str:
        """
        Generate an HTML table representation of the data in the collection.

        Returns:
        - str: An HTML string representing the data in the collection as a table.
        """
        return self.dataframe().to_html() if self.count() > 0 else None
