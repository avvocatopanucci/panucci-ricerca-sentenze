# Panucci ricerca sentenze

**Una skill per Claude che cerca i precedenti utili a un caso concreto, nelle fonti aperte e nelle banche dati con accesso riservato, e consegna un memo in cui ogni citazione è stata ritrovata da un programma nel testo originale del provvedimento.**

Ideata dall'Avv. Giovanna Panucci, novembre 2026. Gratuita, con licenza MIT: potete usarla e modificarla citando l'autrice.

> **Non serve saper programmare.** Questa pagina è scritta per avvocati, non per tecnici. Seguite i passi nell'ordine: la prima volta servono circa venti minuti, poi una ricerca si avvia con una frase.

---

## In breve: che cosa fa

1. **Parte dal vostro caso.** Voi descrivete i fatti, senza nomi, e la tesi da sostenere. La skill costruisce la ricerca intorno a questi, cercando anche la tesi contraria.
2. **Cerca e scarica i provvedimenti.**
   - Dalle fonti aperte (oggi: Garante privacy, EDPB) li scarica direttamente.
   - Dalla Banca Dati di Merito lavora nel **vostro** Chrome, dove l'accesso con SPID lo fate voi.
3. **Li legge solo sul testo integrale.** Ogni frase citata viene ritrovata da un programma nel documento originale, con la sua pagina o il suo paragrafo. Se non si trova, non passa.
4. **Costruisce una matrice dei fattori**: quali fatti hanno portato a quale esito, e quali precedenti somigliano di più al vostro caso.
5. **Attacca il proprio lavoro** prima di consegnarlo. Un revisore separato legge il memo da avversario, da giudice e da verificatore.
6. **Verifica le norme** con LexItalia 2.0 su Normattiva, se l'avete.

---

## I pezzi, in una mappa

Sono tre pezzi, ma **per cominciare ne serve uno solo**.

| Pezzo | A che cosa serve | Serve? |
|---|---|---|
| **Panucci ricerca sentenze** | La skill principale: il metodo di ricerca. Da sola lavora già sulle fonti aperte. | Sempre |
| **bdp-ricerca** | La skill che sa muoversi nella Banca Dati di Merito | Solo per la BDP |
| **LexItalia 2.0** | Verifica le norme su Normattiva e mette i link | Facoltativo |

A questi si aggiunge l'estensione **Claude in Chrome**, che serve solo per le banche dati con accesso riservato.

---

## Che cosa vi serve

| Che cosa | Perché | Serve sempre? |
|---|---|---|
| Un **Mac** | La skill è stata provata su Mac; su Windows non è stata provata. | Sì |
| Un abbonamento a **Claude** (Pro o Max) e l'**app desktop di Claude** | La skill lavora nella sezione **Code** dell'app desktop, che può salvare file sul computer. Nella normale chat del sito non funziona. | Sì |
| **Google Chrome** con l'estensione **Claude in Chrome** | Far lavorare Claude nel vostro browser, dove l'accesso lo fate voi | Solo per la BDP |
| Il vostro **accesso alla Banca Dati di Merito** (SPID, CIE o credenziali Giustizia) | Entrare nella BDP | Solo per la BDP |
| **LexItalia 2.0** | Link verificati alle norme | No |

---

## Passo 1: scaricare le skill

Non serve un account GitHub. Cliccate sui link: ognuno scarica un file nella cartella **Download** del Mac.

