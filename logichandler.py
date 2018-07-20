import os.path

from dbhandler import DBHandler


class AuditorHandler:
    """
        Auditor has:
            full_name, phone, email, role.
    """
    
    def __init__(self):
        db_path = 'data/auditors.json'

        defaultValues = {
            "full_name" : "Dummy name",
            "phone" : "+33 1 23 45 67 89",
            "email" : "dummy.name@email.com",
            "role" : "Pentester"
        }

        if not os.path.isfile(db_path):
            self.db = DBHandler(db_path)
            self.db.insert_record(defaultValues)
        else:
            self.db = DBHandler(db_path)
            for name, value in defaultValues.items():
                self.add_property(name, value)
    
    def get_auditors(self):
        return self.db.get_all()[1:]

    def search_auditor_by_name(self, name):
        return self.db.search("full_name", name)

    def search_auditor_by_phone(self, phone):
        return self.db.search("phone", phone)

    def search_auditor_by_email(self, email):
        return self.db.search("email", email)

    def search_auditor_by_id(self, auditor_id):
        return self.db.search_by_id(auditor_id)
        
    def add_auditor(self, auditor=None):
        return self.db.insert_record(auditor)

    def add_property(self, property_name, default_value):
        return self.db.insert_column(property_name, default_value)

    def update_auditor(self, auditor_id, property_name, new_value):
        auditor = self.search_auditor_by_id(auditor_id)
        auditor[property_name] = new_value
        return self.db.update(auditor)

    def del_auditor(self, auditor_id):
        return self.db.delete(auditor_id)


class VulnHandler:
    """
        A vulnerability has:
            name, observ, category, sub_category, risk, AV, AC, PR, UI, S, C, I, A
    """
    
    def __init__(self):
        db_path = 'data/vulnerabilities.json'

        defaultValues = {
            "name" : "Dummy name",
            "category" : "",
            "sub_category" : "",
            "observ" : "",
            "risk" : "",
            "AV": "Network", "AC": "Low", "PR": "None",
            "UI": "Required", "S": "Unchanged",
            "C": "None", "I": "None", "A": "None"
        }

        if not os.path.isfile(db_path):
            self.db = DBHandler(db_path)
            self.db.insert_record(defaultValues)
        else:
            self.db = DBHandler(db_path)
            for name, value in defaultValues.items():
                self.add_property(name, value)
    
    def get_vulns(self):
        return self.db.get_all()[1:]

    def search_vuln_by_name(self, name):
        return self.db.search("name", name)
    
    def search_vuln_by_id(self, vuln_id):
        return self.db.search_by_id(vuln_id)

    def add_vuln(self, vuln=None):
        return self.db.insert_record(vuln)

    def add_property(self, property_name, default_value):
        return self.db.insert_column(property_name, default_value)

    def update_vuln(self, vuln_id, property_name, new_value):
        vuln = self.search_vuln_by_id(vuln_id)
        vuln[property_name] = new_value
        return self.db.update(vuln)
    
    def del_vuln(self, vuln_id):
        return self.db.delete(vuln_id)


