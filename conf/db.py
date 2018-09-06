import collections

DB_AUDITORS = "db/auditors.json"
DB_CLIENTS = "db/clients.json"
DB_VULNS = "db/vulnerabilities.json"

DB_AUDITORS_DEFAULT = collections.OrderedDict()
DB_AUDITORS_DEFAULT["full_name"] = "Dummy name"
DB_AUDITORS_DEFAULT["phone"] = "+33 1 23 45 67 89"
DB_AUDITORS_DEFAULT["email"] = "dummy.name@email.com"
DB_AUDITORS_DEFAULT["role"] = "Pentester"

DB_CLIENTS_DEFAULT = collections.OrderedDict()
DB_CLIENTS_DEFAULT["full_name"] = "Dummy name"
DB_CLIENTS_DEFAULT["phone"] = "+33 1 23 45 67 89"
DB_CLIENTS_DEFAULT["email"] = "dummy.name@email.com"
DB_CLIENTS_DEFAULT["role"] = "CISO"

DB_VULNS_DEFAULT = collections.OrderedDict()
DB_VULNS_DEFAULT["category"] = ""
DB_VULNS_DEFAULT["sub_category"] = ""
DB_VULNS_DEFAULT["name"] = "Dummy name"
DB_VULNS_DEFAULT["labelNeg"] = ""
DB_VULNS_DEFAULT["labelPos"] = ""
DB_VULNS_DEFAULT["observ"] = ""
DB_VULNS_DEFAULT["observHistory"] = ["New Observation"]
DB_VULNS_DEFAULT["risk"] = ""
DB_VULNS_DEFAULT["riskHistory"] = ["New Risk"]
DB_VULNS_DEFAULT["reco"] = ""
DB_VULNS_DEFAULT["recoHistory"] = ["New Recommandation"]
DB_VULNS_DEFAULT["AV"] = "Network"
DB_VULNS_DEFAULT["AC"] = "Low"
DB_VULNS_DEFAULT["PR"] = "None"
DB_VULNS_DEFAULT["UI"] = "Required"
DB_VULNS_DEFAULT["S"] = "Unchanged"
DB_VULNS_DEFAULT["C"] = "None"
DB_VULNS_DEFAULT["I"] = "None"
DB_VULNS_DEFAULT["A"] = "None"
