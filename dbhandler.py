from tinydb import TinyDB, Query
from os import path


DB_AUDITORS = "data/auditors.json"
DB_CLIENTS = "data/clients.json"
DB_VULNS = "data/vulnerabilities.json"

DB_AUDITORS_DEFAULT = {
    "full_name" : "Dummy name",
    "phone" : "+33 1 23 45 67 89",
    "email" : "dummy.name@email.com",
    "role" : "Pentester"
}

DB_CLIENTS_DEFAULT = {
    "full_name" : "Dummy name",
    "phone" : "+33 1 23 45 67 89",
    "email" : "dummy.name@email.com",
    "role" : "CISO"
}

DB_VULNS_DEFAULT = {
    "name" : "Dummy name",
    "category" : "",
    "sub_category" : "",
    "observ" : "",
    "observHistory": ["New Observation"],
    "risk" : "",
    "riskHistory": ["New Risk"],
    "AV": "Network", "AC": "Low", "PR": "None",
    "UI": "Required", "S": "Unchanged",
    "C": "None", "I": "None", "A": "None"
}

class DBHandler:

    def Auditors():
        return DBHandler(DB_AUDITORS, DB_AUDITORS_DEFAULT)

    def Clients():
        return DBHandler(DB_CLIENTS, DB_CLIENTS_DEFAULT)

    def Vulns():
        return DBHandler(DB_VULNS, DB_VULNS_DEFAULT)

    def __init__(self, db_path, defaultValues={}):
        newDb = not path.isfile(db_path)

        self.path = db_path
        self.db = TinyDB(db_path)

        if newDb:
            self.db.insert_record(defaultValues)
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

    def insert_record(self, d):
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
