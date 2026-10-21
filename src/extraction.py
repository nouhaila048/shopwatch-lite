import re

from src.contrat import Signal

# nom=valeur ou nom: valeur ; la valeur s'arrete a un espace, &, "," ou ";"
MOTIF_SENSIBLE = re.compile(
    r"\b(password|pwd|token|secret|card|iban)(=|:\s*)[^\s&,;]+",
    re.IGNORECASE,
)


def masquer_donnees(texte: str) -> str:
    return MOTIF_SENSIBLE.sub(r"\1\2[MASQUE]", texte)


GRAVITE_JOURNAL = {
    "FATAL": "BLOQUANT",
    "CRITICAL": "BLOQUANT",
    "ERROR": "MAJEUR",
    "WARN": "MODERE",
    "WARNING": "MODERE",
}


def lire_journal(ligne: str, numero: int, origine: str = "PAIEMENT",
                 env: str = "production") -> Signal:
    champs = ligne.split(maxsplit=4)
    if len(champs) < 5:
        raise ValueError(f"Ligne de journal invalide : {ligne!r}")
    jour, heure, service, niveau, message = champs
    return Signal(
        ref=f"SH-{numero:04d}",
        date=f"{jour}T{heure}Z",
        origine=origine,
        service=service,
        env=env,
        categorie="JOURNAL",
        gravite=GRAVITE_JOURNAL.get(niveau.upper(), "MINEUR"),
        texte=masquer_donnees(message),
    )


GRAVITE_SCAN = {
    "critique": "BLOQUANT",
    "haut": "MAJEUR",
    "moyen": "MODERE",
}


def _verifier_cles(rapport: dict, cles: list) -> None:
    for cle in cles:
        if cle not in rapport:
            raise ValueError(f"Cle manquante dans le rapport : {cle}")


def lire_scan(rapport: dict, numero: int, env: str = "production") -> Signal:
    _verifier_cles(rapport, ["id_faille", "paquet", "risque", "date"])
    return Signal(
        ref=f"SH-{numero:04d}",
        date=rapport["date"],
        origine="SCANNER",
        service=rapport["paquet"],
        env=env,
        categorie="FAILLE",
        gravite=GRAVITE_SCAN.get(rapport["risque"].lower(), "MINEUR"),
        texte=f"Faille {rapport['id_faille']} dans {rapport['paquet']}",
    )
