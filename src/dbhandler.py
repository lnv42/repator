"""Interface between repator and TinyDB."""

# coding=utf-8

from os import path, mkdir
import collections

from tinydb import TinyDB, Query

from conf.db import (DB_AUDITORS, DB_AUDITORS_DEFAULT, DB_CLIENTS,
                     DB_CLIENTS_DEFAULT, DB_VULNS, DB_VULNS_DEFAULT,
                     DB_VULNS_GIT, DB_VULNS_INITIAL)


class DBHandler:
    """Class that make the link between the DB and repator."""
    @staticmethod
    def auditors():
        """Default constructor for Auditors database."""
        return DBHandler(DB_AUDITORS, DB_AUDITORS_DEFAULT)

    @staticmethod
    def clients():
        """Default constructor for Clients database."""
        return DBHandler(DB_CLIENTS, DB_CLIENTS_DEFAULT)

    @staticmethod
    def vulns():
        """Default constructor for Vulns database."""
        return DBHandler(DB_VULNS, DB_VULNS_DEFAULT)

    @staticmethod
    def vulns_git():
        """Default constructor for Vulns taken from git database."""
        return DBHandler(DB_VULNS_GIT, DB_VULNS_DEFAULT)

    @staticmethod
    def vulns_initial():
        """Default constructor for vulns database when repator has been launched."""
        return DBHandler(DB_VULNS_INITIAL, DB_VULNS_DEFAULT)

    def __init__(self, db_path, default_values=None):
        if not path.exists(path.dirname(db_path)):
            mkdir(path.dirname(db_path), 0o750)

        new_db = not path.isfile(db_path)

        self.path = db_path
        self.default_values = default_values if default_values else {}
        self.database = TinyDB(db_path, indent=2,
                               object_pairs_hook=collections.OrderedDict)

        if new_db:
            self.insert_record(default_values)
        else:
            for name, value in default_values.items():
                self.insert_column(name, value)

    def insert_column(self, name, value):
        """Creates a new column in the database."""
        values = self.get_all()
        cols = {name: value}
        ids = []
        for record in values:
            if name in record:
                return False  # column already exists
            ids.append(record.doc_id)
        self.database.update(cols, doc_ids=ids)
        return True

    def insert_record(self, dictionary=None):
        """Adds a new empty record to the database."""
        if dictionary is None:
            dictionary = collections.OrderedDict(self.search_by_id(1))
            for k in dictionary:
                dictionary[k] = ""
        return self.database.insert(dictionary)

    def insert_multiple(self, dictionary):
        """Insertion of multiple entries."""
        return self.database.insert_multiple(dictionary)

    def get_all(self):
        """Gets all records but the first one which is a sample record."""
        return self.database.all()[1:]

    def search(self, name, value):
        """Implements the search method of TinyDB."""
        query = Query()
        return self.database.search(query[name] == value)

    def search_by_id(self, id_):
        """Searches for a document with the id id_ in the database."""
        return self.database.get(doc_id=id_)

    def update(self, id_, name, value):
        """Modifies the corresponding record in the database."""
        record = self.search_by_id(id_)
        if record is None:
            return False
        record[name] = value
        return self.database.update(record, doc_ids=[id_])

    def delete(self, id_):
        """Removes the corresponding record from the database."""
        return self.database.remove(doc_ids=[id_])

    def purge(self):
        """Purges the database and adds the default values to the newly created database."""
        self.database.purge()
        self.insert_record(self.default_values)

    def close(self):
        """Implements the close method of TinyDB."""
        self.database.close()
