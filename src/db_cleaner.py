from collections import OrderedDict
from conf.report import LANGUAGES
from conf.db import DB_AUDITORS_DEFAULT,DB_CLIENTS_DEFAULT,DB_VULNS_DEFAULT
from src.dbhandler import DBHandler


def clean_db(db, default, languages=[]):
    data = db.get_all()
    db.purge()
    for row in data:
        new_row = OrderedDict()
        for field in default:
            if field in row:
                new_row[field] = row[field]
            else:
                new_row[field] = ""
            for lang in languages:
                if field+lang in row:
                    new_row[field+lang] = row[field+lang]
        db.insert_record(new_row)

def main(args):
    """Main process."""
    clean_db(DBHandler.auditors(), DB_AUDITORS_DEFAULT)
    clean_db(DBHandler.clients(), DB_CLIENTS_DEFAULT)
    clean_db(DBHandler.vulns(), DB_VULNS_DEFAULT, LANGUAGES)
