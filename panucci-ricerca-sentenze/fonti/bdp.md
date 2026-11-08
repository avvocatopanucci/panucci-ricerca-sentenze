# Fonte: Banca Dati di Merito (bdp.giustizia.it)

- **Prefisso id**: `bdp-<numero R.G.>-<anno R.G.>`, assegnato dal programma.
- **Natura**: sentenze, ordinanze e decreti di tribunali e corti d'appello, anonimizzati. I gradi sono primo grado e appello. Per il vertice (Cassazione) serve un'altra fonte.
- **Accesso**: riservato, con SPID, CIE o credenziali Giustizia. L'accesso lo fa l'utente nel suo Chrome, mai tu.
- **Come si cerca e si scarica**: si usa la skill **bdp-ricerca** (già installata), che conosce il modulo di ricerca e il download. Caricala e seguine le fasi con i parametri di questa ricerca:
  - testo libero dalle parole della tesi e dei fattori;
  - periodo e uffici da `caso.md`;
  - quota di provvedimenti dalla tappa 1.

  Fai scaricare i PDF in `<cartella>/bdp/` senza rinominarli.
- **Importazione**:
  ```
  python3 "<skill>/strumenti/sentenze.py" importa-bdp "<cartella>" "<cartella>/bdp"
  ```
  Aggiunge le righe a `candidati.csv` (scelta `leggi`) e copia i PDF in `fonti/`; gli originali restano in `bdp/`. Poi `sentenze.py testi` come per le altre fonti. Ricalibra le scelte (leggi, riserva) dopo l'importazione.
- **Estremi**: ufficio, tipo, R.G. e data di pubblicazione vengono dal nome del file. Sezione e giudice vanno letti nel testo.
- **Nel memo**: citare la fonte come "Banca Dati di Merito" e indicare nei limiti che la ricerca è testuale sulle motivazioni anonimizzate ed è stata fatta con l'accesso dell'utente.
- **Provato l'8 novembre 2026** su una ricerca reale (5 sentenze civili, penale per ritardo). Cose imparate:
  - **Date.** Il calendario dei filtri per data è poco affidabile. Conviene lasciare vuote le date e ordinare per data decrescente: i risultati più recenti vengono per primi. Dichiara nel memo che il campione è il più recente e non copre tutto il periodo.
  - **Indirizzo del singolo risultato.** Dopo una ricerca, "Apri" sul primo risultato porta a `provvedimento/page?from=N&size=1&...&q=...`. Cambiando N si apre il risultato N-esimo, e su ciascuno si preme "Scarica provvedimento".
  - **Nomi dei file.** Oggi includono anche il numero della sentenza (`SENTENZA_TRIBUNALE_DI_VARESE_N._567_2026_-_N._R.G._...`): `importa-bdp` li riconosce e mette numero e R.G. negli estremi. L'id resta `bdp-<R.G.>-<anno R.G.>`.
  - **Tesi contraria.** Una ricerca per frase esatta (es. "non appare manifestamente eccessiva") misura quanto ricorre l'argomento opposto. I risultati non letti non vanno contati come esiti.
  - **Ricerche costruite a mano.** Gli indirizzi di ricerca costruiti a mano per la frase esatta danno errore: usa il modulo (campo Testo + Tipo ricerca testuale).
