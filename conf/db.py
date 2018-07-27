DB_AUDITORS = "data/auditors.json"
DB_CLIENTS = "data/clients.json"
DB_VULNS = "data/vulnerabilities.json"

DB_AUDITORS_DEFAULT = {
    "full_name": "Dummy name",
    "phone": "+33 1 23 45 67 89",
    "email": "dummy.name@email.com",
    "role": "Pentester"
}

DB_CLIENTS_DEFAULT = {
    "full_name": "Dummy name",
    "phone": "+33 1 23 45 67 89",
    "email": "dummy.name@email.com",
    "role": "CISO"
}

DB_VULNS_DEFAULT = {
    "name": "Dummy name",
    "category": "",
    "sub_category": "",
    "labelNeg": "",
    "labelPos": "",
    "observ": "",
    "observHistory": ["New Observation"],
    "risk": "",
    "riskHistory": ["New Risk"],
    "reco": "",
    "recoHistory": ["New Recommandation"],
    "AV": "Network", "AC": "Low", "PR": "None",
    "UI": "Required", "S": "Unchanged",
    "C": "None", "I": "None", "A": "None"
}
