#!/usr/bin/env python3
"""panucci-ricerca-sentenze: gli attrezzi meccanici della ricerca (nessun modello, 0 token).

Uso:  python3 sentenze.py <comando> <cartella_ricerca> [opzioni]

Comandi:
  scarica      scarica i documenti delle righe di candidati.csv con scelta = leggi
               (--anche-riserva per includere le righe "riserva") in fonti/
  testi        ricava il testo integrale di ogni file in fonti/ in testi/<id>.txt
               e scrive registro.json (metodo, impronta sha256, pagine, stato)
  campione     sceglie le analisi per la seconda lettura -> seconda_lettura.txt
  verifica     controlla le analisi in analisi/: forma, fattori, e che ogni passaggio
               citato sia nel testo integrale; calcola pagina o paragrafo; scrive
               verifiche.json e verifiche.txt. Esce con 1 se c'e' qualcosa da sistemare.
  matrice      costruisce matrice.md (fattori x esito, vicinanza al caso, passaggi
               con la loro posizione) da analisi/, fattori.json e verifiche.json
  memo         [file]  controlla che ogni frase tra «» del memo (default memo.md) sia
               nel testo integrale di un provvedimento letto; esce con 1 se una manca
  importa-bdp  <cartella_bdp>  aggiunge a candidati.csv i PDF scaricati dalla Banca Dati
               di Merito con la skill bdp-ricerca e li copia in fonti/

Regole di rete: user-agent dichiarato, robots.txt rispettato, pausa tra i file,
certificati sempre verificati (si usa curl con i certificati di sistema).
Solo libreria standard di Python 3, piu' curl e, se c'e', pdftotext.
"""
import csv
import hashlib
import html
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import unicodedata
import urllib.parse
import urllib.robotparser
from html.parser import HTMLParser

AGENTE = "panucci-ricerca-sentenze/1.0 (ricerca di provvedimenti pubblici per uno studio legale)"
COLONNE = ["id", "fonte", "autorita", "tipo", "data", "numero", "titolo", "url_pagina",
           "url_documento", "formato", "scelta", "nota"]
SCELTE = ("leggi", "riserva", "scarta")
PESI = ("regge la decisione", "uno dei motivi", "detto di passaggio", "solo citato")
ESITI = ("favorevole alla tesi", "contrario alla tesi", "misto", "neutro")
NON_RISULTA = "non risulta"
RE_ID = re.compile(r"^[a-z0-9][a-z0-9-]*$")
RE_DATA = re.compile(r"^\d{4}-\d{2}-\d{2}$")
MAX_PAROLE_PASSAGGIO = 40


# =============================================================== file di lavoro
def leggi_candidati(cartella):
    p = os.path.join(cartella, "candidati.csv")
    if not os.path.isfile(p):
        return []
    with open(p, encoding="utf-8-sig", newline="") as f:
        return [{(k or "").strip(): (v or "").strip() for k, v in r.items()} for r in csv.DictReader(f)]


def scrivi_candidati(cartella, righe):
    p = os.path.join(cartella, "candidati.csv")
    colonne = list(COLONNE)
    for r in righe:
        colonne += [k for k in r if k and k not in colonne]
    tmp = p + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=colonne)
        w.writeheader()
        for r in righe:
            w.writerow({k: r.get(k, "") for k in colonne})
    os.replace(tmp, p)


def leggi_json(p, predefinito=None):
    try:
        with open(p, encoding="utf-8-sig") as f:
            return json.load(f)
    except (OSError, ValueError):
        return predefinito


def scrivi_json(p, dati):
    tmp = p + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(dati, f, ensure_ascii=False, indent=1)
    os.replace(tmp, p)


