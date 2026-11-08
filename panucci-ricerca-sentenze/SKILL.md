---
name: panucci-ricerca-sentenze
description: Ricerca di precedenti per un caso concreto su fonti pubbliche e istituzionali (Garante privacy, EDPB, Banca Dati di Merito tramite la skill bdp-ricerca, e altre fonti aggiunte con il loro profilo). Parte dai fatti del cliente, legge i provvedimenti sul testo integrale scaricato, costruisce una matrice dei fattori che hanno deciso l'esito con la vicinanza al caso, sottopone il lavoro a una prova di resistenza (avversario, giudice, verificatore) e consegna un memo con passaggi verificati da un programma e norme verificate con LexItalia 2.0. Usala quando l'avvocato chiede di trovare, raccogliere o confrontare sentenze, decisioni o provvedimenti utili a un caso o a un tema. Non per scrivere atti o pareri senza ricerca, né per la sola ricerca di norme.
---

# Panucci ricerca sentenze

Skill ideata dall'Avv. Giovanna Panucci, novembre 2026.

## Il metodo in quattro idee
1. **Si parte dal caso.** La domanda non è "che cosa dicono le sentenze su X", ma "che cosa serve sapere per questo cliente". La ricerca si costruisce intorno ai fatti e alla tesi da sostenere o da valutare.
2. **Si lavora solo sul testo integrale.** Ogni provvedimento viene scaricato e letto da un programma prima che un assistente lo analizzi. Chi analizza cita soltanto passaggi copiati da quel testo; pagina o paragrafo non li scrive lui, li calcola il programma ritrovando il passaggio.
3. **Contano i fattori, non i riassunti.** Per ogni provvedimento si registra quali fatti hanno portato a quale esito. La matrice mostra quali pronunce somigliano al caso e quali gli sono contrarie.
4. **Il lavoro si attacca prima di consegnarlo.** Un avversario cerca le pronunce da usare contro la tesi, un giudice cerca i punti deboli, un verificatore controlla che ogni frase del memo sia sorretta dalle analisi.

## Regole che valgono sempre
- L'utente è un avvocato: parla in italiano semplice, senza gergo tecnico, e fai al massimo una domanda per volta.
- Non inventare: estremi, date, esiti e principi vengono solo dai testi integrali. Se un dato non c'è, si scrive "non risulta".
- Non digitare credenziali e non aggirare login, SPID, captcha o blocchi. Le regole di accesso ai siti sono in `riferimenti/regole_di_accesso.md`: leggile alla tappa 2.
- I programmi si eseguono, non si leggono: `python3 "<skill>/strumenti/sentenze.py" <comando> "<cartella>"`. `<skill>` è la cartella di questa skill, `<cartella>` quella della ricerca.
- Il lavoro ripetitivo va ad assistenti separati (strumento Agent, `subagent_type` "general-purpose"): **haiku** per la lettura, **sonnet** per la seconda lettura e la prova di resistenza. Passa loro solo il compito, i percorsi dei file e il riferimento da leggere; chiedi risposte brevi e il lavoro su file. Se lo strumento Agent manca, fai tu quelle tappe e dichiaralo nel memo.

## Le tappe

### 1. Il caso
Leggi `riferimenti/caso_e_fattori.md`. Ricava dalla richiesta i fatti, la tesi e il periodo. Proponi in UNA domanda quello che manca: fonti (per la protezione dei dati di default Garante + EDPB; per il merito civile o penale la BDP), periodo, quanti provvedimenti leggere (default 12, divisi tra le fonti) e la cartella (default `~/Documents/Ricerche/<tema-breve>`). Poi crea la cartella e scrivi `caso.md` e `fattori.json`.

### 2. Fonti e strumenti
Leggi `riferimenti/regole_di_accesso.md` e, per ogni fonte scelta, il suo profilo in `fonti/` (es. `fonti/garante.md`, `fonti/edpb.md`, `fonti/bdp.md`). Per una fonte senza profilo segui `fonti/nuova_fonte.md`. Verifica: `curl` e `pdftotext` (`which`); lo strumento `risolvi_norma` di LexItalia (nome con "lexitalia"); per la BDP la skill `bdp-ricerca` e Claude in Chrome collegato. Scrivi l'esito in `caso.md`, sezione "Strumenti".

