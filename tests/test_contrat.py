import unittest

from src.contrat import FICHES, NIVEAUX, Signal


class TestContrat(unittest.TestCase):
    def test_etat_par_defaut(self):
        s = Signal("SH-0001", "2026-11-27T17:00:00Z", "PAIEMENT", "paiement",
                   "production", "JOURNAL", "MINEUR", "demarrage")
        self.assertEqual(s.etat, "RECU")

    def test_niveaux_ordonnes(self):
        self.assertEqual(NIVEAUX[0], "MINEUR")
        self.assertEqual(NIVEAUX[-1], "BLOQUANT")

    def test_base_fiches(self):
        self.assertIn("timeout", FICHES)
