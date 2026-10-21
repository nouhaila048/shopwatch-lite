import re

from src.contrat import Signal

# nom=valeur ou nom: valeur ; la valeur s'arrete a un espace, &, "," ou ";"
MOTIF_SENSIBLE = re.compile(
    r"\b(password|pwd|token|secret|card|iban)(=|:\s*)[^\s&,;]+",
    re.IGNORECASE,
)


def masquer_donnees(texte: str) -> str:
    return MOTIF_SENSIBLE.sub(r"\1\2[MASQUE]", texte)
