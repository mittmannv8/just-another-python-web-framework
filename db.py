"""
This module is just a helper to emulate a in-memory database.
It's useful for learning purposes
"""
from uuid import uuid4


class DB:
    database = {
        'users': {
            1: {'name': 'Klaus', 'age': 33, 'id': 1},
            2: {'name': 'Diego', 'age': 30, 'id': 2},
        }
    }

    def get(self, table, id=None):
        table = self.database.get(table, [])
        return table.get(id) if id else table

    def insert(self, table_name, values):
        id = values.get('id')
        table = self.database.get(table_name, {})
        if not table:
            self.database[table_name] = table

        if id and id in table.keys():
            raise ValueError('Duplicated ID')
        elif not id:
            id = str(uuid4())
            values['id'] = id

        self.database[table_name].update({id: values})
        return values


db = DB()
