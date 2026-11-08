# Il memo (tappe 9 e 10)

Il memo è per l'avvocato che deve decidere che cosa fare per il cliente. Si scrive solo da: analisi, `matrice.md`, `seconda_lettura.md`, `caso.md`. Non si rileggono i provvedimenti per aggiungere cose nuove: se manca qualcosa, torna alla tappa 5.

## Struttura di `memo_bozza.md` e di `memo.md`
1. **In breve.** Al massimo 6 righe:
   - la risposta alla domanda del caso, con il numero di pronunce lette che la reggono e gli id;
   - la principale pronuncia contraria;
   - il rischio per il cliente.
2. **Il caso e la domanda**, in tre righe, da `caso.md`.
3. **Che cosa decide l'esito.** I fattori che, nelle pronunce lette, si accompagnano a esiti diversi, con gli id. Riprendi la sezione "Ogni valore dei fattori" di `matrice.md` e commentala.
4. **I precedenti più vicini al caso.** Da 3 a 5, dalla sezione "Vicinanza al caso". Per ciascuno:
   - estremi;
   - che cosa ha deciso;
   - perché somiglia al caso;
   - in che cosa se ne discosta;
   - un passaggio tra virgolette con la sua posizione.
5. **I precedenti contrari** e come si distinguono dal caso, se si distinguono. Questa sezione non si omette mai: se non ci sono precedenti contrari, si scrive anche come sono stati cercati.
6. **Divergenze**: tra autorità, tra Stati, all'interno della stessa autorità. Le fonti di ordinamenti diversi non si sommano.
7. **Matrice dei fattori**: si incolla la tabella "Provvedimenti e fattori" di `matrice.md`.
8. **Come è stata fatta la ricerca**:
   - fonti, periodo, interrogazioni, comprese quelle per la tesi contraria (da `caso.md`);
   - numeri: candidati, letti, scartati con il motivo, testi integrali disponibili;
   - verifica: passaggi ritrovati X/Y (da `verifiche.txt`) e correzioni della seconda lettura;
   - prova di resistenza: rilievi accolti e respinti;
   - limiti: quello che la ricerca non copre.
9. **Nota sulle fonti normative**: vedi la sezione "Norme".

## Regole di scrittura
- Ogni affermazione sui precedenti indica gli id che la reggono. Con meno di 10 pronunce lette non si usano formule di prevalenza: si scrive "in N delle M pronunce lette".
- Vietati "costante", "consolidato", "pacifico", "sempre", "mai", "primo", "unico" se le analisi non lo dimostrano.
- Le frasi tra virgolette si prendono solo dalla sezione "Passaggi verificati" di `matrice.md`, con la posizione indicata lì. Un passaggio segnato "NON VERIFICATO" non entra nel memo.
- Le deduzioni tue si scrivono come tali ("Se ne può ricavare, ma le pronunce non lo dicono, che…").
- Un campione non è la prassi: si scrive "non risulta nelle pronunce lette", mai "non esiste".
- Gli atti di indirizzo (linee guida, pareri, provvedimenti generali) non sono precedenti: se servono, vanno in un paragrafo a parte.
- Niente dati che identificano persone fisiche oltre a quelli già pubblici nel provvedimento, e mai tentativi di riconoscere le persone oscurate.

## Norme
Per ogni norma italiana citata nel memo usa **LexItalia 2.0**: carica la skill `lexitalia-2` e segui la sua procedura.
- Chiama `risolvi_norma` con l'articolo scritto come testo, es. `"art. 130"`. Un numero semplice viene rifiutato.
- Il link è solo quello restituito dallo strumento. Se lo strumento non lo dà, la norma resta senza link.
- Gli atti dell'Unione europea non sono su Normattiva: si citano con gli estremi e si indicano come "non verificati con LexItalia".
- In fondo al memo va la **Nota sulle fonti normative** nel formato di `lexitalia-2`, chiusa da "Dati: Normattiva Open Data (dati.normattiva.it), licenza CC BY 4.0."
- Se LexItalia non è collegato, dillo all'utente come prevede `lexitalia-2` e chiedi come procedere.
