# Fonte: Comitato europeo per la protezione dei dati (edpb.europa.eu)

Provato l'8 novembre 2026, da terminale.

- **Prefisso id**: `edpb-<numero della decisione>` (es. `edpb-3906`); per le decisioni vincolanti art. 65: `edpb-vincolante-<anno>-<n>`.
- **Natura**:
  - **Registro delle decisioni finali art. 60 GDPR**: decisioni di autorità nazionali capofila nei casi transfrontalieri. L'autorità che decide è quella nazionale, che va indicata in `estremi.autorita` (es. "CNIL (Francia)"), non l'EDPB. Più decisioni della stessa autorità non sono "più autorità".
  - **Decisioni vincolanti art. 65**: decisioni dell'EDPB, che è il vertice per i casi transfrontalieri. Va fatta almeno un'interrogazione anche lì.
  - **Linee guida e pareri**: sono atti di indirizzo, non precedenti.
- **Come si cerca nel registro**: `https://www.edpb.europa.eu/registers/register-of-final-one-stop-shop-decisions_en?keys=<parole in inglese>`, con pagine successive `&page=1`, `&page=2`. Ogni voce mostra autorità capofila, argomenti ("Legal basis", "Marketing"…), esito, identificativo EDPBI e data. Il robots.txt vieta /search/: non usare la ricerca generale del sito.
- **Decisioni vincolanti**: `https://www.edpb.europa.eu/our-work-tools/consistency-findings/binding-decisions_en`.
- **Documento**: PDF in `/system/files/...`, permessi dal robots.txt. In `url_pagina` metti l'indirizzo della ricerca nel registro.
- **Estremi**: in `estremi.numero` l'identificativo EDPBI (es. EDPBI:FR:OSS:D:2026:3906); `tipo` come risulta dal documento.
- **Attenzione (prova dell'8/11/2026)**:
  - alcuni PDF del registro sono solo lettere di chiusura senza la decisione (n. 419, n. 3902): vanno scartati con il motivo;
  - alcuni documenti sono intestati "Draft decision" o sono lettere con un ordine di conformarsi: va segnalato in `lacune`;
  - molte decisioni sono traduzioni non ufficiali (lo dice la prima riga): `lacune` "traduzione non ufficiale; fa fede la lingua originale";
  - i passaggi restano nella lingua del documento.
- **Norme**: GDPR e direttive non sono su Normattiva. Le norme nazionali straniere citate nelle decisioni non si verificano: si riportano come citate.
