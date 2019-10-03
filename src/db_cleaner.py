from collections import OrderedDict
from conf.report import LANGUAGES
from conf.db import DB_AUDITORS_DEFAULT,DB_CLIENTS_DEFAULT,DB_VULNS_DEFAULT
from src.dbhandler import DBHandler

def strip_field(field):
    try: # string
        return field.replace("[[/]]","").strip()
    except:
        try: # iterable
            for cpt in range(0, len(field)):
                field[cpt] = field[cpt].replace("[[/]]","").strip()
        except:
            pass
        return field

def clean_db(db, default, languages=[]):
    data = db.get_all()
    db.purge()

    if len(languages) > 1: # remove default lang from list
        languages = languages[1:]
    else:
        languages = []

    for row in data:
        new_row = OrderedDict()
        for field in default:
            if field in row: # field exist
                new_row[field] = strip_field(row[field])
                if field == "observNeg" or field == "observNegHistory":
                    # take old observ value as observNeg default
                    if field.replace("Neg", "") in row:
                        new_row[field] = strip_field(row[field.replace("Neg", "")])
                    for lang in languages: # multi lang
                        if field.replace("Neg", "")+lang in row:
                            new_row[field+lang] = strip_field(row[field.replace("Neg", "")+lang])

            if field not in new_row:
                new_row[field] = default[field] # set field to default value

            for lang in languages: # multi lang
                if field+lang in row:
                    new_row[field+lang] = strip_field(row[field+lang])

        db.insert_record(new_row)

def main(args):
    """Main process."""
    clean_db(DBHandler.auditors(), DB_AUDITORS_DEFAULT)
    clean_db(DBHandler.clients(), DB_CLIENTS_DEFAULT)
    clean_db(DBHandler.vulns(), DB_VULNS_DEFAULT, LANGUAGES)