1. **[Scarica Panucci ricerca sentenze](https://github.com/avvocatopanucci/panucci-ricerca-sentenze/raw/main/pacchetti/panucci-ricerca-sentenze.skill)**: il file si chiama `panucci-ricerca-sentenze.skill`.
2. **[Scarica bdp-ricerca](https://github.com/avvocatopanucci/panucci-ricerca-sentenze/raw/main/pacchetti/bdp-ricerca.skill)**, solo se userete la Banca Dati di Merito: il file si chiama `bdp-ricerca.skill`.

Non aprite e non rinominate i file.

Se i link non funzionano: in questa pagina aprite la cartella `pacchetti`, cliccate sul nome del file e usate il pulsante con la freccia verso il basso in alto a destra ("Download raw file").

## Passo 2: installare le skill in Claude

1. Aprite Claude e andate nelle **Impostazioni**: cliccate sul vostro nome o sulle iniziali, in basso a sinistra.
2. Cercate la sezione **Skill**, di solito sotto **Funzionalità** (*Capabilities*). I nomi possono cambiare leggermente con gli aggiornamenti.
3. Cliccate **Carica skill** (*Upload skill*) e scegliete `panucci-ricerca-sentenze.skill` dalla cartella Download.
4. Se serve, ripetete con `bdp-ricerca.skill`.
5. Controllate che le skill siano **attive**: c'è un interruttore accanto a ciascuna.

Se Claude vi chiede di attivare l'esecuzione di codice o la creazione di file, attivatela.

## Passo 3 (solo per la Banca Dati di Merito): Claude in Chrome

1. In Chrome andate su **[claude.ai/chrome](https://claude.ai/chrome)**, installate l'estensione e fate l'accesso con **lo stesso account** di Claude.
2. **Tocca a voi, un'impostazione:** scrivete `chrome://settings/downloads` nella barra degli indirizzi e disattivate **"Chiedi dove salvare ogni file prima di scaricarlo"**.

   Altrimenti Chrome apre una finestra per ogni sentenza e la ricerca si ferma. I file finiscono in Download e la skill li sposta da sola. A ricerca finita potete riattivare l'opzione.
3. **Tocca a voi, l'accesso alla BDP.** Non adesso: durante la ricerca Claude apre la BDP in una scheda nuova del vostro Chrome e, se trova la pagina di accesso, si ferma. Entrate voi con SPID, CIE o credenziali Giustizia e scrivete "fatto". Claude non vede e non digita mai le credenziali.

## Passo 4 (facoltativo): LexItalia 2.0

Se avete già LexItalia 2.0, la skill lo trova da sola. Se non l'avete, funziona lo stesso: cita le norme senza link e lo dichiara nel memo.

## Passo 5: la prima ricerca

**Dove.** Aprite l'**app desktop di Claude**, sezione **Code**, e avviate una nuova sessione. Se vi chiede una cartella, scegliete Documenti.

**Che cosa scrivere.** Il caso senza nomi né dati identificativi, e la tesi. Iniziare con "Usa Panucci ricerca sentenze" garantisce che Claude usi questa skill.

> **Solo fonti aperte.** *Usa Panucci ricerca sentenze. Il caso: un'azienda ha inviato SMS promozionali ai propri clienti senza consenso, sostenendo di avere un legittimo interesse. Vorrei capire se questa tesi regge. Cerca sul Garante privacy e sull'EDPB negli ultimi tre anni.*

> **Solo Banca Dati di Merito.** *Usa Panucci ricerca sentenze. Il caso: un'impresa ha consegnato i lavori con 40 giorni di ritardo, e la penale prevista in contratto è pari a un terzo del prezzo. Vorrei sostenere che la penale è manifestamente eccessiva e va ridotta. Cerca nella Banca Dati di Merito, leggi 5 sentenze.*

**Che cosa succede, e chi fa che cosa.**

| Momento | Chi | Che cosa fare |
|---|---|---|
| Claude fa **una domanda** sui dati mancanti (fonti, periodo, quanti provvedimenti, cartella) | Voi | Rispondete o accettate le proposte. Per cominciare, 5 provvedimenti bastano. |
| Il Mac propone di installare gli **"strumenti per sviluppatori"** (solo la prima volta, se mancano) | Voi | Accettate: è un'installazione gratuita di Apple. |
| Claude chiede il **permesso** di eseguire un comando o creare file; il Mac chiede l'accesso a Documenti | Voi | Consentite: servono a scaricare e leggere i provvedimenti. |
| Ricerca e scaricamento dalle fonti aperte | Claude | Aspettate. |
| Solo BDP: Claude si ferma sulla pagina di accesso della BDP | Voi | Fate l'accesso e scrivete "fatto"; se c'è un captcha, risolvetelo voi. |
| Lettura, verifica, seconda lettura, prova di resistenza | Claude | Aspettate. |
| Consegna: Claude dice dove si trova il memo, la risposta in una frase e i limiti | Voi | Leggete il memo. |

**Quanto ci vuole.** Nelle prove, da mezz'ora a un'ora a seconda di quanti provvedimenti si leggono. Non chiudete l'app e non mettete il Mac in stop.

## Che cosa trovate alla fine

Una cartella in **Documenti → Ricerche**, con il nome del tema.

| File o cartella | Che cos'è |
|---|---|
| `memo.md` | **Il risultato**: risposta, precedenti più vicini, precedenti contrari, limiti, nota sulle norme |
| `fonti/` | I provvedimenti scaricati |
| `matrice.md` | La tabella dei fattori e i passaggi citati con pagina o paragrafo |
| `prova_di_resistenza.md` | Le obiezioni del revisore e come sono state risolte |
| `caso.md` | Il caso e le ricerche fatte, con il numero di risultati |

Per aprire `memo.md`: tasto destro → **Apri con → TextEdit**. Oppure chiedete a Claude: *"Trasforma il memo in un documento Word"*.

---

## Domande frequenti

**Devo saper programmare?** No. I comandi tecnici li esegue Claude, dopo avervi chiesto il permesso.

**Quanto costa?** La skill è gratuita. Serve un abbonamento a Claude. Una ricerca completa consuma una parte dei limiti di utilizzo del vostro piano, più di una conversazione normale: per cominciare, leggete pochi provvedimenti.

**Funziona su Windows?** Non è stata provata.

**Funziona nella chat di claude.ai, dal browser?** No: deve salvare file sul computer, e lo fa l'app desktop nella sezione Code.

**Posso usarla senza la Banca Dati di Merito?** Sì. Senza la BDP non servono né bdp-ricerca né Claude in Chrome.

**E le altre banche dati, comprese quelle a pagamento?** Oggi le fonti pronte sono Garante privacy, EDPB e Banca Dati di Merito. Per una fonte nuova la skill prima prova il sito e poi vi chiede se salvarne la descrizione. Per le banche dati in abbonamento controllate prima le condizioni del contratto. La skill, davanti a contenuti riservati, si ferma e vi chiede il permesso.

**E i dati del cliente?** Descrivete il caso senza nomi né dati identificativi. I provvedimenti scaricati restano nella cartella sul vostro Mac. Il loro testo viene letto da Claude, come qualsiasi documento che gli fate leggere.

**Posso fidarmi del memo?** Ogni frase tra virgolette è stata ritrovata da un programma nel testo originale, con la sua pagina. Ma il memo ragiona su un campione di provvedimenti e lo dichiara: la lettura e la strategia restano vostre.

**Come aggiorno la skill?** Riscaricate i file del passo 1 e caricateli come nel passo 2, al posto dei vecchi.

**Uso già Claude Code dal Terminale.** Scaricate il progetto (pulsante verde *Code → Download ZIP*) e copiate le cartelle `panucci-ricerca-sentenze` e `bdp-ricerca` in `~/.claude/skills/`.

## Se qualcosa non va

| Cosa succede | Cosa fare |
|---|---|
| Claude non sembra usare la skill | Iniziate con *"Usa Panucci ricerca sentenze"* e controllate che la skill sia attiva (passo 2). |
| Claude in Chrome non risulta collegato | Verificate che l'estensione sia installata e collegata allo stesso account di Claude (passo 3). |
| Chrome chiede dove salvare ogni sentenza | Disattivate "Chiedi dove salvare ogni file prima di scaricarlo" (passo 3). |
| La BDP chiede di nuovo l'accesso | Rifate l'accesso nella scheda aperta da Claude e scrivete "fatto". |
| Compare un captcha | Risolvetelo voi, poi scrivete "fatto". |
| Un sito non permette lo scaricamento automatico | È previsto: Claude vi dà i link da aprire a mano. |
| Un provvedimento è "senza testo" | È una scansione: viene escluso e dichiarato nel memo. |

**Segnalazioni:** per errori e suggerimenti usate la pagina **[Issues](https://github.com/avvocatopanucci/panucci-ricerca-sentenze/issues)** (serve un account GitHub gratuito). Spiegate che cosa avete chiesto e che cosa è successo, e copiate il messaggio di Claude.

---

## Regole d'uso

- **Accessi e blocchi.** Login, SPID e captcha restano dell'utente. La skill non digita credenziali, non aggira blocchi e rispetta le regole dei siti (robots.txt).
- **Banche dati a pagamento.** Prima di farci lavorare l'IA, verificate che le condizioni d'uso del vostro abbonamento lo consentano.
- **Uso mirato.** Pochi provvedimenti utili al caso, uno alla volta: non è uno strumento per copiare banche dati.
- **Il memo non sostituisce la lettura dell'avvocato.**

## Contenuto del progetto (per chi è curioso)

| Cartella | Che cos'è |
|---|---|
| `pacchetti/` | Le due skill pronte da installare |
| `panucci-ricerca-sentenze/` | La skill principale: istruzioni, profili delle fonti, il programma `strumenti/sentenze.py` |
| `bdp-ricerca/` | La skill per la Banca Dati di Merito |
| `prove/` | Le prove automatiche del programma (`python3 -B -m unittest discover -s prove -v`) |

**Stato:** provata su ricerche complete con Garante privacy, EDPB e Banca Dati di Merito (novembre 2026), su Mac, nell'app desktop di Claude.

**Licenza:** MIT, vedi `LICENSE`.
