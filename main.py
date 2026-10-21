import sys
from datetime import datetime, timezone

from src.notification import approuver, consigner
from src.workflow import traiter_build, traiter_journal, traiter_scan

JOURNAL = [
    "2026-11-27 17:00:01 paiement INFO Service demarre",
    "2026-11-27 17:02:11 paiement ERROR timeout passerelle apres 30s card=4970123412341234",
    "2026-11-27 17:02:11 paiement ERROR timeout passerelle apres 30s card=4970123412341234",
    "2026-11-27 17:03:20 paiement ERROR timeout passerelle apres 31s",
    "2026-11-27 17:04:30 paiement ERROR timeout passerelle apres 29s",
    "2026-11-27 17:05:40 paiement ERROR timeout passerelle apres 33s",
    "2026-11-27 17:06:50 paiement ERROR timeout passerelle apres 35s",
]
RAPPORTS_BUILD = [
    {"etape": "deploiement", "resultat": "echec", "date": "2026-11-27T17:08:00Z"},
]
RAPPORTS_SCAN = [
    {"id_faille": "CVE-2026-7788", "paquet": "lib-panier", "risque": "critique",
     "date": "2026-11-27T17:09:00Z"},
]


def afficher(resultat, carnet):
    msg, diag = resultat["message"], resultat["diagnostic"]
    print(f">>> {msg.signal_ref} par {msg.canal} ({msg.destinataire})")
    print(msg.contenu)
    if diag.critique:
        reponse = input("Action critique. Autoriser ? (o/n) : ")
        accord = approuver(diag, reponse)
        instant = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        consigner(diag, accord, "astreinte-shop", carnet, instant)
        print("Decision :", "AUTORISEE" if accord else "REFUSEE",
              "(simulation : rien n'est execute)")
    print()


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    vus, compteur, registre, carnet = set(), {}, [], []
    entrees = [(traiter_journal, x) for x in JOURNAL]
    entrees += [(traiter_build, x) for x in RAPPORTS_BUILD]
    entrees += [(traiter_scan, x) for x in RAPPORTS_SCAN]
    repetes = 0
    for numero, (traiter, brut) in enumerate(entrees, start=1):
        resultat = traiter(brut, numero, vus, compteur, registre)
        if resultat is None:
            repetes += 1
            print(f">>> SH-{numero:04d} ignore (repete)\n")
        else:
            afficher(resultat, carnet)
    print(f"{len(entrees)} signaux recus, {repetes} repete(s) ignore(s), "
          f"{len(registre)} message(s) diffuse(s), {len(carnet)} decision(s) consignee(s).")


if __name__ == "__main__":
    main()