def impronta(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


# =============================================================== rete
def curl(url, dest, rinvio=None, attesa=60):
    """Scarica con curl (certificati di sistema, verificati). Restituisce (ok, messaggio)."""
    exe = shutil.which("curl")
    if not exe:
        return False, "curl non disponibile"
    cmd = [exe, "-sS", "-L", "--proto", "=https,http", "-m", str(attesa), "-A", AGENTE,
           "-o", dest, "-w", "%{http_code}"]
    if rinvio and rinvio.startswith("http"):
        cmd += ["-e", rinvio]
    try:
        r = subprocess.run(cmd + [url], capture_output=True, text=True, timeout=attesa + 15)
    except (OSError, subprocess.SubprocessError) as e:
        return False, "rete: %s" % e
    codice = (r.stdout or "").strip()[-3:]
    if r.returncode != 0:
        return False, "rete: %s" % (r.stderr.strip().splitlines() or ["errore curl %d" % r.returncode])[-1]
    if not codice.startswith("2"):
        return False, "il sito risponde HTTP %s" % codice
    return True, "ok"


_regole_robots = {}


def robots_permette(url):
    """True/False secondo robots.txt; None se robots.txt non e' leggibile (si tratta come permesso
    ma lo si annota)."""
    p = urllib.parse.urlparse(url)
    base = "%s://%s" % (p.scheme, p.netloc)
    if base not in _regole_robots:
        fd, tmp = tempfile.mkstemp(suffix=".txt")
        os.close(fd)
        try:
            ok, _ = curl(base + "/robots.txt", tmp, attesa=20)
            if ok:
                rp = urllib.robotparser.RobotFileParser()
                with open(tmp, encoding="utf-8", errors="replace") as f:
                    rp.parse(f.read().splitlines())
                _regole_robots[base] = rp
            else:
                _regole_robots[base] = None
        finally:
            os.remove(tmp)
    rp = _regole_robots[base]
    return None if rp is None else rp.can_fetch(AGENTE, url)


def tipo_contenuto(p):
    with open(p, "rb") as f:
        testa = f.read(4096)
    if testa.startswith(b"%PDF"):
        return "pdf"
    t = testa.lower()
    if b"<html" in t or b"<!doctype html" in t:
        return "html"
    return None


def file_in_fonti(cartella, ident):
    d = os.path.join(cartella, "fonti")
    for est in ("pdf", "html"):
        p = os.path.join(d, "%s.%s" % (ident, est))
        if os.path.isfile(p) and os.path.getsize(p) > 0:
            return p
    return None


def cmd_scarica(cartella, opzioni):
    righe = leggi_candidati(cartella)
    volute = ("leggi", "riserva") if "--anche-riserva" in opzioni else ("leggi",)
    os.makedirs(os.path.join(cartella, "fonti"), exist_ok=True)
    esiti, primo = [], True
    for r in righe:
        ident = r.get("id", "")
        if r.get("scelta") not in volute:
            continue
        if file_in_fonti(cartella, ident):
            esiti.append((ident, "gia' presente"))
            continue
        url = r.get("url_documento") or r.get("url_pagina")
        if not url.startswith("http"):
            esiti.append((ident, "nessun indirizzo scaricabile"))
            continue
        permesso = robots_permette(url)
        if permesso is False:
            esiti.append((ident, "robots.txt non permette lo scaricamento automatico: aprire a mano " + url))
            continue
        if not primo:
            time.sleep(2)
        primo = False
        fd, tmp = tempfile.mkstemp(dir=os.path.join(cartella, "fonti"), suffix=".part")
        os.close(fd)
        ok, msg = curl(url, tmp, rinvio=r.get("url_pagina"))
        tipo = tipo_contenuto(tmp) if ok else None
        if ok and tipo:
            os.replace(tmp, os.path.join(cartella, "fonti", "%s.%s" % (ident, tipo)))
            esiti.append((ident, "scaricato (%s)%s" % (tipo, "; robots.txt non leggibile" if permesso is None else "")))
        else:
            os.remove(tmp)
            esiti.append((ident, msg if not ok else "risposta non PDF ne' HTML (pagina di errore o di accesso?)"))
    with open(os.path.join(cartella, "scaricamenti.txt"), "w", encoding="utf-8") as f:
        f.write("".join("%s\t%s\n" % e for e in esiti))
    for e in esiti:
        print("%-28s %s" % e)
    falliti = [e for e in esiti if not e[1].startswith(("scaricato", "gia'"))]
    print("Totale: %d, non riusciti: %d" % (len(esiti), len(falliti)))
    return 1 if falliti else 0


# =============================================================== testi
class _Lettore(HTMLParser):
    NASCOSTI = {"script", "style", "noscript", "nav", "header", "footer", "form", "svg", "button", "aside"}
    A_CAPO = {"p", "div", "br", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6", "section",
              "article", "td", "blockquote"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.pezzi, self.nascosto = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in self.NASCOSTI:
            self.nascosto += 1
        elif tag in self.A_CAPO:
            self.pezzi.append("\n")

    def handle_endtag(self, tag):
        if tag in self.NASCOSTI:
            self.nascosto = max(0, self.nascosto - 1)
        elif tag in self.A_CAPO:
            self.pezzi.append("\n")

    def handle_data(self, data):
        if not self.nascosto:
            self.pezzi.append(data)


def testo_da_html(p):
    grezzo = open(p, "rb").read()
    m = re.search(rb'charset=["\']?([A-Za-z0-9_-]+)', grezzo[:4000])
    try:
        t = grezzo.decode(m.group(1).decode() if m else "utf-8", "replace")
    except LookupError:
        t = grezzo.decode("utf-8", "replace")
    lt = _Lettore()
    lt.feed(t)
    righe = (" ".join(html.unescape(x).split()) for x in "".join(lt.pezzi).splitlines())
    return "\n".join(x for x in righe if x), "html"


PDFKIT = r"""ObjC.import('PDFKit');
function run(a){var d=$.PDFDocument.alloc.initWithURL($.NSURL.fileURLWithPath(a[0]));
if(!d||d.isNil())return '';var o=[];for(var i=0;i<d.pageCount;i++){var s=d.pageAtIndex(i).string;
o.push((s&&!s.isNil())?ObjC.unwrap(s):'');}return o.join('\f');}"""


def testo_da_pdf(p):
    exe = shutil.which("pdftotext")
    if exe:
        r = subprocess.run([exe, "-enc", "UTF-8", p, "-"], capture_output=True, timeout=180)
        if r.returncode == 0:
            return r.stdout.decode("utf-8", "replace"), "pdftotext"
    exe = shutil.which("osascript")
    if exe:
        r = subprocess.run([exe, "-l", "JavaScript", "-e", PDFKIT, p], capture_output=True, timeout=180)
        if r.returncode == 0:
            return r.stdout.decode("utf-8", "replace"), "pdfkit"
    return None, None


def cmd_testi(cartella, opzioni):
    d_fonti, d_testi = os.path.join(cartella, "fonti"), os.path.join(cartella, "testi")
    os.makedirs(d_testi, exist_ok=True)
    registro = []
    nomi = sorted(os.listdir(d_fonti)) if os.path.isdir(d_fonti) else []
    for nome in nomi:
        ident, est = os.path.splitext(nome)
        if est not in (".pdf", ".html"):
            continue
        p = os.path.join(d_fonti, nome)
        voce = {"id": ident, "file": "fonti/" + nome, "sha256": impronta(p), "metodo": None,
                "pagine": None, "caratteri": 0, "stato": "illeggibile", "nota": ""}
        tipo = tipo_contenuto(p)
        testo, metodo = (testo_da_pdf(p) if tipo == "pdf" else testo_da_html(p) if tipo == "html"
                         else (None, None))
        if testo is None:
            voce["nota"] = "nessuno strumento per leggere il file" if tipo else "file non riconosciuto"
        elif len(re.sub(r"\s", "", testo)) < 200:
            voce.update(metodo=metodo, stato="senza testo", nota="probabile scansione: serve OCR, non fatto")
        else:
            with open(os.path.join(d_testi, ident + ".txt"), "w", encoding="utf-8") as f:
                f.write(testo)
            voce.update(metodo=metodo, stato="ok", caratteri=len(testo),
                        pagine=(testo.count("\f") + (0 if testo.endswith("\f") else 1)) if tipo == "pdf" else None)
        registro.append(voce)
    scrivi_json(os.path.join(cartella, "registro.json"), registro)
    ok = sum(1 for v in registro if v["stato"] == "ok")
    print("Testi integrali: %d su %d file" % (ok, len(registro)))
    for v in registro:
        if v["stato"] != "ok":
            print("  - %s: %s (%s)" % (v["id"], v["stato"], v["nota"]))
    return 0


# =============================================================== confronto testuale
_SOSTITUZIONI = {"’": "'", "‘": "'", "´": "'", "`": "'", "ʼ": "'", "“": '"', "”": '"', "«": '"',
                 "»": '"', "„": '"', "–": "-", "—": "-", "‐": "-", "‑": "-", "−": "-",
                 "\u00ad": "", "\u200b": ""}


def piatto(testo):
    """Testo ridotto per il confronto, con la mappa verso le posizioni originali.
    NFKC (legature), apostrofi e virgolette uniformi, niente spazi; il trattino seguito da
    a capo (sillabazione) sparisce."""
    out, mappa = [], []
    n = len(testo)
    i = 0
    while i < n:
        ch = testo[i]
        if ch in "-‐‑" and i + 1 < n and testo[i + 1] in "\r\n":
            j = i + 1
            while j < n and testo[j].isspace():
                j += 1
            i = j
            continue
        for c in unicodedata.normalize("NFKC", _SOSTITUZIONI.get(ch, ch)):
            if not c.isspace():
                out.append(c.lower())
                mappa.append(i)
        i += 1
    return "".join(out), mappa


RE_PARAGRAFO = re.compile(r"^\s*((?:\d+\.)*\d+)\.?\s+\S|^\s*(?:par(?:agrafo)?\.?|punto)\s*((?:\d+\.)*\d+)", re.I)


def posizione(testo, inizio, tipo):
    """Pagina (PDF) o paragrafo (HTML) della posizione 'inizio' nel testo integrale."""
    if tipo == "pdf":
        return "p. %d" % (testo.count("\f", 0, inizio) + 1)
    righe = testo[:inizio].splitlines()
    for r in reversed(righe[-400:]):
        m = RE_PARAGRAFO.match(r)
        if m:
            return "par. %s" % (m.group(1) or m.group(2))
    return "testo HTML, paragrafo non numerato"


def cerca(passaggio, testo_piatto):
    q, _ = piatto(passaggio)
    q = q.strip("\"'")
    if len(q) < 12:
        return "troppo breve", []
    trovati, k = [], testo_piatto.find(q)
    while k != -1:
        trovati.append((k, len(q)))
        k = testo_piatto.find(q, k + 1)
    if trovati:
        return ("unico" if len(trovati) == 1 else "ripetuto"), trovati
    return "assente", []


# =============================================================== verifica
def parole(s):
    return len(s.split())


def valida(a, ident, fattori_def):
    err = []
    if not isinstance(a, dict):
        return ["non e' un oggetto JSON"]
    attese = {"id", "estremi", "domanda_affrontata", "risposta", "peso", "esito", "fattori",
              "passaggi", "conseguenze", "norme", "precedenti", "lacune"}
    for k in sorted(set(a) - attese):
        err.append("campo non previsto: " + k)
    for k in sorted(attese - set(a)):
        err.append("campo mancante: " + k)
    if a.get("id") != ident:
        err.append("id %r diverso dal nome del file" % a.get("id"))
    e = a.get("estremi")
    if not isinstance(e, dict):
        err.append("estremi deve essere un oggetto")
    else:
        for k in ("autorita", "organo", "tipo", "data", "numero", "parti"):
            if not isinstance(e.get(k), str) or not e.get(k).strip():
                err.append("estremi.%s mancante (scrivi 'non risulta')" % k)
        if isinstance(e.get("data"), str) and e["data"] != NON_RISULTA and not RE_DATA.match(e["data"]):
            err.append("estremi.data non in forma AAAA-MM-GG")
    for k, lim in (("domanda_affrontata", 30), ("risposta", 50)):
        v = a.get(k)
        if not isinstance(v, str) or not v.strip():
            err.append("%s vuoto" % k)
        elif parole(v) > lim:
            err.append("%s oltre %d parole" % (k, lim))
    if a.get("peso") not in PESI:
        err.append("peso deve essere uno di: " + " | ".join(PESI))
    if a.get("esito") not in ESITI:
        err.append("esito deve essere uno di: " + " | ".join(ESITI))
    for k in ("conseguenze", "norme", "precedenti", "lacune"):
        if not isinstance(a.get(k), list) or not all(isinstance(x, str) for x in a.get(k, [])):
            err.append("%s deve essere una lista di frasi" % k)
    nomi = {f["nome"]: f for f in fattori_def}
    fz = a.get("fattori")
    if not isinstance(fz, dict):
        err.append("fattori deve essere un oggetto")
        fz = {}
    for nome in nomi:
        if nome not in fz:
            err.append("fattore mancante: %s (scrivi 'non risulta')" % nome)
    for nome, val in fz.items():
        if nome not in nomi:
            err.append("fattore non previsto in fattori.json: " + nome)
        elif val != NON_RISULTA and val not in nomi[nome].get("valori", []):
            err.append("fattore %s: valore %r non previsto (ammessi: %s, oppure 'non risulta')"
                       % (nome, val, ", ".join(nomi[nome].get("valori", []))))
    ps = a.get("passaggi")
    if not isinstance(ps, list) or not ps:
        err.append("passaggi deve essere una lista non vuota")
        ps = []
    usi = set()
    for i, x in enumerate(ps, 1):
        if not isinstance(x, dict) or set(x) != {"testo", "serve_a"}:
            err.append("passaggi[%d]: servono esattamente 'testo' e 'serve_a'" % i)
            continue
        if parole(x["testo"]) > MAX_PAROLE_PASSAGGIO:
            err.append("passaggi[%d]: oltre %d parole" % (i, MAX_PAROLE_PASSAGGIO))
        if re.search(r"\[\s*\.\.\.\s*\]|\(\s*\.\.\.\s*\)|…", x["testo"]):
            err.append("passaggi[%d]: niente omissioni [...]: cita un tratto continuo" % i)
        s = x["serve_a"]
        if s not in ("risposta", "esito") and not (s.startswith("fattore:") and s[8:] in nomi):
            err.append("passaggi[%d]: serve_a deve essere 'risposta', 'esito' o 'fattore:<nome>'" % i)
        usi.add(s)
    # ancoraggio: ogni affermazione importante poggia su un passaggio
    for nome, val in fz.items():
        if nome in nomi and val != NON_RISULTA and "fattore:" + nome not in usi:
            err.append("fattore %s = %r senza un passaggio che lo regga (serve_a 'fattore:%s')" % (nome, val, nome))
    if "risposta" not in usi:
        err.append("manca un passaggio che regga la risposta (serve_a 'risposta')")
    if a.get("peso") in ("regge la decisione", "uno dei motivi") and "esito" not in usi:
        err.append("peso %r senza un passaggio sul dispositivo o sulla decisione (serve_a 'esito')" % a.get("peso"))
    return err


def cmd_verifica(cartella, opzioni):
    fdef = leggi_json(os.path.join(cartella, "fattori.json"), {}) or {}
    fattori_def = fdef.get("fattori", [])
    reg = {v["id"]: v for v in (leggi_json(os.path.join(cartella, "registro.json"), []) or [])}
    d_an = os.path.join(cartella, "analisi")
    nomi = sorted(n for n in os.listdir(d_an) if n.endswith(".json")) if os.path.isdir(d_an) else []
    lette = {r["id"] for r in leggi_candidati(cartella) if r.get("scelta") == "leggi"}
    righe, problemi, esiti_passaggi = [], [], []
    tot = trovati = 0
    for nome in nomi:
        ident = nome[:-5]
        a = leggi_json(os.path.join(d_an, nome))
        if a is None:
            problemi.append("%s: JSON non leggibile" % ident)
            continue
        for e in valida(a, ident, fattori_def):
            problemi.append("%s: %s" % (ident, e))
        pt = os.path.join(cartella, "testi", ident + ".txt")
        if not os.path.isfile(pt):
            problemi.append("%s: manca il testo integrale testi/%s.txt" % (ident, ident))
            continue
        testo = open(pt, encoding="utf-8").read()
        tp, mappa = piatto(testo)
        tipo = "pdf" if reg.get(ident, {}).get("file", "").endswith(".pdf") else "html"
        for i, x in enumerate(a.get("passaggi") or []):
            if not isinstance(x, dict) or not isinstance(x.get("testo"), str):
                continue
            tot += 1
            stato, dove = cerca(x["testo"], tp)
            pos = [posizione(testo, mappa[k], tipo) for k, _ in dove]
            esiti_passaggi.append({"id": ident, "i": i, "serve_a": x.get("serve_a"), "stato": stato,
                                   "posizione": pos[0] if len(pos) == 1 else None, "tutte": pos})
            if stato == "unico":
                trovati += 1
            elif stato == "ripetuto":
                trovati += 1
                righe.append("avviso %s passaggio %d: compare %d volte (%s): allungalo per renderlo univoco"
                             % (ident, i + 1, len(pos), ", ".join(pos)))
            else:
                problemi.append("%s passaggio %d %s nel testo integrale: \"%s\"" % (
                    ident, i + 1, "ASSENTE" if stato == "assente" else "troppo breve per verificarlo",
                    x["testo"][:160]))
    d_sc = os.path.join(cartella, "scarti")
    scarti = {n[:-4] for n in os.listdir(d_sc) if n.endswith(".txt")} if os.path.isdir(d_sc) else set()
    for i in sorted(scarti & lette):
        righe.append("avviso: %s scartato all'apertura ma ancora 'leggi' in candidati.csv: aggiorna la scelta" % i)
    mancanti = sorted(lette - {n[:-5] for n in nomi} - scarti - {i for i, v in reg.items() if v["stato"] != "ok"})
    for i in mancanti:
        problemi.append("%s scelto da leggere ma senza analisi e senza scarto" % i)
    scrivi_json(os.path.join(cartella, "verifiche.json"),
                {"analisi": len(nomi), "passaggi": tot, "trovati": trovati, "problemi": len(problemi),
                 "dettaglio": esiti_passaggi})
    testo_out = ["VERIFICA - analisi %d, passaggi ritrovati nel testo integrale %d/%d" % (len(nomi), trovati, tot), ""]
    testo_out += ["DA SISTEMARE (%d)" % len(problemi)] + ["- " + p for p in problemi] or []
    testo_out += ["", "AVVISI (%d)" % len(righe)] + ["- " + r for r in righe]
    testo_out += ["", "ESITO: " + ("in regola" if not problemi and nomi else "ci sono punti da sistemare")]
    out = "\n".join(testo_out) + "\n"
    with open(os.path.join(cartella, "verifiche.txt"), "w", encoding="utf-8") as f:
        f.write(out)
    print(out)
    return 0 if not problemi and nomi else 1


# =============================================================== campione per la seconda lettura
def cmd_campione(cartella, opzioni):
    d_an = os.path.join(cartella, "analisi")
    an = []
    for nome in sorted(os.listdir(d_an)) if os.path.isdir(d_an) else []:
        a = leggi_json(os.path.join(d_an, nome))
        if nome.endswith(".json") and isinstance(a, dict):
            an.append((nome[:-5], a))
    scelte = {}
    for i, a in an:
        if a.get("peso") == "regge la decisione":
            scelte[i] = "peso 'regge la decisione': controllare che non sia sopravvalutato"
        elif a.get("esito") in ("contrario alla tesi", "misto"):
            scelte[i] = "esito contrario o misto: e' la pronuncia che userebbe l'avversario"
        elif a.get("lacune"):
            scelte[i] = "lacune segnalate dal primo lettore"
    resto = sorted(((i, a) for i, a in an if i not in scelte),
                   key=lambda x: (0 if x[1].get("peso") in ("detto di passaggio", "solo citato") else 1,
                                  hashlib.sha256(x[0].encode()).hexdigest()))
    for i, a in resto[:min(len(resto), max(2, math.ceil(len(resto) * 0.3)))]:
        scelte[i] = "peso %r: controllare che non sia sottovalutato" % a.get("peso")
    with open(os.path.join(cartella, "seconda_lettura.txt"), "w", encoding="utf-8") as f:
        f.write("".join("%s\t%s\n" % (i, scelte[i]) for i, _ in an if i in scelte))
    print("Seconda lettura: %d analisi su %d" % (len(scelte), len(an)))
    return 0


# =============================================================== matrice
def cella(s):
    return str(s).replace("|", "/").replace("\n", " ")


def cmd_matrice(cartella, opzioni):
    fdef = leggi_json(os.path.join(cartella, "fattori.json"), {}) or {}
    fattori = [f["nome"] for f in fdef.get("fattori", [])]
    caso = fdef.get("caso", {}) or {}
    ver = leggi_json(os.path.join(cartella, "verifiche.json"), {}) or {}
    pos = {(d["id"], d["i"]): d for d in ver.get("dettaglio", [])}
    cand = {r["id"]: r for r in leggi_candidati(cartella)}
    an = []
    d_an = os.path.join(cartella, "analisi")
    for nome in sorted(os.listdir(d_an)) if os.path.isdir(d_an) else []:
        a = leggi_json(os.path.join(d_an, nome))
        if nome.endswith(".json") and isinstance(a, dict):
            an.append(a)
    an.sort(key=lambda a: (a.get("estremi", {}).get("data", ""), a.get("id", "")))
    out = ["# Matrice dei fattori", "",
           "Tesi del caso: %s" % fdef.get("tesi", "non indicata"), "",
           "## Provvedimenti e fattori", ""]
    intest = ["Data", "id", "Fonte", "Autorità"] + fattori + ["Peso del tema", "Esito per la tesi"]
    out.append("| " + " | ".join(intest) + " |")
    out.append("|" + "---|" * len(intest))
    for a in an:
        e = a.get("estremi", {})
        out.append("| " + " | ".join(cella(x) for x in
                   [e.get("data", ""), a.get("id"), cand.get(a.get("id"), {}).get("fonte", ""), e.get("autorita", "")]
                   + [a.get("fattori", {}).get(f, "") for f in fattori] + [a.get("peso"), a.get("esito")]) + " |")
    out += ["", "## Ogni valore dei fattori, con gli esiti", "",
            "Conta solo le pronunce lette; non e' una statistica sulla prassi.", ""]
    for f in fattori:
        valori = {}
        for a in an:
            v = a.get("fattori", {}).get(f, NON_RISULTA)
            valori.setdefault(v, []).append(a)
        out.append("**%s**" % f)
        for v, gruppo in sorted(valori.items(), key=lambda x: (x[0] == NON_RISULTA, x[0])):
            conta = {}
            for a in gruppo:
                conta.setdefault(a.get("esito"), []).append(a.get("id"))
            out.append("- %s: " % v + "; ".join("%s %d (%s)" % (k, len(ids), ", ".join(ids)) for k, ids in sorted(conta.items())))
        out.append("")
    if caso:
        out += ["## Vicinanza al caso", "",
                "Fattori del caso: " + "; ".join("%s = %s" % (k, v) for k, v in caso.items()), "",
                "| id | Fattori uguali al caso | Fattori diversi | Non risulta | Esito per la tesi |",
                "|---|---|---|---|---|"]
        righe = []
        for a in an:
            fz = a.get("fattori", {})
            ug = [k for k, v in caso.items() if fz.get(k) == v]
            nr = [k for k in caso if fz.get(k, NON_RISULTA) == NON_RISULTA]
            dv = [k for k in caso if k not in ug and k not in nr]
            righe.append((len(ug), -len(dv), a, ug, dv, nr))
        for n, _, a, ug, dv, nr in sorted(righe, key=lambda x: (-x[0], x[1], x[2].get("id"))):
            out.append("| %s | %d (%s) | %s | %s | %s |" % (a.get("id"), n, ", ".join(ug) or "-",
                       ", ".join(dv) or "-", ", ".join(nr) or "-", a.get("esito")))
        out.append("")
    out += ["## Passaggi verificati, con la loro posizione", "",
            "Posizione calcolata dal programma nel testo integrale (pagina per i PDF, paragrafo per le pagine web).", ""]
    for a in an:
        out.append("**%s**" % a.get("id"))
        for i, x in enumerate(a.get("passaggi", [])):
            d = pos.get((a.get("id"), i), {})
            dove = d.get("posizione") or ("; ".join(d.get("tutte", [])) if d.get("tutte") else "NON VERIFICATO")
            out.append("- [%s] «%s» (%s)" % (x.get("serve_a"), x.get("testo"), dove))
        out.append("")
    with open(os.path.join(cartella, "matrice.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print("Scritta matrice.md: %d provvedimenti, %d fattori" % (len(an), len(fattori)))
    return 0


# =============================================================== BDP
RE_BDP = re.compile(r"^(?P<tipo>[A-Z]+)_(?P<uff>.+?)(?:_N\._(?P<pn>\d+)_(?P<pa>\d{4}))?_-_N\._R\.G\._(?P<n>\d+)_(?P<a>\d{4})"
                    r"(?:_DEPOSITO_MINUTA_(?P<dep>\d\d_\d\d_\d{4}))?(?:_+PUBBLICAZIONE_(?P<pub>\d\d_\d\d_\d{4}))?"
                    r"(?:\s*\(\d+\))?\.pdf$", re.I)


def cmd_importa_bdp(cartella, opzioni):
    if not opzioni:
        print("Serve la cartella con i PDF della BDP")
        return 2
    src = os.path.abspath(os.path.expanduser(opzioni[0]))
    righe = leggi_candidati(cartella)
    usati = {r["id"] for r in righe}
    os.makedirs(os.path.join(cartella, "fonti"), exist_ok=True)
    nuovi, ignoti = 0, []
    for nome in sorted(os.listdir(src)):
        m = RE_BDP.match(nome)
        if not nome.lower().endswith(".pdf"):
            continue
        if not m:
            ignoti.append(nome)
            continue
        base = "bdp-%d-%s" % (int(m.group("n")), m.group("a"))
        ident, k = base, 2
        while ident in usati:
            ident, k = "%s-%d" % (base, k), k + 1
        usati.add(ident)
        g = lambda s: "%s-%s-%s" % (s[6:], s[3:5], s[:2]) if s else ""
        uff = " ".join(m.group("uff").replace("_", " ").split()).title().replace(" Di ", " di ")
        righe.append({"id": ident, "fonte": "bdp", "autorita": uff, "tipo": m.group("tipo").lower(),
                      "data": g(m.group("pub")) or g(m.group("dep")),
                      "numero": ("n. %d/%s, " % (int(m.group("pn")), m.group("pa")) if m.group("pn") else "")
                                + "R.G. %d/%s" % (int(m.group("n")), m.group("a")), "titolo": nome,
                      "url_pagina": "", "url_documento": "", "formato": "pdf", "scelta": "leggi",
                      "nota": "Banca Dati di Merito, accesso dell'utente"})
        shutil.copy2(os.path.join(src, nome), os.path.join(cartella, "fonti", ident + ".pdf"))
        nuovi += 1
    scrivi_candidati(cartella, righe)
    print("Importati dalla BDP: %d; nomi non riconosciuti: %d" % (nuovi, len(ignoti)))
    for n in ignoti:
        print("  - " + n)
    return 0


def cmd_memo(cartella, opzioni):
    nome = opzioni[0] if opzioni else "memo.md"
    p = os.path.join(cartella, nome)
    if not os.path.isfile(p):
        print("File non trovato: %s" % p)
        return 2
    d = os.path.join(cartella, "testi")
    testi = {n[:-4]: piatto(open(os.path.join(d, n), encoding="utf-8").read())[0]
             for n in sorted(os.listdir(d)) if n.endswith(".txt")} if os.path.isdir(d) else {}
    frasi = re.findall(r"«([^»]+)»", open(p, encoding="utf-8").read())
    mancanti = []
    for f in frasi:
        dove = [i for i, t in testi.items() if cerca(f, t)[0] in ("unico", "ripetuto")]
        if not dove:
            mancanti.append(f)
    print("Frasi tra «» nel memo ritrovate nei testi integrali: %d/%d" % (len(frasi) - len(mancanti), len(frasi)))
    for f in mancanti:
        print("  NON TROVATA: «%s»" % f)
    return 1 if mancanti else 0


COMANDI = {"scarica": cmd_scarica, "testi": cmd_testi, "campione": cmd_campione,
           "verifica": cmd_verifica, "matrice": cmd_matrice, "memo": cmd_memo, "importa-bdp": cmd_importa_bdp}


def main(argv):
    if len(argv) < 3 or argv[1] not in COMANDI:
        print(__doc__)
        return 2
    cartella = os.path.abspath(os.path.expanduser(argv[2]))
    if not os.path.isdir(cartella):
        print("Cartella della ricerca non trovata: %s" % cartella)
        return 2
    return COMANDI[argv[1]](cartella, argv[3:])


if __name__ == "__main__":
    sys.exit(main(sys.argv))
