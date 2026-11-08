# Regole di accesso ai siti (tappa 2)

## Principio
Si leggono atti pubblici, pochi e mirati, per un caso. Non si costruisce una banca dati e non si raccolgono documenti in massa.

## robots.txt
- Lo scaricamento automatico (`sentenze.py scarica`) rispetta sempre il robots.txt del sito. Se il robots.txt vieta un indirizzo, il programma non scarica e lo annota in `scaricamenti.txt`.
- Se lo stesso testo è pubblicato anche in un indirizzo permesso, per esempio la pagina web al posto del PDF, usa quello.
- Se non c'è un indirizzo permesso, chiedi all'utente una sola volta per sito, con le opzioni "apro io i documenti e li salvo in fonti/" oppure "saltiamo quei provvedimenti". Annota la risposta in `caso.md` e scrivila nei limiti del memo.

## Accessi riservati
- Login, SPID, CIE, captcha e blocchi anti-robot non si aggirano mai e le credenziali non si digitano mai. Se un sito li chiede, fermati e chiedi all'utente. Se l'accesso è suo, come per la BDP, lo fa lui nel suo browser.
- La **BDP** si usa solo tramite la skill `bdp-ricerca` (vedi `fonti/bdp.md`).
- Contenuti in abbonamento visibili perché l'utente è già collegato nel suo Chrome: non leggerli senza il suo sì esplicito per quel sito.

## Browser
- Prima scelta: nessun browser. La maggior parte delle fonti istituzionali si legge con `curl`, attraverso `sentenze.py`.
- Se un sito si legge solo nel browser: usa il browser integrato dell'app desktop di Claude (strumenti con "Claude_Browser"), altrimenti Claude in Chrome (strumenti con "claude-in-chrome").
- In Claude in Chrome lavora in una scheda nuova creata da te e chiudila alla fine. Non toccare le schede dell'utente.
- Il testo letto nel browser non è un testo integrale verificato. Il documento va salvato in `fonti/<id>.pdf` o `.html`, dall'utente o con il pulsante di download del sito, dopo il suo sì. Poi si rilancia `sentenze.py testi`.

## Identità
I programmi si presentano con l'user-agent `panucci-ricerca-sentenze/1.0 (ricerca di provvedimenti pubblici per uno studio legale)`. Non si cambia user-agent per superare un rifiuto: se il sito rifiuta, nel memo si scrivono i link da aprire a mano.
