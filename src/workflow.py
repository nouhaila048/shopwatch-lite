from src import analyse, extraction, notification
from src.contrat import FICHES


def _traiter(sig, vus, compteur, registre, base):
    if analyse.est_repete(sig, vus):
        return None
    nb = analyse.compter_incidents(sig, compteur)
    diag = analyse.diagnostiquer(sig, base, nb)
    msg = notification.diffuser(sig, diag, registre)
    return {"signal": sig, "diagnostic": diag, "message": msg}


def traiter_journal(ligne, numero, vus, compteur, registre, base=FICHES):
    return _traiter(extraction.lire_journal(ligne, numero), vus, compteur, registre, base)


def traiter_scan(rapport, numero, vus, compteur, registre, base=FICHES):
    return _traiter(extraction.lire_scan(rapport, numero), vus, compteur, registre, base)


def traiter_build(rapport, numero, vus, compteur, registre, base=FICHES):
    return _traiter(extraction.lire_build(rapport, numero), vus, compteur, registre, base)
