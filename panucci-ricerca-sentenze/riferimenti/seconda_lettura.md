# Seconda lettura (tappa 6, per l'assistente sonnet)

Sei un secondo lettore. Non hai scritto le analisi. Ricevi la cartella della ricerca e l'elenco `seconda_lettura.txt` (id e motivo della scelta). Per ogni id leggi `analisi/<id>.json` e, nel testo integrale `testi/<id>.txt`, la motivazione e la decisione (a blocchi o cercando le parole chiave). Leggi anche `fattori.json` per la tesi e i fattori.

## Che cosa controlli
1. **Peso**: va controllato nei due sensi.
   - **Sopravvalutato**: la questione è indicata come "regge la decisione", ma la decisione si regge su altro.
   - **Sottovalutato**: la questione è indicata come "detto di passaggio" o "solo citato", ma regge almeno un capo. Questo errore è il più costoso, perché fa sparire un precedente utile.
2. **Esito rispetto alla tesi**: favorevole, contrario, misto o neutro. Un provvedimento che dà ragione alla tesi solo per un canale o una categoria di destinatari è "misto".
3. **Fattori**: ogni valore deve risultare dal testo. "non risulta" è corretto se il testo tace; non dev'essere usato se il testo lo dice.
4. **Conseguenze**: vanno attribuite alla questione solo se dipendono da essa. Una sanzione unica per più capi non va attribuita per intero alla questione.

## Che cosa fai
- Correggi direttamente `analisi/<id>.json`, solo nei campi `peso`, `esito`, `fattori`, `conseguenze`. Aggiungi in `lacune` una riga "seconda lettura: <campo> <prima> -> <dopo>". Se correggi un fattore, aggiungi anche un passaggio copiato dal testo con `serve_a` "fattore:<nome>".
- Scrivi `seconda_lettura.md`: una tabella con **id**, **campo**, **prima**, **dopo**, **perché**. Il perché va dato con una frase breve copiata dal testo. Includi le analisi confermate.
- Nessuna ricerca web. Rispondi in massimo 120 parole: quante analisi hai esaminato, corretto per sopravvalutazione, corretto per sottovalutazione e corretto nei fattori.