### 3. Candidati
Per ogni fonte, con le istruzioni del profilo, fai al massimo 8 interrogazioni:
- almeno una per la tesi del caso;
- almeno una **per la tesi contraria**;
- almeno una per l'autorità di vertice, se la fonte ne ha una.

Annota ogni interrogazione in `caso.md` ("Registro delle interrogazioni": testo, risultati, scelti). Scrivi `candidati.csv` (colonne in `riferimenti/caso_e_fattori.md`) con `scelta` = leggi, riserva o scarta. Scegli "leggi" per varietà: esiti diversi, fattori diversi, comprese le pronunce contrarie.

### 4. Acquisizione
```
python3 "<skill>/strumenti/sentenze.py" scarica "<cartella>"
python3 "<skill>/strumenti/sentenze.py" testi "<cartella>"
```
Per la BDP i file arrivano con `importa-bdp` (vedi `fonti/bdp.md`). I provvedimenti senza testo integrale, cioè scansioni o siti che rifiutano lo scaricamento, non si analizzano: lo si scrive nel memo.

### 5. Lettura
Assistenti **haiku**, al massimo 6 provvedimenti ciascuno, in parallelo: lavorano solo su file locali. Passa a ciascuno il percorso di `riferimenti/analisi.md` (lo legge lui), la cartella, gli id, la tesi e il percorso di `fattori.json`. Producono `analisi/<id>.json`. Se un provvedimento non affronta la domanda, l'assistente scrive `scarti/<id>.txt` con il motivo. Tu riporti lo scarto in `candidati.csv` (scelta `scarta`, motivo in `nota`) e valuti se leggere una riserva.

### 6. Seconda lettura
```
python3 "<skill>/strumenti/sentenze.py" campione "<cartella>"
```
Poi UN assistente **sonnet** con il percorso di `riferimenti/seconda_lettura.md`. Ricontrolla sul testo integrale peso, esito e fattori delle analisi scelte, sia le possibili sopravvalutazioni sia le sottovalutazioni, e scrive `seconda_lettura.md`.

### 7. Verifica
```
python3 "<skill>/strumenti/sentenze.py" verifica "<cartella>"
```
Ogni passaggio deve essere ritrovato nel testo integrale e ogni fattore deve poggiare su un passaggio. Finché `verifiche.txt` non dice "in regola", rimanda le analisi all'assistente che le ha scritte o correggile tu sul testo integrale. Un passaggio assente non è "falso": va ritrovato o tolto.

### 8. Matrice
```
python3 "<skill>/strumenti/sentenze.py" matrice "<cartella>"
```
`matrice.md` contiene:
- i fattori per ogni provvedimento;
- gli esiti per ciascun valore dei fattori;
- la vicinanza al caso;
- i passaggi con la loro posizione.

Non riscriverla a mano.

### 9. Memo e prova di resistenza
Leggi `riferimenti/memo.md` e scrivi `memo_bozza.md` usando solo analisi, `matrice.md` e `seconda_lettura.md`. Poi UN assistente **sonnet** con il percorso di `riferimenti/prova_di_resistenza.md`: legge la bozza da avversario, da giudice e da verificatore e scrive `prova_di_resistenza.md`. Controlla ogni rilievo sul testo integrale prima di accettarlo: chi attacca può sbagliare.

### 10. Consegna
Applica i rilievi accolti e verifica le norme come dice `riferimenti/memo.md`, sezione "Norme". Scrivi `memo.md` nella cartella della ricerca, poi:
```
python3 "<skill>/strumenti/sentenze.py" memo "<cartella>"
```
Ogni frase tra «» del memo deve essere ritrovata nei testi integrali; correggi finché il programma non dà tutte le frasi ritrovate. Le citazioni vanno sempre tra «» e mai tra altre virgolette, così il controllo le vede tutte. Messaggio finale all'utente in poche righe:
- dove sono il memo e i documenti;
- la risposta in una frase;
- i limiti principali.
