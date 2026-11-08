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
- **Stato**: questo collegamento non è ancora stato provato su una ricerca reale.
