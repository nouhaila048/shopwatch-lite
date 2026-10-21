from dataclasses import dataclass

NIVEAUX = ["MINEUR", "MODERE", "MAJEUR", "BLOQUANT"]

# Fiches de procedures (recherche simplifiee) : mot-cle -> conseil
FICHES = {
    "timeout": "Delai depasse : verifier la passerelle de paiement puis relancer le service.",
    "build": "Echec de build : lire le journal de l'etape puis rejouer apres correction.",
    "faille": "Faille connue : mettre a jour la dependance vers une version corrigee.",
}


@dataclass
class Signal:
    ref: str
    date: str
    origine: str        # PAIEMENT, SCANNER ou BUILD
    service: str
    env: str            # dev, test ou production
    categorie: str      # JOURNAL, FAILLE, BUILD_ECHEC ou BUILD_OK
    gravite: str
    texte: str
    etat: str = "RECU"  # RECU -> EVALUE -> DIFFUSE


@dataclass
class Diagnostic:
    signal_ref: str
    niveau: str
    cause: str
    action: str
    critique: bool
    origines: list


@dataclass
class Message:
    signal_ref: str
    canal: str
    destinataire: str
    contenu: str
