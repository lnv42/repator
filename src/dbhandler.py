from tinydb import TinyDB, Query
from os import path,mkdir

from conf.db import *

class DBHandler:

    def Auditors():
        return DBHandler(DB_AUDITORS, DB_AUDITORS_DEFAULT)

    def Clients():
        return DBHandler(DB_CLIENTS, DB_CLIENTS_DEFAULT)

    def Vulns():
        return DBHandler(DB_VULNS, DB_VULNS_DEFAULT)

    def __init__(self, db_path, defaultValues={}):
        if not path.exists(path.dirname(db_path)):
            mkdir(path.dirname(db_path), 0o750)

        newDb = not path.isfile(db_path)

        self.path = db_path
        self.db = TinyDB(db_path)

        if newDb:
            self.insert_record(defaultValues)
        else:
            for name, value in defaultValues.items():
                self.insert_column(name, value)

    def insert_column(self, name, value):
        l = self.get_all()
        cols = {name: value}
        ids = []
        for r in l:
            if name in r:
                return False # column already exist
            ids.append(r.doc_id)
        self.db.update(cols, doc_ids=ids)
        return True

    def insert_record(self, d=None):
        if d == None:
            d = dict(self.search_by_id(1))
            for k in d:
                d[k] = ""
        return self.db.insert(d)

    def get_all(self):
        return self.db.all()[1:]

    def search(self, name, value):
        q = Query()
        return self.db.search(q[name] == value)

    def search_by_id(self, id_):
        return self.db.get(doc_id=id_)

    def update(self, id_, name, value):
        record = self.search_by_id(id_)
        if record is None:
            return False
        record[name] = value
        return self.db.update(record, doc_ids=[id_])

    def delete(self, id_):
        return self.db.remove(doc_ids = [id_])

"""    
# Testing
db = DBHandler('/tmp/db.json')
db.insert_record({"Name": "SQLi", "Desc": "Inject SQL stuff", "Metrics": {"Exploitability": {"AV": "N", "AC": "M", "AU": "M"}, "Impact": {"C": "C", "I": "C", "A": "C"}}})
db.insert_record({"Name": "XSS", "Desc": "Inject JS stuff", "Metrics": {"Exploitability": {"AV": "N", "AC": "L", "AU": "M"}, "Impact": {"C": "C", "I": "C", "A": "N"}}})
db.insert_record({"Name": "CSRF", "Desc": "Make user do stuff", "Metrics": {"Exploitability": {"AV": "N", "AC": "H", "AU": "M"}, "Impact": {"C": "N", "I": "C", "A": "N"}}})
print(type(db.get_all()[0].doc_id))
db.insert_column("Score", 5.5)
print(db.search("Name", "XSS"))
"""
