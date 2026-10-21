from src.contrat import Diagnostic, Signal


def est_repete(sig: Signal, vus: set) -> bool:
    raise NotImplementedError


def compter_incidents(sig: Signal, compteur: dict) -> int:
    raise NotImplementedError


def chercher_fiches(sig: Signal, base: dict) -> list:
    raise NotImplementedError


def evaluer(sig: Signal, nb_incidents: int = 0) -> str:
    raise NotImplementedError


def diagnostiquer(sig: Signal, base: dict, nb_incidents: int = 0) -> Diagnostic:
    raise NotImplementedError
