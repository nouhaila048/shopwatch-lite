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


if __name__ == "__main__":
    unittest.main()
