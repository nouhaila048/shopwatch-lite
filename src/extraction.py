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
