def vulnCvssv3(v):
    return cvssv3(v["AV"], v["AC"], v["PR"], v["UI"], v["S"], v["C"], v["I"], v["A"])

def cvssv3(av, ac, pr, ui, s, c, i, a):
    AV = {"N": 0.85, "A": 0.62, "L": 0.55, "P": 0.2}
    AC = {"L": 0.77, "H": 0.44}
    if s == "C":
        PR = {"N": 0.85, "L": 0.68, "H": 0.5}
    else:
        PR = {"N": 0.85, "L": 0.62, "H": 0.27}
    UI = {"N": 0.85, "R": 0.62}
    CIA = {"N": 0, "L": 0.22, "H": 0.56}
    av = AV[av[0]]
    ac = AC[ac[0]]
    pr = PR[pr[0]]
    ui = UI[ui[0]]
    c = CIA[c[0]]
    i = CIA[i[0]]
    a = CIA[a[0]]
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

def vulnRiskLevel(v):
    return riskLevel(v["AV"], v["AC"], v["PR"], v["UI"], v["S"], v["C"], v["I"], v["A"])

def riskLevel(av, ac, pr, ui, s, c, i, a):
    CIA = {"N": 0, "L": 1, "H": 2}
    S = {"U": False, "C": True}
    c = CIA[c[0]]
    i = CIA[i[0]]
    a = CIA[a[0]]
    s = S[s[0]]

    if c == 2 or i == 2 or (c*2+i*2+a >= 5 and s):
        iLvl = 4
    elif a == 2 or c*2+i*2+a >= 5 or (c*2+i*2+a >= 3 and s):
        iLvl = 3
    elif c*2+i*2+a >= 3 or s:
        iLvl = 2
    else:
        iLvl = 1

    AV = {"N": 1, "A": 2, "L": 3, "P": 4}
    AC = {"L": 1, "H": 2}
    PR = {"N": 0, "L": 1, "H": 2}
    UI = {"N": False, "R": True}
    av = AV[av[0]]
    ac = AC[ac[0]]
    pr = PR[pr[0]]
    ui = UI[ui[0]]

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
