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
                try: # string
                    new_row[field] = new_row[field].replace("[[/]]","").strip()
                except:
                    try: # iterable
                        for cpt in range(0, len(new_row[field])):
                            new_row[field][cpt] = new_row[field][cpt].replace("[[/]]","").strip()
                    except:
                        pass
            else:
                new_row[field] = ""
            for lang in languages:
                if field+lang in row:
                    new_row[field+lang] = row[field+lang]
                    try: # string
                        new_row[field+lang] = new_row[field+lang].replace("[[/]]","").strip()
                    except:
                        try: # iterable
                            for cpt in range(0, len(new_row[field+lang])):
                                new_row[field+lang][cpt] = new_row[field+lang][cpt].replace("[[/]]","").strip()
                        except:
                            pass
                    if len(new_row[field]) < 1:
                        new_row[field] = new_row[field+lang]
        db.insert_record(new_row)

def main(args):
    """Main process."""
    clean_db(DBHandler.auditors(), DB_AUDITORS_DEFAULT)
    clean_db(DBHandler.clients(), DB_CLIENTS_DEFAULT)
    clean_db(DBHandler.vulns(), DB_VULNS_DEFAULT, LANGUAGES)
