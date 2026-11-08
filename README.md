# Panucci ricerca sentenze

Skill per Claude che cerca precedenti utili a un caso concreto, dalle fonti aperte alle banche dati ad accesso riservato, e consegna un memo in cui ogni citazione è stata ritrovata da un programma nel testo originale del provvedimento.

Ideata dall'Avv. Giovanna Panucci (novembre 2026). Licenza MIT: uso e modifica liberi, citando l'autrice.

> **Stato: versione di prova.** Provata su ricerche complete con Garante privacy, EDPB e Banca Dati di Merito (novembre 2026). Le altre fonti si aggiungono con il loro profilo.

## Che cosa fa

1. **Parte dal caso.** Fatti del cliente, tesi da sostenere e fattori che possono cambiare l'esito. Una parte delle ricerche è pensata apposta per trovare la tesi contraria.
2. **Lavora solo sul testo integrale.** Un programma scarica ogni provvedimento e ne ricava il testo prima che l'IA lo legga. L'IA cita soltanto frasi copiate da lì; pagina e paragrafo li calcola il programma ritrovando la frase.
3. **Ogni affermazione ha un appiglio.** Ogni fattore registrato e ogni peso attribuito a una questione deve poggiare su una frase del provvedimento, altrimenti la verifica si blocca.
4. **Costruisce una matrice dei fattori**, con i precedenti ordinati per somiglianza al caso.
5. **Attacca il proprio lavoro** prima di consegnarlo. Un revisore separato legge il memo da avversario, da giudice con poco tempo e da verificatore.
6. **Verifica le norme con LexItalia 2.0** su Normattiva.

## Contenuto del repository

| Cartella | Che cos'è |
|---|---|
| `panucci-ricerca-sentenze/` | la skill principale: istruzioni, profili delle fonti, programma `strumenti/sentenze.py` |
| `bdp-ricerca/` | skill di supporto per cercare e scaricare dalla Banca Dati di Merito tramite Claude in Chrome |
| `pacchetti/` | le due skill in formato `.skill`, pronte da installare |
| `prove/` | prove automatiche del programma |

## Che cosa serve

- **Claude**: l'app desktop (Code o Cowork) oppure Claude Code.
- **Un Mac** con Python 3 e `curl`, di solito già presenti. `pdftotext` è utile ma facoltativo; senza, si usa PDFKit di macOS.
- **LexItalia 2.0** collegato, per la verifica delle norme.
- **Per le banche dati ad accesso riservato**: l'estensione [Claude in Chrome](https://claude.ai/chrome) e il proprio accesso. Per la Banca Dati di Merito: SPID, CIE o credenziali Giustizia, e la skill `bdp-ricerca`.

## Installazione

**Dall'app desktop di Claude:** scarica i file da `pacchetti/` e installali dalle impostazioni delle skill.

**In Claude Code:** copia le cartelle `panucci-ricerca-sentenze` e `bdp-ricerca` in `~/.claude/skills/`.

## Come si usa

Basta descrivere il caso, senza nomi, e la tesi:

> *Usa Panucci ricerca sentenze. Il caso: [i fatti in cinque righe]. Vorrei sostenere che [la tesi]. Cerca su [le fonti] negli ultimi tre anni.*

La skill fa al massimo una domanda sui dati mancanti, poi lavora da sola. Alla fine, in `Documenti/Ricerche/<tema>`, trovi:
- il memo;
- i provvedimenti scaricati;
- la matrice dei fattori;
- tutti i passaggi intermedi, per ricontrollare ogni affermazione.

## Fonti con profilo

- **Garante privacy**: pagine dei provvedimenti.
- **EDPB**: registro delle decisioni finali art. 60 e decisioni vincolanti art. 65.
- **Banca Dati di Merito**: tramite `bdp-ricerca`.

Per una fonte nuova la skill fa prima una prova sul sito e poi ne scrive il profilo.

## Regole d'uso

- **Accessi e blocchi.** Login, SPID e captcha li gestisce l'utente. La skill non digita credenziali, non aggira blocchi e rispetta il robots.txt dei siti.
- **Banche dati a pagamento.** Prima di farci lavorare l'IA, verificate che le condizioni d'uso del vostro abbonamento lo consentano. Davanti a contenuti riservati la skill chiede un consenso esplicito per quel sito.
- **Uso mirato.** Pochi provvedimenti utili al caso, uno alla volta: non è uno strumento per copiare banche dati.
- **Il memo non sostituisce la lettura dell'avvocato.** Dice dove guardare e con quali rischi; la decisione resta di chi firma.

## Prove automatiche

```
python3 -B -m unittest discover -s prove -v
```

## Licenza

MIT. Vedi `LICENSE`.
