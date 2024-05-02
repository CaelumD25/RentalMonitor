from abc import ABC
import sqlite3
from API.unitInterface import UnitInterface
from Database.databaseInterface import Database

def execute_query_all_results(database_connection: sqlite3.Connection, query: str) -> list or None:
    """
    Executes a SQL query and returns all the results
    :param database_connection: The SQL connection object
    :param query: The query to be passed to the SQL DB
    :return list: Returns the retrieved results from the query, None if the query breaks
    """
    cursor = database_connection.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        database_connection.commit()
        database_connection.cursor().close()
        return result
    except sqlite3.Error as e:
        cursor.close()
        print("Error occurred with running query", e, "\n", query)
        return None

class SQL(Database, ABC):
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        print(self.connection)

    def get_new_additions(self) -> list:
        query = f"SELECT * FROM rental_record WHERE sent=0 ORDER BY ID ASC"
        return execute_query_all_results(self.connection, query)

    def mark_sent_by_id(self, id_to_update):
        query = f"UPDATE rental_record SET sent=1 WHERE ID={id_to_update}"
        execute_query_all_results(self.connection, query)
    def has_been_sent(self, id_to_check):
        query = f"SELECT sent from rental_record WHERE ID={id_to_check}"
        result = 0
        try:
            result = execute_query_all_results(self.connection, query)[0][0]
        except sqlite3.Error as e:
            print("Error occurred with running query", e, "\n", query)
        return 1==result
    def add(self, unit: UnitInterface) -> None:
        query = f"""INSERT INTO rental_record (date_time, host_website, url, title, cost, bedrooms, bathrooms, rental_size, location, description) 
                VALUES({unit.time if unit.time is not None else 0}, 
                "{unit.website if unit.time is not None else "Unknown"}", 
                "{unit.url if unit.url is not None else "Unknown"}", 
                "{unit.name if unit.name is not None else "Unknown"}", 
                {unit.cost if unit.cost is not None else -1}, 
                {unit.bedrooms if unit.bedrooms is not None else -1}, 
                {unit.bathrooms if unit.bathrooms is not None else -1}, 
                {unit.size if unit.size is not None else -1}, 
                "{unit.location if unit.location is not None else "Unknown"}", 
                "{unit.description if unit.description is not None else "Not Found"}")"""
        execute_query_all_results(self.connection, query=query)

    def unit_exists(self, unit: UnitInterface) -> bool:
        query = f"SELECT count(*) FROM rental_record rr WHERE title LIKE \"%{unit.name}%\""
        try:
            result = execute_query_all_results(self.connection, query=query)[0][0]
        except TypeError:
            return False
        return result > 0

    def close(self):
        self.connection.close()