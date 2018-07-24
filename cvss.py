def cvssFromValues(v, doc_id):
    av = v["AV-"+str(doc_id)]
    ac = v["AC-"+str(doc_id)]
    pr = v["PR-"+str(doc_id)]
    ui = v["UI-"+str(doc_id)]
    s = v["S-"+str(doc_id)]
    c = v["C-"+str(doc_id)]
    i = v["I-"+str(doc_id)]
    a = v["A-"+str(doc_id)]
    cvss, imp, exp = cvssv3(av, ac, pr, ui, s, c, i, a)
    rLvl, iLvl, eLvl = riskLevel(av, ac, pr, ui, s, c, i, a)
    return cvss, imp, exp, rLvl, iLvl, eLvl

def cvssv3(av, ac, pr, ui, s, c, i, a):
    AV = {"Network": 0.85, "Adjacent Network": 0.62, "Local": 0.55, "Physical": 0.2}
    AC = {"Low": 0.77, "High": 0.44}
    if s == "Changed":
        PR = {"None": 0.85, "Low": 0.68, "High": 0.5}
    else:
        PR = {"None": 0.85, "Low": 0.62, "High": 0.27}
    UI = {"None": 0.85, "Required": 0.62}
    CIA = {"None": 0, "Low": 0.22, "High": 0.56}
    av = AV[av]
    ac = AC[ac]
    pr = PR[pr]
    ui = UI[ui]
    c = CIA[c]
    i = CIA[i]
    a = CIA[a]
    exp = 8.22 * av * ac * pr * ui
    imp = 1-((1-c)*(1-i)*(1-a))
    if s == "Changed":
        imp = 7.52*(imp-0.029) - 3.25*(imp-0.02)**15
        score = 1.08 * (imp+exp)
    else:
        imp = 6.42 * imp
        score = imp + exp
    if imp <= 0:
        score = 0.0
    if score > 10:
        score = 10.0
    return round(score,1), round(imp,1), round(exp,1)

def riskLevel(av, ac, pr, ui, s, c, i, a):
    CIA = {"None": 0, "Low": 1, "High": 2}
    S = {"Unchanged": False, "Changed": True}
    c = CIA[c]
    i = CIA[i]
    a = CIA[a]
    s = S[s]

    if c == 2 or i == 2 or (c*2+i*2+a >= 5 and s):
        iLvl = 4
    elif a == 2 or c*2+i*2+a >= 5 or (c*2+i*2+a >= 3 and s):
        iLvl = 3
    elif c*2+i*2+a >= 3 or s:
        iLvl = 2
    else:
        iLvl = 1

    AV = {"Network": 1, "Adjacent Network": 2, "Local": 3, "Physical": 4}
    AC = {"Low": 1, "High": 2}
    PR = {"None": 0, "Low": 1, "High": 2}
    UI = {"None": False, "Required": True}
    av = AV[av]
    ac = AC[ac]
    pr = PR[pr]
    ui = UI[ui]

    if av == 4 or pr == 2 or (av == 3 and pr == 1 and ui) or (ac == 2 and (av == 3 or pr == 1 or ui)):
        eLvl = 1
    elif ac == 2 or av == 3 or (av == 2 and (pr == 1 or ui)) or (pr == 1 and ui):
        eLvl = 2
    elif av == 2 or pr == 1 or ui:
        eLvl = 3
    else:
        eLvl = 4

    if (iLvl == 1 and eLvl <= 2) or (eLvl == 1 and iLvl <= 2):
        rLvl = 1
    elif (iLvl <= 3 and eLvl <= 2) or iLvl == 1:
        rLvl = 2
    elif (iLvl <= 4 and eLvl <= 2) or (iLvl <= 3 and eLvl <= 3) or iLvl == 2:
        rLvl = 3
    else:
        rLvl = 4

    RLVL = {1:"Low", 2:"Medium", 3:"High", 4:"Very High"}
    ILVL = {1:"Low", 2:"Medium", 3:"High", 4:"Very High"}
    ELVL = {1:"Dificult", 2:"Medium", 3:"Easy", 4:"Very Easy"}

    return RLVL[rLvl], ILVL[iLvl], ELVL[eLvl]
