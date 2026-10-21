from src.contrat import Diagnostic, Message, Signal

CANAUX = {
    "BLOQUANT": "SLACK",
    "MAJEUR": "TEAMS",
    "MODERE": "EMAIL",
    "MINEUR": "TABLEAU",
}


def choisir_canal(niveau: str) -> str:
    if niveau not in CANAUX:
        raise ValueError(f"Niveau inconnu : {niveau}")
    return CANAUX[niveau]


def composer(sig: Signal, diag: Diagnostic) -> str:
    raise NotImplementedError


def diffuser(sig: Signal, diag: Diagnostic, registre: list) -> Message:
    raise NotImplementedError


def approuver(diag: Diagnostic, reponse: str) -> bool:
    raise NotImplementedError


def consigner(diag: Diagnostic, accord: bool, responsable: str,
              carnet: list, instant: str) -> dict:
    raise NotImplementedError
