#!/usr/bin/env python3
"""Prove automatiche di panucci-ricerca-sentenze (senza rete, solo libreria standard).

Esecuzione:  python3 -B -m unittest discover -s prove -v
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

QUI = Path(__file__).resolve().parent
SKILL = QUI.parent / "panucci-ricerca-sentenze"
PROGRAMMA = SKILL / "strumenti" / "sentenze.py"

FATTORI = {
    "tesi": "Il legittimo interesse fonda le telefonate promozionali ai clienti",
    "fattori": [
        {"nome": "canale", "domanda": "Mezzo?", "valori": ["telefono con operatore", "sms", "posta"]},
        {"nome": "destinatari", "domanda": "Chi?", "valori": ["clienti", "prospect"]},
    ],
    "caso": {"canale": "telefono con operatore", "destinatari": "clienti"},
}

HTML = """<!DOCTYPE html><html><head><meta charset="utf-8"><script>var menu=1;</script></head><body>
<nav>Home Provvedimenti Contatti</nav>
<h2>Provvedimento del 11 gennaio 2024</h2>
<p>1. Premessa</p><p>La società ha effettuato telefonate promozionali ai propri clienti.</p>
<p>4.1 Le telefonate</p><p>Pertanto non può essere invocato il legittimo interesse del titolare quale presupposto
giuridico del trattamento per le telefonate con operatore verso i clienti.</p>
<p>4.2 La posta</p><p>Per la posta cartacea è invece possibile invocare il legittimo interesse, purché ricorra un bilanciamento conﬁgurato correttamente.</p>
<p>5. Dispositivo</p><p>Il Garante dichiara illecito il trattamento e irroga una sanzione di 100.000 euro alla società.</p>
<footer>Piè di pagina</footer></body></html>"""


def pdf_due_pagine(percorso, pagina1, pagina2):
    """Un PDF minimo di due pagine con testo semplice, scritto a mano (nessuna libreria)."""
    oggetti = []

    def flusso(testo):
        righe = "".join("BT /F1 11 Tf 40 %d Td (%s) Tj ET\n" % (780 - 16 * i, r.replace("(", "\\(").replace(")", "\\)"))
                        for i, r in enumerate(testo))
        return "<< /Length %d >>\nstream\n%sendstream" % (len(righe), righe)
    oggetti.append("<< /Type /Catalog /Pages 2 0 R >>")
    oggetti.append("<< /Type /Pages /Kids [3 0 R 4 0 R] /Count 2 >>")
    oggetti.append("<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Contents 5 0 R /Resources << /Font << /F1 7 0 R >> >> >>")
    oggetti.append("<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Contents 6 0 R /Resources << /Font << /F1 7 0 R >> >> >>")
    oggetti.append(flusso(pagina1))
    oggetti.append(flusso(pagina2))
    oggetti.append("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    out, posizioni = "%PDF-1.4\n", []
    for i, o in enumerate(oggetti, 1):
        posizioni.append(len(out))
        out += "%d 0 obj\n%s\nendobj\n" % (i, o)
    xref = len(out)
    out += "xref\n0 %d\n0000000000 65535 f \n" % (len(oggetti) + 1)
    out += "".join("%010d 00000 n \n" % p for p in posizioni)
    out += "trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(oggetti) + 1, xref)
    Path(percorso).write_bytes(out.encode("latin-1"))


def esegui(*args):
    return subprocess.run([sys.executable, "-I", str(PROGRAMMA), *map(str, args)], capture_output=True, text=True)


def ricerca(tmp):
    c = Path(tmp)
    for d in ("fonti", "analisi"):
        (c / d).mkdir()
    (c / "fattori.json").write_text(json.dumps(FATTORI, ensure_ascii=False), encoding="utf-8")
    (c / "candidati.csv").write_text(
        "id,fonte,autorita,tipo,data,numero,titolo,url_pagina,url_documento,formato,scelta,nota\n"
        "garante-1,garante,Garante,provvedimento,2024-01-11,1,prova,,,html,leggi,\n", encoding="utf-8")
    (c / "fonti" / "garante-1.html").write_text(HTML, encoding="utf-8")
    return c


def analisi(**cambi):
    a = {
        "id": "garante-1",
        "estremi": {"autorita": "Garante", "organo": "Collegio", "tipo": "provvedimento", "data": "2024-01-11",
                    "numero": "n. 1/2024", "parti": "oscurate"},
        "domanda_affrontata": "Se il legittimo interesse fondi le telefonate ai clienti",
        "risposta": "No per il telefono, sì per la posta",
        "peso": "regge la decisione", "esito": "contrario alla tesi",
        "fattori": {"canale": "telefono con operatore", "destinatari": "clienti"},
        "passaggi": [
            {"testo": "non può essere invocato il legittimo interesse del titolare quale presupposto giuridico del trattamento",
             "serve_a": "risposta"},
            {"testo": "per le telefonate con operatore verso i clienti", "serve_a": "fattore:canale"},
            {"testo": "telefonate promozionali ai propri clienti", "serve_a": "fattore:destinatari"},
            {"testo": "dichiara illecito il trattamento e irroga una sanzione di 100.000 euro", "serve_a": "esito"},
        ],
        "conseguenze": ["sanzione di 100.000 euro"], "norme": [], "precedenti": [], "lacune": [],
    }
    a.update(cambi)
    return a


def scrivi(c, a, nome="garante-1"):
    (c / "analisi" / (nome + ".json")).write_text(json.dumps(a, ensure_ascii=False), encoding="utf-8")


class Testi(unittest.TestCase):
    def test_html_senza_menu_e_script(self):
        with tempfile.TemporaryDirectory() as tmp:
            c = ricerca(tmp)
            self.assertEqual(esegui("testi", c).returncode, 0)
            t = (c / "testi" / "garante-1.txt").read_text(encoding="utf-8")
            self.assertIn("telefonate promozionali", t)
            self.assertNotIn("Contatti", t)
            self.assertNotIn("var menu", t)
            reg = json.loads((c / "registro.json").read_text(encoding="utf-8"))
            self.assertEqual(reg[0]["stato"], "ok")
            self.assertEqual(len(reg[0]["sha256"]), 64)


class Verifica(unittest.TestCase):
    def prepara(self, tmp, a):
        c = ricerca(tmp)
        esegui("testi", c)
        scrivi(c, a)
        return c

    def test_in_regola_e_paragrafi(self):
        with tempfile.TemporaryDirectory() as tmp:
            c = self.prepara(tmp, analisi())
            r = esegui("verifica", c)
            self.assertEqual(r.returncode, 0, r.stdout)
            v = json.loads((c / "verifiche.json").read_text(encoding="utf-8"))
            pos = {d["i"]: d["posizione"] for d in v["dettaglio"]}
            self.assertEqual(pos[0], "par. 4.1")
            self.assertEqual(pos[3], "par. 5")

    def test_passaggio_ritoccato_bloccato(self):
        with tempfile.TemporaryDirectory() as tmp:
            a = analisi()
            a["passaggi"][0]["testo"] = "non può mai essere invocato il legittimo interesse del titolare"
            c = self.prepara(tmp, a)
            r = esegui("verifica", c)
            self.assertEqual(r.returncode, 1)
            self.assertIn("ASSENTE", r.stdout)

    def test_fattore_senza_appiglio(self):
        with tempfile.TemporaryDirectory() as tmp:
            a = analisi()
            a["passaggi"] = [p for p in a["passaggi"] if p["serve_a"] != "fattore:destinatari"]
            c = self.prepara(tmp, a)
            r = esegui("verifica", c)
            self.assertEqual(r.returncode, 1)
            self.assertIn("senza un passaggio che lo regga", r.stdout)

    def test_peso_senza_passaggio_sulla_decisione(self):
        with tempfile.TemporaryDirectory() as tmp:
            a = analisi()
            a["passaggi"] = [p for p in a["passaggi"] if p["serve_a"] != "esito"]
            c = self.prepara(tmp, a)
            self.assertIn("senza un passaggio sul dispositivo", esegui("verifica", c).stdout)

    def test_omissioni_e_valori_non_previsti(self):
        with tempfile.TemporaryDirectory() as tmp:
            a = analisi(fattori={"canale": "fax", "destinatari": "clienti"})
            a["passaggi"][0]["testo"] = "non può essere invocato [...] presupposto giuridico del trattamento"
            c = self.prepara(tmp, a)
            out = esegui("verifica", c).stdout
            self.assertIn("niente omissioni", out)
            self.assertIn("valore 'fax' non previsto", out)

    def test_legatura_tipografica(self):
        with tempfile.TemporaryDirectory() as tmp:
            a = analisi()
            a["passaggi"].append({"testo": "purché ricorra un bilanciamento configurato correttamente", "serve_a": "risposta"})
            c = self.prepara(tmp, a)
            self.assertEqual(esegui("verifica", c).returncode, 0)

    def test_scelto_senza_analisi_e_scarti(self):
        with tempfile.TemporaryDirectory() as tmp:
            c = ricerca(tmp)
            esegui("testi", c)
            self.assertIn("senza analisi e senza scarto", esegui("verifica", c).stdout)
            (c / "scarti").mkdir()
            (c / "scarti" / "garante-1.txt").write_text("non tratta il tema", encoding="utf-8")
            self.assertIn("aggiorna la scelta", esegui("verifica", c).stdout)


@unittest.skipUnless(shutil.which("pdftotext") or shutil.which("osascript"), "nessun lettore PDF")
class Pdf(unittest.TestCase):
    def test_pagina_calcolata_e_sillabazione(self):
        with tempfile.TemporaryDirectory() as tmp:
            c = ricerca(tmp)
            (c / "fonti" / "garante-1.html").unlink()
            pdf_due_pagine(c / "fonti" / "garante-1.pdf",
                           ["Prima pagina del provvedimento.", "Fatti della causa e domande delle parti."]
                           + ["Riga di svolgimento del processo numero %d, senza rilievo." % i for i in range(6)],
                           ["Il ricorso e' fondato per le seguenti ra-", "gioni di diritto esposte dal collegio."]
                           + ["Riga di motivazione numero %d, senza rilievo per la prova." % i for i in range(6)])
            self.assertEqual(esegui("testi", c).returncode, 0)
            a = analisi(fattori={"canale": "non risulta", "destinatari": "non risulta"}, peso="solo citato",
                        passaggi=[{"testo": "Il ricorso e' fondato per le seguenti ragioni di diritto", "serve_a": "risposta"}])
            scrivi(c, a)
            r = esegui("verifica", c)
            self.assertEqual(r.returncode, 0, r.stdout)
            v = json.loads((c / "verifiche.json").read_text(encoding="utf-8"))
            self.assertEqual(v["dettaglio"][0]["posizione"], "p. 2")


class Campione(unittest.TestCase):
    def test_due_direzioni(self):
        with tempfile.TemporaryDirectory() as tmp:
            c = ricerca(tmp)
            casi = {"a-1": ("regge la decisione", "favorevole alla tesi"), "a-2": ("uno dei motivi", "contrario alla tesi"),
                    "a-3": ("detto di passaggio", "favorevole alla tesi"), "a-4": ("uno dei motivi", "favorevole alla tesi"),
                    "a-5": ("uno dei motivi", "neutro"), "a-6": ("solo citato", "neutro")}
            for i, (peso, esito) in casi.items():
                scrivi(c, analisi(id=i, peso=peso, esito=esito), nome=i)
            esegui("campione", c)
            righe = dict(r.split("\t") for r in (c / "seconda_lettura.txt").read_text(encoding="utf-8").splitlines())
            self.assertIn("a-1", righe)
            self.assertIn("a-2", righe)
            self.assertIn("a-3", righe)   # detto di passaggio: possibile sottovalutazione
            self.assertIn("a-6", righe)
            self.assertEqual(len(righe), 4)


class Matrice(unittest.TestCase):
    def test_vicinanza_e_posizioni(self):
        with tempfile.TemporaryDirectory() as tmp:
            c = ricerca(tmp)
            esegui("testi", c)
            scrivi(c, analisi())
            esegui("verifica", c)
            self.assertEqual(esegui("matrice", c).returncode, 0)
            m = (c / "matrice.md").read_text(encoding="utf-8")
            self.assertIn("| garante-1 | 2 (canale, destinatari) |", m)
            self.assertIn("(par. 4.1)", m)
            self.assertIn("contrario alla tesi 1 (garante-1)", m)


class Memo(unittest.TestCase):
    def test_frasi_del_memo(self):
        with tempfile.TemporaryDirectory() as tmp:
            c = ricerca(tmp)
            esegui("testi", c)
            (c / "memo.md").write_text("Il Garante: «dichiara illecito il trattamento e irroga una sanzione»; e «frase che nessuno ha mai scritto in alcun atto».", encoding="utf-8")
            r = esegui("memo", c)
            self.assertEqual(r.returncode, 1)
            self.assertIn("ritrovate nei testi integrali: 1/2", r.stdout)


class Bdp(unittest.TestCase):
    def test_importa(self):
        with tempfile.TemporaryDirectory() as tmp:
            c = ricerca(tmp)
            bdp = c / "bdp"
            bdp.mkdir()
            for n in ["SENTENZA_TRIBUNALE_DI_VARESE_N._567_2026_-_N._R.G._00001481_2025_DEPOSITO_MINUTA_10_10_2026__PUBBLICAZIONE_14_10_2026.pdf",
                      "SENTENZA_TRIBUNALE_DI_MILANO_-_N._R.G._00004147_2025_DEPOSITO_MINUTA_03_03_2025__PUBBLICAZIONE_04_03_2025.pdf",
                      "SENTENZA_TRIBUNALE_DI_MILANO_-_N._R.G._00004147_2025_DEPOSITO_MINUTA_03_03_2025__PUBBLICAZIONE_04_03_2025 (1).pdf",
                      "altro.pdf"]:
                (bdp / n).write_bytes(b"%PDF-1.4\n")
            r = esegui("importa-bdp", c, bdp)
            self.assertIn("Importati dalla BDP: 3; nomi non riconosciuti: 1", r.stdout)
            cand = (c / "candidati.csv").read_text(encoding="utf-8")
            self.assertIn("bdp-1481-2025,bdp,Tribunale di Varese,sentenza,2026-10-14,\"n. 567/2026, R.G. 1481/2025\"", cand)
            self.assertIn("bdp-4147-2025,bdp,Tribunale di Milano,sentenza,2025-03-04", cand)
            self.assertIn("bdp-4147-2025-2,", cand)
            self.assertTrue((c / "fonti" / "bdp-4147-2025.pdf").is_file())
            self.assertEqual(len(list(bdp.iterdir())), 4)


class Struttura(unittest.TestCase):
    def test_frontmatter(self):
        t = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        m = re.match(r"^---\nname: (.+)\ndescription: (.+)\n---\n", t)
        self.assertTrue(m)
        self.assertEqual(m.group(1), "panucci-ricerca-sentenze")
        self.assertLessEqual(len(m.group(2)), 1024)

    def test_file_citati_esistono(self):
        testi = "".join(p.read_text(encoding="utf-8") for p in SKILL.rglob("*.md"))
        for rel in set(re.findall(r"`((?:riferimenti|fonti|strumenti)/[a-z_]+\.(?:md|py))`", testi)):
            self.assertTrue((SKILL / rel).is_file(), rel)

    def test_programma_compila(self):
        r = subprocess.run([sys.executable, "-I", "-c", "import ast,sys;ast.parse(open(sys.argv[1]).read())", str(PROGRAMMA)])
        self.assertEqual(r.returncode, 0)

    def test_nessun_riferimento_ad_altre_skill_di_ricerca(self):
        vietati = ["ricerca-giurisprudenza", "strozzi", "avvocati-e-mac", "red team", "conteggi.py", "controlli.py"]
        for p in SKILL.rglob("*"):
            if p.is_file() and p.suffix in (".md", ".py", ".json"):
                t = p.read_text(encoding="utf-8").lower()
                for v in vietati:
                    self.assertNotIn(v, t, "%s contiene %r" % (p.name, v))


if __name__ == "__main__":
    unittest.main()
