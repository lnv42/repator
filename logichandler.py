


class AuditorHandler:
	"""
		Auditor has:
			full_name, phone, email.
	"""
	
	def __init__(self):
		self.db = DBHandler('data/auditors.json')
	
	def get_auditors(self):
		return self.db.get_all()

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



