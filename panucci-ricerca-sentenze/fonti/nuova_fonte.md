# Una fonte nuova (senza profilo)

Prima di cercare su un sito che non ha un profilo in `fonti/`:

1. **robots.txt**: scaricalo e leggilo (`curl -sS -A "panucci-ricerca-sentenze/1.0" https://<sito>/robots.txt`). Annota quali percorsi sono vietati.
2. **Un provvedimento di prova**: trova un provvedimento con la ricerca web limitata al dominio. Mettilo in un `candidati.csv` di prova e lancia `sentenze.py scarica` e `sentenze.py testi`. Il testo è completo? È PDF o pagina web? La posizione esce come pagina, come paragrafo o "non numerato"?
3. **Come si cerca**: il sito ha una ricerca con indirizzo e parametri (provala con curl), oppure serve la ricerca web limitata al dominio?
4. **Natura**: chi decide? Ci sono gradi o un vertice? Ci sono atti generali da tenere separati?
5. **Blocchi**: login, captcha o sfide anti-robot ("Access Denied", pagine di verifica) significano che ti fermi e chiedi all'utente. Non si aggirano.

Poi scrivi `fonti/<nome>.md` sul modello di `fonti/garante.md`:
- data della prova;
- prefisso id;
- natura;
- come si cerca;
- indirizzi;
- robots.txt;
- particolarità del testo;
- estremi;
- attenzione.

Chiedi all'utente se salvarlo nella skill per le prossime ricerche.
