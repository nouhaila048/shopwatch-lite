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


class TestLireJournal(unittest.TestCase):
    def test_lire_journal(self):
        sig = extraction.lire_journal(LIGNE, 42)
        self.assertEqual(sig.ref, "SH-0042")
        self.assertEqual(sig.date, "2026-11-27T17:02:11Z")
        self.assertEqual(sig.service, "paiement")
        self.assertEqual(sig.categorie, "JOURNAL")
        self.assertEqual(sig.origine, "PAIEMENT")
        self.assertEqual(sig.env, "production")
        self.assertEqual(sig.gravite, "MAJEUR")
        self.assertNotIn("4970123412341234", sig.texte)

    def test_gravites_journal(self):
        base = "2026-11-27 17:00:00 paiement {} message"
        attendu = {"FATAL": "BLOQUANT", "critical": "BLOQUANT",
                   "ERROR": "MAJEUR", "warn": "MODERE",
                   "WARNING": "MODERE", "INFO": "MINEUR"}
        for niveau, gravite in attendu.items():
            with self.subTest(niveau=niveau):
                sig = extraction.lire_journal(base.format(niveau), 1)
                self.assertEqual(sig.gravite, gravite)

    def test_journal_ligne_trop_courte(self):
        with self.assertRaises(ValueError):
            extraction.lire_journal("2026-11-27 17:00:00 paiement ERROR", 1)


class TestLireScan(unittest.TestCase):
    def test_lire_scan(self):
        sig = extraction.lire_scan(SCAN, 9)
        self.assertEqual(sig.ref, "SH-0009")
        self.assertEqual(sig.origine, "SCANNER")
        self.assertEqual(sig.service, "lib-panier")
        self.assertEqual(sig.categorie, "FAILLE")
        self.assertEqual(sig.gravite, "BLOQUANT")
        self.assertEqual(sig.texte, "Faille CVE-2026-7788 dans lib-panier")

    def test_gravites_scan(self):
        attendu = {"HAUT": "MAJEUR", "moyen": "MODERE", "faible": "MINEUR"}
        for risque, gravite in attendu.items():
            with self.subTest(risque=risque):
                sig = extraction.lire_scan({**SCAN, "risque": risque}, 1)
                self.assertEqual(sig.gravite, gravite)

    def test_scan_cle_manquante(self):
        with self.assertRaises(ValueError):
            extraction.lire_scan({"paquet": "lib-panier"}, 1)


class TestLireBuild(unittest.TestCase):
    def test_lire_build_echec(self):
        sig = extraction.lire_build(BUILD, 8)
        self.assertEqual(sig.origine, "BUILD")
        self.assertEqual(sig.service, "deploiement")
        self.assertEqual(sig.categorie, "BUILD_ECHEC")
        self.assertEqual(sig.gravite, "MAJEUR")
        self.assertEqual(sig.texte, "Build deploiement : echec")

    def test_lire_build_ok(self):
        sig = extraction.lire_build({**BUILD, "resultat": "succes"}, 8)
        self.assertEqual(sig.categorie, "BUILD_OK")
        self.assertEqual(sig.gravite, "MINEUR")

    def test_build_cle_manquante(self):
        with self.assertRaises(ValueError):
            extraction.lire_build({"etape": "test"}, 1)
