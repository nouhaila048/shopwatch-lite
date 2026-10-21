from src.contrat import Diagnostic, Signal


def est_repete(sig: Signal, vus: set) -> bool:
    cle = (
        sig.date,
        sig.origine,
        sig.service,
        sig.categorie,
        sig.texte
    )

    if cle in vus:
        return True

    vus.add(cle)
    return False


def compter_incidents(sig: Signal, compteur: dict) -> int:
    if (
        sig.categorie == "JOURNAL"
        and sig.gravite in ("MAJEUR", "BLOQUANT")
    ):
        compteur[sig.service] = compteur.get(sig.service, 0) + 1
        return compteur[sig.service]

    return 0


def chercher_fiches(sig: Signal, base: dict) -> list:
    resultats = []

    for mot_cle, conseil in base.items():
        if mot_cle.lower() in sig.texte.lower():
            resultats.append(conseil)

    return resultats


def evaluer(sig: Signal, nb_incidents: int = 0) -> str:
    if nb_incidents > 100:
        return "BLOQUANT"

    return sig.gravite


def diagnostiquer(
    sig: Signal,
    base: dict,
    nb_incidents: int = 0
) -> Diagnostic:

    # 1. Evaluer le niveau
    niveau = evaluer(sig, nb_incidents)

    # 2. Rechercher les fiches de procedures
    conseils = chercher_fiches(sig, base)

    # 3. Determiner la cause
    if conseils:
        cause = " ; ".join(conseils)
    else:
        cause = "Cause inconnue : verification manuelle"

    # 4. Determiner l'action
    if sig.categorie == "FAILLE":
        action = f"Corriger la dependance {sig.service}"

    elif sig.categorie == "BUILD_ECHEC":
        action = f"Rejouer le build {sig.service}"

    elif niveau == "BLOQUANT":
        action = f"Isoler le service {sig.service}"

    else:
        action = "Observer"

    # 5. Determiner si l'action est critique
    critique = action.startswith("Isoler")

    # 6. Creer le diagnostic
    diagnostic = Diagnostic(
        signal_ref=sig.ref,
        niveau=niveau,
        cause=cause,
        action=action,
        critique=critique,
        origines=[sig.origine]
    )

    # 7. Mettre a jour l'etat du signal
    sig.etat = "EVALUE"

    return diagnostic
