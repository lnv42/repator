import os.path

from dbhandler import DBHandler


class AuditorHandler:
	"""
		Auditor has:
			full_name, phone, email.
	"""
	
	def __init__(self):
		db_path = 'data/auditors.json'
		if not os.path.isfile(db_path):
			self.db = DBHandler(db_path)
			self.db.insert_record({"full_name" : "Dummy name", "phone" : "06 66 66 66 66", "email" : "dummy.name@email.com"})
		self.db = DBHandler(db_path)
	
	def get_auditors(self):
		return self.db.get_all()[1:]

	def search_auditor_by_name(self, name):
		return self.db.search("full_name", name)

	def search_auditor_by_phone(self, phone):
		return self.db.search("phone", phone)

	def search_auditor_by_email(self, email):
		return self.db.search("email", email)

	def search_auditor_by_id(self, auditor_id):
		return self.db.search_by_id(auditory_id)
		
	def add_auditor(self, auditor):
		return self.db.insert_record(auditor)

	def add_property(self, property_name, default_value):
		return self.db.insert_column(property_name, default_value)

	def update_auditor(self, auditor):
		return self.db.update(auditor)


class VulnHandler:
	"""
		A vulnerability has:
			name, observ, category, sub_category, risk, AV, AC, PR, UI, S, C, I, A
	"""
	
	def __init__(self):
		db_path = 'data/vulnerabilities.json'
		if not os.path.isfile(db_path):
			self.db = DBHandler(db_path)
			self.db.insert_record({"name" : "Dummy name", "category" : "cat", "sub_category" : "sub_cat",  "observ" : "long long obs", "risk" : "risk desc", "AV": "av", "AC": "ac", "PR": "pr", "UI": "ui", "S": "s", "C": "c", "I": "i", "A": "a" })
		self.db = DBHandler(db_path)
	
	def get_vulns(self):
		return self.db.get_all()[1:]

	def search_vuln_by_name(self, name):
		return self.db.search("name", name)
	
	def search_vuln_by_id(self, vuln_id):
		return self.db.search_by_id(vuln_id)

	def add_vuln(self, vuln):
		return self.db.insert_record(vuln)

	def add_property(self, property_name, default_value):
		return self.db.insert_column(property_name, default_value)

	def update_vuln(self, vuln):
		return self.db.update(vuln)

VulnHandler()
AuditorHandler()
