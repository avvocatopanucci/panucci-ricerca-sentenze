# Il caso, i fattori e i file della ricerca (tappa 1)

## La cartella
Default `~/Documents/Ricerche/<tema-breve>` (Documenti nel Finder). Dentro:

```
caso.md            fatti, tesi, periodo, fonti, strumenti, registro delle interrogazioni
fattori.json       la tesi e i fattori da registrare per ogni provvedimento
candidati.csv      tutti i provvedimenti trovati, con la scelta (leggi / riserva / scarta)
fonti/<id>.pdf|html  i documenti scaricati
testi/<id>.txt     testo integrale ricavato dal programma
registro.json      come è stato ricavato ogni testo (metodo, impronta sha256, pagine)
analisi/<id>.json  l'analisi di ogni provvedimento letto
scarti/<id>.txt    motivo per cui un provvedimento aperto non è pertinente
seconda_lettura.txt / seconda_lettura.md
verifiche.txt / verifiche.json
matrice.md
memo_bozza.md, prova_di_resistenza.md, memo.md
```

## caso.md
Scrivilo in poche righe:
- **Fatti** del cliente, anonimi: niente nomi né dati identificativi;
- **Tesi**, cioè che cosa si vuole sostenere o valutare, in una frase;
- **Periodo**, con date precise;
- **Fonti**;
- **Quanti provvedimenti leggere**, con la quota per fonte.

Se l'utente chiede una ricerca su un tema senza un caso, scrivi un "caso tipo" e dichiaralo.

## fattori.json
I fattori sono i fatti o le circostanze che, secondo la tua ipotesi, cambiano l'esito. Scegline da 3 a 7, ciascuno con pochi valori chiusi. Esempio per il marketing:

```json
{
 "tesi": "Il titolare può fondare sul legittimo interesse le telefonate promozionali ai propri clienti",
 "fattori": [
  {"nome": "canale", "domanda": "Con quale mezzo avviene il contatto?", "valori": ["telefono con operatore", "sms", "email", "posta", "pubblicità online", "altro"]},
  {"nome": "destinatari", "domanda": "Chi riceve il contatto?", "valori": ["clienti", "ex clienti", "prospect", "utenti di un servizio"]},
  {"nome": "opposizione_alla_raccolta", "domanda": "L'interessato poteva opporsi al momento della raccolta dei dati?", "valori": ["sì", "no"]},
  {"nome": "bilanciamento_documentato", "domanda": "Il titolare ha prodotto un bilanciamento degli interessi?", "valori": ["sì", "no"]}
 ],
 "caso": {"canale": "telefono con operatore", "destinatari": "clienti", "opposizione_alla_raccolta": "sì", "bilanciamento_documentato": "sì"}
}
```
- `nome`: minuscole, cifre e trattino basso.
- `caso`: i valori dei fattori nel caso del cliente; un fattore ignoto si omette.
- I fattori si possono correggere dopo le prime letture, se emerge un elemento che conta e non era previsto. In quel caso fai rileggere le analisi già scritte solo per quel fattore.

## candidati.csv
Colonne: `id,fonte,autorita,tipo,data,numero,titolo,url_pagina,url_documento,formato,scelta,nota`
- `id`: minuscole, cifre e trattino, con il prefisso della fonte indicato nel profilo (es. `garante-10082705`, `edpb-3906`, `bdp-4147-2025`).
- `data`: AAAA-MM-GG.
- `formato`: pdf o html.
- `scelta`: leggi, riserva o scarta.
- `nota`: perché è stato scelto o scartato.
