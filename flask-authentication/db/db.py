import os, sys, json
from typing import Any

DB_LOCATION = "C:/Github/Python-Study/flask-authentication/db/jsons"

class DB:
    def __init__(self, dbName: str) -> None:
        self.db = dbName
        
    def __contains__(self, item: Any) -> bool:
        return item in self.getDB()
            
    def getDB(self) -> Any:
        with open(f'{DB_LOCATION}/{self.db}.json') as f:
            return json.load(f)
    
    def saveDB(self, json_object: Any) -> None:
        with open(f'{DB_LOCATION}/{self.db}.json', 'w') as f:
            json.dump(json_object, f, indent=2)
        
    def insert(self, key: str, value: Any) -> None:
        DB = self.getDB()
        DB[key] = value
        self.saveDB(DB)
    
    def select(self, key: str) -> dict | list:
        try:
            return self.getDB()[key]
        except KeyError:
            return None
    
    def where(self, key: str, value: Any) -> int:
        try:
            return list(map(lambda x: x[key] == value, self.getDB())).index(True)
        except ValueError:
            return -1
