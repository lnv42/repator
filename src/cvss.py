"""Module computing the CVSS scores and risk levels of a vulnerability."""

# coding=utf-8


def vuln_cvssv3(values):
    """Returns the CVSSv3 score from an array."""
    return cvssv3(values["AV"], values["AC"], values["PR"], values["UI"],
                  values["S"], values["C"], values["I"], values["A"])


# attack_vector, attack_complexity, privileges_required, user_interaction,
# scope, confidentiality, integrity, availability


def cvssv3(attack_vector, attack_complexity, privileges_required,
           user_interaction, scope, confidentiality, integrity, availability):
    """Function that returns the CVSSv3 score of the vulnerability which attributes are given."""
    av_coeff = {"N": 0.85, "A": 0.62, "L": 0.55, "P": 0.2}
    ac_coeff = {"L": 0.77, "H": 0.44}
    if scope == "C":
        pr_coeff = {"N": 0.85, "L": 0.68, "H": 0.5}
    else:
        pr_coeff = {"N": 0.85, "L": 0.62, "H": 0.27}
    ui_coeff = {"N": 0.85, "R": 0.62}
    cia_coeff = {"N": 0, "L": 0.22, "H": 0.56}
    attack_vector = av_coeff[attack_vector[0]]
    attack_complexity = ac_coeff[attack_complexity[0]]
    privileges_required = pr_coeff[privileges_required[0]]
    user_interaction = ui_coeff[user_interaction[0]]
    confidentiality = cia_coeff[confidentiality[0]]
    integrity = cia_coeff[integrity[0]]
    availability = cia_coeff[availability[0]]
    exp = 8.22 * attack_vector * attack_complexity * \
        privileges_required * user_interaction
    imp = 1 - ((1 - confidentiality) * (1 - integrity) * (1 - availability))
    if scope == "Changed":
        imp = 7.52 * (imp - 0.029) - 3.25 * (imp - 0.02) ** 15
        score = 1.08 * (imp + exp)
    else:
        imp = 6.42 * imp
        score = imp + exp
    if imp <= 0:
        score = 0.0
    if score > 10:
        score = 10.0
    return round(score, 1), round(imp, 1), round(exp, 1)


def vuln_risk_level(values, lang="EN"):
    """Returns the risk level from an array."""
    return risk_level(values["AV"], values["AC"], values["PR"], values["UI"],
                      values["S"], values["C"], values["I"], values["A"], lang)


def risk_level(attack_vector, attack_complexity, privileges_required,
               user_interaction, scope, confidentiality, integrity,
               availability, lang="EN"):
    """Function that returns the risk level of the vulnerability which attributes are given."""
    cia_coeff = {"N": 0, "L": 1, "H": 2}
    s_coeff = {"U": False, "C": True}
    confidentiality = cia_coeff[confidentiality[0]]
    integrity = cia_coeff[integrity[0]]
    availability = cia_coeff[availability[0]]
    scope = s_coeff[scope[0]]

    if confidentiality == 2 or integrity == 2 or (
            confidentiality * 2 + integrity * 2 + availability >= 5 and scope):
        impact_lvl = 4
    elif availability == 2 or (
            confidentiality * 2 + integrity * 2 + availability >= 5) or (
                confidentiality * 2 + integrity * 2 + availability >= 3 and scope):
        impact_lvl = 3
    elif confidentiality * 2 + integrity * 2 + availability >= 3 or scope:
        impact_lvl = 2
    else:
        impact_lvl = 1

    av_coeff = {"N": 1, "A": 2, "L": 3, "P": 4}
    ac_coeff = {"L": 1, "H": 2}
    pr_coeff = {"N": 0, "L": 1, "H": 2}
    ui_coeff = {"N": False, "R": True}
    attack_vector = av_coeff[attack_vector[0]]
    attack_complexity = ac_coeff[attack_complexity[0]]
    privileges_required = pr_coeff[privileges_required[0]]
    user_interaction = ui_coeff[user_interaction[0]]

    if attack_vector == 4 or privileges_required == 2 or (
            attack_vector == 3 and privileges_required == 1 and user_interaction) or (
                attack_complexity == 2 and (
                    attack_vector == 3 or privileges_required == 1 or user_interaction)):
        exploitability_lvl = 1
    elif attack_complexity == 2 or attack_vector == 3 or (
            attack_vector == 2 and (privileges_required == 1 or user_interaction)) or (
                privileges_required == 1 and user_interaction):
        exploitability_lvl = 2
    elif attack_vector == 2 or privileges_required == 1 or user_interaction:
        exploitability_lvl = 3
    else:
        exploitability_lvl = 4

    if (impact_lvl == 1 and exploitability_lvl <= 2) or (
            exploitability_lvl == 1 and impact_lvl <= 2):
        risk_lvl = 1
    elif (impact_lvl <= 3 and exploitability_lvl <= 2) or impact_lvl == 1:
        risk_lvl = 2
    elif (impact_lvl <= 4 and exploitability_lvl <= 2) or (
            impact_lvl <= 3 and exploitability_lvl <= 3) or impact_lvl == 2:
        risk_lvl = 3
    else:
        risk_lvl = 4

    if lang == "FR":
        risk_lvl_values = {1: "Faible", 2: "Modéré", 3: "Élevé", 4: "Très élevé"}
        impact_lvl_values = {1: "Faible", 2: "Moyen", 3: "Fort", 4: "Très fort"}
        exploitability_lvl_values = {1: "Très difficile", 2: "Difficile",
                                     3: "Moyenne", 4: "Facile"}
    else:
        risk_lvl_values = {1: "Low", 2: "Medium", 3: "High", 4: "Very High"}
        impact_lvl_values = {1: "Low", 2: "Medium", 3: "High", 4: "Very High"}
        exploitability_lvl_values = {1: "Dificult", 2: "Medium", 3: "Easy",
                                     4: "Very Easy"}

    return (risk_lvl_values[risk_lvl], impact_lvl_values[impact_lvl],
            exploitability_lvl_values[exploitability_lvl])
