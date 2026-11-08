---
name: bdp-ricerca
description: Ricerca e download automatizzato di giurisprudenza di merito sulla Banca Dati di Merito (BDP) del Ministero della Giustizia (https://bdp.giustizia.it). Si attiva ogni volta che l'utente chiede di "cercare su BDP", "ricerca su Banca Dati di Merito", "scaricare sentenze/ordinanze/decreti di un tribunale", "trovare giurisprudenza di merito su [tema]", "cerca pronunce di merito", "BDP giustizia", "bdp.giustizia.it", oppure menziona Tribunale/Corte di Appello + materia + necessità di reperire provvedimenti. Attivare anche con varianti come "cerca le ordinanze del Trib. di Milano su X", "trovami le sentenze del Trib. di Roma in materia Y", "scarica i provvedimenti di merito su Z". NON attivare per Cassazione (banca dati separata), né per giurisprudenza amministrativa (TAR/CdS), né per dottrina. Richiede l'estensione Claude in Chrome attiva e l'utente loggato su BDP.
---

# Ricerca BDP — Banca Dati di Merito

Questa skill replica il flusso operativo testato per cercare, scaricare e classificare provvedimenti giurisdizionali sulla **Banca Dati di Merito** del Ministero della Giustizia. È un database accessibile solo via login (SPID/CIE/credenziali Giustizia) e con accesso vincolato al browser dell'utente: per questo serve l'estensione **Claude in Chrome**, che eredita la sessione del browser locale.

L'obiettivo è risparmiare all'utente la navigazione manuale (form complesso, autocomplete capricciosi, download uno-per-uno) e produrre alla fine una cartella organizzata con i PDF e, se richiesto, una classificazione di pertinenza.

---

## Fase 0 — Pre-requisiti tecnici (non saltare)

Prima di iniziare, **verifica sempre**:

1. **Estensione Claude in Chrome installata e collegata**.
   - Esegui `mcp__Claude_in_Chrome__list_connected_browsers`.
   - Se ritorna `[]`, ferma tutto e guida l'utente a:
     - Installare l'estensione da `claude.ai/chrome` (serve piano Max/Pro).
     - Fare login con lo stesso account Anthropic.
   - Se ritorna un browser, esegui `select_browser` con il `deviceId`.

2. **Utente loggato su BDP nel suo Chrome**.
   - I cookie di Chrome sono condivisi a livello di profilo, quindi se l'utente ha fatto l'accesso in una qualunque tab, anche la tab MCP isolata erediterà la sessione.
   - Chiedi all'utente di andare su `https://bdp.giustizia.it/login` e fare il login con SPID/CIE/credenziali Giustizia **prima** di proseguire.

3. **Auto-download abilitato in Chrome** (necessario solo se si dovranno scaricare PDF).
   - L'utente deve aprire `chrome://settings/downloads` e **disattivare** il toggle "Chiedi dove salvare ogni file prima di scaricarlo".
   - Senza questa modifica, Chrome chiede conferma per ogni singolo download (impraticabile con N file).
   - I file verranno scaricati in `~/Downloads`, poi vanno spostati nella cartella di destinazione.

4. **Cartella di destinazione**. Chiedere all'utente dove vuole i file (default suggerito: `~/Desktop/sentenze/` o sotto-cartella tematica). Creare la cartella con `mkdir -p` se non esiste.

**Non procedere finché tutti i pre-requisiti non sono soddisfatti.** Se mancano, chiedi con `AskUserQuestion` o fermati a istruire l'utente.

---

## Fase 1 — Raccolta parametri di ricerca

Chiedi (o inferisci dalla richiesta) **questi parametri prima di toccare il browser**:

| Parametro | Valori possibili | Note |
|---|---|---|
| **Tipo provvedimento** | SENTENZA / ORDINANZA / DECRETO / TUTTI | Default: TUTTI se non specificato |
| **Distretto** | Uno dei 26 distretti di Corte di Appello (Milano, Roma, Napoli, …) | Obbligatorio se l'utente cita un tribunale specifico |
| **Ufficio** | Tribunale / Corte di Appello / Tribunale per i Minorenni | Dipende dal Distretto, le opzioni si caricano dinamicamente |
| **Periodo** | Data pubblicazione "da"/"a" (formato gg/mm/aaaa) | "Ultimi N anni" → calcola da oggi |
| **Riferimento normativo** | Solo se l'utente lo richiede esplicitamente | **⚠️ Vedi nota critica sotto** |
| **Materia** | Una delle ~70 voci predefinite | Spesso troppo restrittiva: usare con cautela |
| **Parola chiave** | Tag descrittivo associato dal classificatore | Diverso dal "Testo" |
| **Testo** | Ricerca full-text nelle motivazioni anonimizzate | **Strumento principale per cercare temi/articoli** |
| **Tipo ricerca testuale** | ALMENO UNA PAROLA / TUTTE LE PAROLE / FRASE ESATTA | Default: ALMENO UNA PAROLA |
| **Giudice/Presidente/Relatore** | Nome del magistrato | Solo se richiesto |

### ⚠️ Nota critica sulla ricerca per riferimento normativo

Il campo **"Riferimento normativo"** ha un autocomplete che **NON è esaustivo**: per molti articoli del codice civile (verificato: art. 1384 c.c.) l'autocomplete non restituisce suggerimenti pertinenti perché il classificatore della BDP non indicizza sistematicamente quel riferimento.

**Regola operativa**: se l'utente cerca pronunce su un articolo specifico, **usa SEMPRE il campo "Testo"** con il numero dell'articolo (es. "1384") in modalità "ALMENO UNA PAROLA". Non fidarti dell'autocomplete del campo Riferimento normativo. Il trade-off è che si avranno alcuni falsi positivi (numeri di RG, importi, ID che contengono la stringa), gestibili in fase di triage (Fase 4).

---

## Fase 2 — Compilazione del form e ricerca

Esegui questi step **in sequenza** (le combobox sono dipendenti, devi rispettare l'ordine):

1. **Apri/usa una tab MCP** con `tabs_context_mcp` (createIfEmpty: true).

2. **Naviga** alla home BDP: `https://bdp.giustizia.it/`.

3. **Verifica sessione**: leggi la pagina (`read_page`). Se vedi il nome dell'utente loggato nell'header, ok. Altrimenti torna alla Fase 0.

4. **Compila i filtri dropdown con `form_input`** in quest'ordine:
   - Tipo (ref del combobox "TUTTI" iniziale)
   - Distretto (es. "MILANO")
   - **Pausa e rileggi**: l'Ufficio si popola dinamicamente in base al Distretto. Rileggi la pagina (`read_page` con `ref_id` del combobox Ufficio) per vedere le opzioni disponibili.
   - Ufficio (es. "TRIBUNALE DI MILANO")

5. **Compila la ricerca testuale** (se richiesta):
   - Usa `form_input` sul campo "Testo" (textbox) — **non** il tipo `type` action, che ha problemi di focus.
   - Il dropdown "Tipo ricerca testuale" di solito non va toccato (default "ALMENO UNA PAROLA").

6. **Imposta le date di pubblicazione**:
   - I campi data sono **pulsanti** che aprono un date picker, non textbox.
   - Strategia:
     - `find` "Data di pubblicazione da button" → ottieni il ref → `left_click`.
     - Si apre un calendar widget con dropdown "Mese" e "Anno".
     - `find` "year selector in date picker" → `form_input` con l'anno desiderato.
     - Se serve cambiare mese, usa le frecce `<` `>` accanto al nome del mese (o clicca il dropdown mese).
     - **Clicca il giorno** con `computer left_click` sulle coordinate del numero. Attenzione: i giorni sono piccoli e ravvicinati, una piccola imprecisione clicca il giorno sbagliato. Se serve precisione assoluta, fai uno screenshot prima e zooma.
   - Ripeti per "Data di pubblicazione a".
   - Se l'utente dice "ultimi N anni", calcola: `da = oggi - N anni`, `a = oggi`.

7. **Clicca "Ricerca"** (`find` "Ricerca submit button" → `left_click`).

8. **Verifica il risultato**: aspetta 3 secondi, poi leggi la pagina o fai screenshot. Cerca il testo "**N Risultati**" in alto alla lista.

### Quando troppi risultati

Se il numero di risultati è > 50, **fermati** e proponi all'utente di restringere:
- Periodo più stretto
- Materia più specifica
- Parola chiave aggiuntiva nel campo Testo

Scaricare 50+ PDF è un'operazione lunga; meglio raffinare prima.

### Quando zero risultati

Se 0 risultati, prova in quest'ordine:
1. Allarga il periodo (es. da 2 a 5 anni).
2. Rimuovi filtro Materia se presente.
3. Cambia tipo provvedimento (es. da ORDINANZA a TUTTI).
4. Riprova con sinonimi nel campo Testo.

---

## Fase 3 — Apertura e download dei provvedimenti

Ogni risultato ha 4 azioni: **Organizza** (cartelle BDP), **Mostra** (anteprima), **Apri** (pagina dettaglio), **Altre azioni**.

### URL pattern (essenziale per l'iterazione)

Quando si clicca "Apri" sul primo risultato, l'URL diventa:

```
https://bdp.giustizia.it/provvedimento/page?from=0&size=1&area=CIVILE&target=provvedimento&sort_field=_score&sort_order=desc&q=<query>
```

**Il parametro `from=N` permette di navigare tra i risultati cambiando N da 0 a (totale-1)**. Conserva la query URL completa dopo aver cliccato "Apri" sul primo risultato — userai quella come template.

### Meccanismo di download (importante)

Il pulsante **"Scarica"** NON scarica da un endpoint server: genera il PDF **lato client via JavaScript** (blob URL tipo `blob:https://bdp.giustizia.it/<uuid>`). Conseguenze:

- Non si può fare `curl` o `fetch` lato server — bisogna passare per il click.
- Ogni click triggera un download blob in Chrome.
- Se "Chiedi dove salvare" è attivo, Chrome aspetta conferma → file resta come `.com.google.Chrome.XXXX` nascosto in `~/Downloads`. **Per questo serve la Fase 0 punto 3**.

### Loop di download

Per ogni N da 0 a (totale-1):

1. **Navigate** al template URL con `from=N`.
2. **Wait** 3 secondi (la pagina carica via JS, deve renderizzare i pulsanti).
3. **Find** "Scarica provvedimento button" → ottieni il ref.
4. **Left_click** sul ref.
5. **Wait** 2 secondi per il download.

Il `ref` del pulsante Scarica tende a restare stabile (es. `ref_79`) tra navigazioni successive sulla stessa tab — puoi riusarlo, ma se diventa stale ri-esegui `find`.

### Checkpoint progressivi

Ogni ~5 download, esegui un Bash per verificare:

```bash
find "$HOME/Downloads" -name "ORDINANZA*.pdf" -newer /tmp/bdp_start_ts | wc -l
```

(Prima del loop, registra il timestamp di partenza: `date +%s > /tmp/bdp_start_ts`.)

Se il conteggio non avanza come previsto, fermati e indaga (probabile reset del setting di Chrome, o estensione che blocca).

### Naming dei file

BDP nomina i file come:
```
<TIPO>_<UFFICIO>_-_N._R.G._<numero>_<anno>_DEPOSITO_MINUTA_<gg_mm_aaaa>__PUBBLICAZIONE_<gg_mm_aaaa>.pdf
```

Esempio: `ORDINANZA_TRIBUNALE_DI_MILANO_-_N._R.G._00004147_2025_DEPOSITO_MINUTA_03_03_2025__PUBBLICAZIONE_03_03_2025.pdf`.

Non rinominare i file: il formato è utile per parsing successivo (RG, ufficio, date).

### Spostamento finale

Dopo aver scaricato tutto, sposta in batch dalla cartella Downloads alla cartella di destinazione:

```bash
find "$HOME/Downloads" -maxdepth 1 -name "<TIPO>_<UFFICIO>*.pdf" -newer /tmp/bdp_start_ts -exec mv {} "<DEST>/" \;
```

Verifica il conteggio finale.

---

## Fase 4 — Triage di pertinenza (opzionale, su richiesta)

Quando si usa la ricerca full-text con un numero (es. "1384"), ci saranno **falsi positivi** (numeri di sentenze citate, RG, importi). Il triage filtra questi.

**Solo se l'utente lo richiede esplicitamente** o se proponi tu il triage e l'utente accetta, esegui questo workflow:

1. Verifica che `pypdf` sia installato in Python3: `python3 -c "import pypdf"`. Se no: `pip3 install --quiet pypdf`.

2. Scrivi uno script Python in `/tmp/triage_<topic>.py` che:
   - Apre ogni PDF nella cartella di destinazione.
   - Estrae il testo via `pypdf`.
   - Cerca pattern regex per il **vero** riferimento (es. `art\.?\s*1384\s*(c\.?c\.?|cod\.?\s*civ\.?)`) — adatta i pattern al tema della ricerca.
   - Cerca parole chiave di contesto (es. "riduzione della penale", "manifestamente eccessiva").
   - Classifica in 4 categorie:
     - **PERTINENTE** — l'articolo è citato esplicitamente nella forma giusta.
     - **PROBABILMENTE PERTINENTE** — concetti pertinenti ma senza citazione esplicita.
     - **NON PERTINENTE** — il numero compare ma per altre ragioni.
     - **NON PRESENTE** — il numero non compare affatto (sospetto: file corrotto).
   - Stampa per ogni categoria: RG, data pubblicazione, file, occorrenze, estratti del contesto (50-150 caratteri prima/dopo).

3. Esegui lo script e mostra l'output organizzato.

4. **Sposta i non pertinenti** in una sotto-cartella `non_pertinenti/`:

```bash
mkdir -p "<DEST>/non_pertinenti"
mv "<DEST>/<file_non_pertinente>.pdf" "<DEST>/non_pertinenti/"
```

5. Mostra all'utente:
   - Conteggio finale pertinenti vs. non pertinenti.
   - Per i pertinenti, raggruppa per "filone" (materia, ratio comune) e produci un mini-indice tematico con suggerimenti su quali aprire.

---

## Fase 5 — Output finale all'utente

Concludi sempre con:

1. **Path della cartella** con link cliccabile in stile markdown: `[~/Desktop/sentenze/](sentenze)`.
2. **Conteggio per categoria** (totale, pertinenti, non pertinenti se hai fatto triage).
3. **Sintesi dei filoni** emersi (max 3-4 raggruppamenti tematici).
4. **Avvertenza sui limiti** della ricerca BDP:
   - Solo provvedimenti pubblicati con consenso dei magistrati.
   - Anonimizzati (nomi sostituiti con `Parte_1`, `CP_1`, ecc.).
   - L'autocomplete del campo "Riferimento normativo" non è esaustivo.
5. **Proposte di follow-up**:
   - Sintesi delle massime delle 2-3 più rilevanti.
   - Indice ragionato salvato in `indice.md` nella cartella.
   - Ricerca cross-distretto sullo stesso tema.

---

## Errori comuni e troubleshooting

| Sintomo | Causa probabile | Rimedio |
|---|---|---|
| `list_connected_browsers` ritorna `[]` | Estensione Claude in Chrome non installata o non loggata | Fase 0 punto 1 |
| Pagina BDP mostra schermata di login | Sessione utente scaduta | Chiedi all'utente di rifare login nel suo Chrome |
| Solo "4" nel campo Testo dopo aver typato "1384" | Focus perso tra le battute | Usa `form_input` invece di `computer type` |
| Date picker apre sull'anno corrente, clic sbagliato | Click su giorno sbagliato (1 al posto di 15) | Usa `scroll_to ref` se possibile; controlla con screenshot dopo |
| Download non parte (no file in Downloads) | "Ask where to save" ancora attivo | Verifica `chrome://settings/downloads` |
| Stesso file scaricato 2 volte | Click ripetuto durante test | Filtra duplicati con `sort | uniq` sui nomi |
| Autocomplete del Riferimento normativo non trova l'articolo | Indicizzazione incompleta del classificatore BDP | Usa il campo Testo, non Riferimento normativo |
| `ref_NNN` diventa stale dopo click | Pagina re-renderizzata | Riesegui `find` |

---

## Note di stile per l'esecuzione

- **Annuncia ogni fase** all'utente con una frase prima dei tool call.
- **Aggiorna TodoWrite** appena hai più di 3 step (è quasi sempre il caso qui).
- **Non fare 19 conferme** all'utente: chiedi una volta per il batch all'inizio.
- **Se la ricerca produce >50 risultati**, fermati e proponi raffinazioni invece di scaricare tutto.
- **Rispetta la privacy**: i documenti sono già anonimizzati da BDP, ma non condividerne il contenuto fuori dalla conversazione (no upload a terzi, no copie su cloud) senza autorizzazione.
- **Non bypassare i meccanismi di sicurezza Chrome/Anthropic**: l'auto-download è una preferenza che l'utente deve impostare manualmente, non si forza via JS.
