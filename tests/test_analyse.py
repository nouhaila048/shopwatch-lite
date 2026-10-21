import unittest

from src.analyse import (
    est_repete,
    compter_incidents,
    chercher_fiches,
    evaluer,
    diagnostiquer
)
from src.contrat import FICHES, Signal


def sig(
    categorie="JOURNAL",
    gravite="MAJEUR",
    texte="timeout passerelle apres 30s",
    service="paiement",
    date="2026-11-27T17:00:00Z"
):
    return Signal(
        "SH-0001",
        date,
        "PAIEMENT",
        service,
        "production",
        categorie,
        gravite,
        texte
    )


class TestAnalyse(unittest.TestCase):

    def test_repete(self):
        vus = set()

        self.assertFalse(est_repete(sig(), vus))
        self.assertTrue(est_repete(sig(), vus))

    def test_dates_differentes(self):
        vus = set()

        s1 = sig(date="2026-11-27T17:00:00Z")
        s2 = sig(date="2026-11-27T17:00:01Z")

        self.assertFalse(est_repete(s1, vus))
        self.assertFalse(est_repete(s2, vus))

    def test_compter_incidents(self):
        compteur = {}

        s1 = sig()
        s2 = sig()
        s3 = sig()

        self.assertEqual(compter_incidents(s1, compteur), 1)
        self.assertEqual(compter_incidents(s2, compteur), 2)
        self.assertEqual(compter_incidents(s3, compteur), 3)

        self.assertEqual(compteur["paiement"], 3)

    def test_incident_non_compte(self):
        compteur = {}

        s1 = sig(gravite="MODERE")
        s2 = sig(categorie="BUILD_ECHEC")

        self.assertEqual(compter_incidents(s1, compteur), 0)
        self.assertEqual(compter_incidents(s2, compteur), 0)
        self.assertEqual(compteur, {})
    def test_chercher_fiches(self):
        s = sig(texte="TIMEOUT sur la passerelle")

        resultats = chercher_fiches(s, FICHES)

        self.assertEqual(
            resultats,
            [FICHES["timeout"]]
        )

    def test_chercher_plusieurs_fiches(self):
        s = sig(texte="timeout et build en echec")

        resultats = chercher_fiches(s, FICHES)

        self.assertEqual(
            resultats,
            [FICHES["timeout"], FICHES["build"]]
        )

    def test_aucune_fiche(self):
        s = sig(texte="probleme inconnu")

        self.assertEqual(
            chercher_fiches(s, FICHES),
            []
        )

    def test_evaluer_panne_en_boucle(self):
        s = sig()

        self.assertEqual(evaluer(s, 4), "BLOQUANT")
        self.assertEqual(evaluer(s, 3), "MAJEUR")

    def test_diagnostiquer_bloquant(self):
        s = sig()

        diagnostic = diagnostiquer(s, FICHES, 4)

        self.assertEqual(diagnostic.signal_ref, "SH-0001")
        self.assertEqual(diagnostic.niveau, "BLOQUANT")
        self.assertEqual(
            diagnostic.cause,
            FICHES["timeout"]
        )
        self.assertEqual(
            diagnostic.action,
            "Isoler le service paiement"
        )
        self.assertTrue(diagnostic.critique)
        self.assertEqual(diagnostic.origines, ["PAIEMENT"])
        self.assertEqual(s.etat, "EVALUE")

    def test_diagnostiquer_faille(self):
        s = sig(
            categorie="FAILLE",
            gravite="BLOQUANT",
            texte="faille detectee",
            service="lib-panier"
        )

        diagnostic = diagnostiquer(s, FICHES)

        self.assertEqual(
            diagnostic.action,
            "Corriger la dependance lib-panier"
        )
        self.assertFalse(diagnostic.critique)
        self.assertEqual(s.etat, "EVALUE")

    def test_diagnostiquer_build(self):
        s = sig(
            categorie="BUILD_ECHEC",
            gravite="MAJEUR",
            texte="build en echec",
            service="deploiement"
        )

        diagnostic = diagnostiquer(s, FICHES)

        self.assertEqual(
            diagnostic.action,
            "Rejouer le build deploiement"
        )
        self.assertFalse(diagnostic.critique)

    def test_diagnostiquer_inconnu(self):
        s = sig(
            gravite="MINEUR",
            texte="probleme inconnu"
        )

        diagnostic = diagnostiquer(s, FICHES)

        self.assertEqual(
            diagnostic.cause,
            "Cause inconnue : verification manuelle"
        )
        self.assertEqual(diagnostic.action, "Observer")
        self.assertFalse(diagnostic.critique)

if __name__ == "__main__":
    unittest.main()
