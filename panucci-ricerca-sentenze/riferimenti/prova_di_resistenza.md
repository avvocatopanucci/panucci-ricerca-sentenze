# Prova di resistenza (tappa 9, per l'assistente sonnet)

Ricevi la cartella della ricerca. Leggi `memo_bozza.md`, `caso.md`, `fattori.json`, `matrice.md`, `seconda_lettura.md` e, quando serve, `analisi/<id>.json` e `testi/<id>.txt` (cerca nei testi con grep o a blocchi). Non modificare file e non fare ricerche web.

Leggi la bozza tre volte, ogni volta con un'identità diversa e con un solo scopo.

## 1. L'avversario
Difende la tesi opposta a quella del caso e vuole usare questa stessa ricerca contro il cliente.
- Quali provvedimenti contrari o misti userebbe? Sono presentati nel memo con il peso che hanno davvero, o sono stati attenuati?
- Su quali fattori il caso del cliente si discosta dai precedenti favorevoli? È un "distinguo" che l'avversario potrebbe sollevare?
- C'è una lettura dei precedenti favorevoli che li rende inutili per il caso, per esempio perché decisi su un altro canale o su un'altra categoria di destinatari?

## 2. Il giudice con poco tempo
Vuole capire in due minuti se il memo regge.
- La risposta è nelle prime righe ed è proporzionata alle pronunce lette?
- Ci sono formule di prevalenza ("orientamento costante", "consolidato", "pacifico", "sempre") non giustificate dal numero di pronunce lette?
- Sono sommate autorità o Stati diversi come se fossero un unico orientamento?
- Sono distinti il peso pieno, il motivo concorrente e il detto di passaggio?

## 3. Il verificatore
Controlla che ogni frase del memo sia sorretta dalle fonti.
- Ogni affermazione sui precedenti indica gli id che la reggono, e quegli id dicono davvero quella cosa?
- Ogni frase tra virgolette compare identica in `matrice.md`, nella sezione dei passaggi verificati, o nel testo integrale?
- I numeri della bozza (quante pronunce, quanti favorevoli) coincidono con `matrice.md`?
- Le deduzioni dell'autore sono dichiarate come tali?
- I limiti dichiarati sono completi: fonti non coperte, scarti, testi mancanti?

## Che cosa restituisci
Una tabella con le colonne:
- **lettore** (avversario / giudice / verificatore);
- **rilievo**, con il punto del memo e gli id;
- **gravità** (alta / media / bassa);
- **correzione proposta**, con il testo pronto o la cancellazione.

Sotto la tabella, in massimo 3 righe: il punto più debole del memo e il suo giudizio complessivo. Se non trovi rilievi per un lettore, dillo e scrivi che cosa hai controllato. Massimo 500 parole in tutto.
