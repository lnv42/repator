from tinydb import TinyDB, Query


class DBHandler:
	
	def __init__(self, db_path):
		self.path = db_path
		self.db = TinyDB(db_path)
	
	def insert_column(self, name, value):
		l = self.get_all()
		cols = {name: value}
		ids = []
		for r in l:
			ids.append(r.doc_id)
		self.db.update(cols, doc_ids=ids)
		return True

	def insert_record(self, d):
		return self.db.insert(d)

	def get_all(self):
		return self.db.all()

	def search(self, name, value):
		q = Query()
		return self.db.search(q[name] == value)

	def search_by_id(self, id_):
		return self.db.get(doc_id=id_)

	def update(self, rec):
		return self.db.update(dict(rec), doc_ids=[rec.doc_id])

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
