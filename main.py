import sqlite3
import sqlite_vec 
from typing import Dict, List, Any
import struct


def serialize(vector: List[float]) -> bytes:
    """serializes a list of floats into a compact "raw bytes" format"""
    return struct.pack("%sf" % len(vector), *vector)

def crappy_embedding(text: str) -> List[float]:
    words = text.split()
    word_to_index = {word: idx for idx, word in enumerate(set(words))}
    max_index = len(word_to_index) - 1
    embedding = [word_to_index[word] / max_index for word in words]

    return embedding

class SqliteUtil:

    def __init__(self, db_name: str) -> None:
        self.db_name: str = db_name 
        self._set_db()

    def _set_db(self) -> None:
        self.db = sqlite3.connect(f"db/{self.db_name}.db")
        self.db.enable_load_extension(True)
        sqlite_vec.load(self.db) 
        self.db.enable_load_extension(False)

    def _set_params(self, query: str, params: Dict [str,str] |None = None) -> str:
        
        return query.format(**params) if params else query

    def execute_qry(self, query: str, params: Dict [str,str] |None = None) -> None:

        sql = self._set_params(query, params) 
        with self.db as db:
            db.execute(sql)

    def insert_many(self, query: str, values: List[Any]) -> None:

        with self.db as db:
            db.execute(query, values)


    def query_to_list(self, query: str, params: Dict [str,str] | None = None) -> Any:

        sql = self._set_params(query, params)
        with self.db as db:
            results = db.execute(sql).fetchall()

            return results


def main():
    db_name: str = "test"

    sqlite_util:SqliteUtil = SqliteUtil(db_name=db_name)

    ddl = "create virtual table if not exists test using vec0 (id integer primary key, embedding float[5]);"

    sqlite_util.execute_qry(ddl)

    ins = "insert into test (embedding) values(?)"
    embedding_text = "wow what a neat sentence"
    sqlite_util.insert_many(ins, [serialize(crappy_embedding(embedding_text))])

    for row in sqlite_util.query_to_list("select * from test"):
        print(row)


if __name__ == "__main__":
    main()
