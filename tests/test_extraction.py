import unittest

from src import extraction

LIGNE = ("2026-11-27 17:02:11 paiement ERROR timeout passerelle apres 30s "
         "card=4970123412341234")
SCAN = {"id_faille": "CVE-2026-7788", "paquet": "lib-panier",
        "risque": "critique", "date": "2026-11-27T17:09:00Z"}
BUILD = {"etape": "deploiement", "resultat": "echec",
         "date": "2026-11-27T17:08:00Z"}


class TestExtraction(unittest.TestCase):
    def test_masquer_donnees(self):
        self.assertEqual(extraction.masquer_donnees("client=bob pwd=abc123"),
                         "client=bob pwd=[MASQUE]")

    def test_masquer_insensible_casse(self):
        self.assertEqual(extraction.masquer_donnees("PASSWORD=Secret1"),
                         "PASSWORD=[MASQUE]")

    def test_masquer_forme_deux_points(self):
        self.assertEqual(extraction.masquer_donnees("token: xyz789 ok"),
                         "token: [MASQUE] ok")

    def test_masquer_separateurs(self):
        self.assertEqual(
            extraction.masquer_donnees("iban=FR76&secret=abc;card=1234,fin"),
            "iban=[MASQUE]&secret=[MASQUE];card=[MASQUE],fin")

    def test_texte_sans_secret_inchange(self):
        self.assertEqual(extraction.masquer_donnees("Service demarre"),
                         "Service demarre")
