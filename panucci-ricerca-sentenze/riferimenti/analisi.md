# Come si legge un provvedimento (tappa 5, per l'assistente che legge)

Ricevi: la cartella della ricerca, gli id da leggere, la tesi del caso e il percorso di `fattori.json`. Per ogni id lavori solo su `testi/<id>.txt`, il testo integrale ricavato dal documento da un programma. Niente ricerche web. Se il testo comincia con menu o intestazioni del sito, ignorali.

## Prima domanda: è pertinente?
Il provvedimento affronta nella motivazione la questione della tesi? Se no, non scrivere l'analisi: scrivi invece `scarti/<id>.txt` con una riga sul motivo. Non modificare `candidati.csv`: altri lettori lavorano in parallelo e lo aggiorna l'orchestratore.

## L'analisi: `analisi/<id>.json`
```json
{
 "id": "garante-10082705",
 "estremi": {"autorita": "Garante per la protezione dei dati personali", "organo": "Collegio", "tipo": "ordinanza ingiunzione", "data": "2024-01-11", "numero": "n. 4/2024", "parti": "Findomestic Banca S.p.A."},
 "domanda_affrontata": "Se il legittimo interesse possa fondare telefonate e lettere promozionali ai clienti",
 "risposta": "No per le telefonate con operatore, per le quali serve il consenso; sì per la posta cartacea, con un bilanciamento documentato",
 "peso": "regge la decisione",
 "esito": "contrario alla tesi",
 "fattori": {"canale": "telefono con operatore", "destinatari": "clienti", "opposizione_alla_raccolta": "non risulta", "bilanciamento_documentato": "sì"},
 "passaggi": [
  {"testo": "l’unica base ammissibile è il consenso dell’interessato", "serve_a": "risposta"},
  {"testo": "...", "serve_a": "esito"},
  {"testo": "...", "serve_a": "fattore:canale"}
 ],
 "conseguenze": ["sanzione di 100.000 euro", "divieto del trattamento telefonico senza consenso"],
 "norme": ["art. 130 d.lgs. 196/2003", "art. 6, par. 1, lett. f) Reg. (UE) 2016/679"],
 "precedenti": [],
 "lacune": []
}
```

## Regole
- **estremi**: tutti e sei i campi; quello che il testo non dice è "non risulta". `parti`: come nel testo; se sono oscurate, "oscurate". Non cercare mai di identificare persone oscurate.
- **domanda_affrontata** (max 30 parole) e **risposta** (max 50 parole): la risposta che il provvedimento dà, non la tua opinione.
- **peso**: quanto conta la questione nella decisione, valutando ogni capo, comprese sanzioni e misure:
  - `regge la decisione`: senza di essa l'esito di almeno un capo cambierebbe;
  - `uno dei motivi`: pesa insieme ad altri motivi autonomi;
  - `detto di passaggio`: affermato ma non necessario;
  - `solo citato`.
- **esito**, rispetto alla TESI del caso: `favorevole alla tesi`, `contrario alla tesi`, `misto` (in parte sì, in parte no, per esempio a seconda del canale), `neutro`.
- **fattori**: tutti quelli di `fattori.json`, con uno dei valori ammessi o "non risulta". Non dedurre: se il testo non lo dice, è "non risulta". Un valore ricavato da date o calcoli tuoi (per esempio "entro 72 ore" contando i giorni) non vale: serve una frase del provvedimento che lo dica.
- **passaggi**: quanti ne servono per reggere risposta, esito e ogni fattore con un valore (di solito da 3 a 10). Non lasciare un fattore a "non risulta" solo per non aggiungere un passaggio. Ognuno è una frase **copiata parola per parola** da `testi/<id>.txt`, di massimo 40 parole, continua e senza omissioni come "[...]". Non correggere i refusi del testo: copiali. Ogni passaggio indica a che cosa serve con `serve_a`:
  - `risposta`: obbligatorio, almeno uno;
  - `esito`: il passaggio della decisione o del dispositivo; obbligatorio se il peso è "regge la decisione" o "uno dei motivi";
  - `fattore:<nome>`: obbligatorio per ogni fattore con un valore diverso da "non risulta".

  Non scrivere pagine o paragrafi: li calcola il programma.
- **conseguenze**: misure e sanzioni legate alla questione, in frasi brevi; [] se nessuna.
- **norme** e **precedenti**: come citati nel testo.
- **lacune**: dubbi e incertezze, per esempio traduzione non ufficiale, testo incompleto, refusi nelle date, sanzione unica per più capi.

Prima di chiudere ogni analisi, rileggi i passaggi nel file di testo e controlla che siano identici.

Rispondi in massimo 120 parole: id analizzati, id scartati con il motivo, dubbi.
