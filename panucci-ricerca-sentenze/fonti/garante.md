# Fonte: Garante per la protezione dei dati personali (garanteprivacy.it)

Provato l'8 novembre 2026, da terminale, su 8 provvedimenti.

- **Prefisso id**: `garante-<numero docweb>` (es. `garante-10082705`).
- **Natura**: autorità amministrativa unica. Non ci sono gradi interni: i ricorsi vanno al giudice ordinario e non si trovano su questo sito. Distingui i provvedimenti su un caso (ordinanze ingiunzione, ammonimenti, provvedimenti correttivi) dagli atti generali (linee guida, provvedimenti generali, FAQ, newsletter). Gli atti generali vanno, se servono, tra gli atti di indirizzo.
- **Come si cerca**: ricerca web limitata al dominio (`allowed_domains: ["garanteprivacy.it"]`). Con 2-3 parole tecniche e un anno dà risultati docweb con data e numero. Le newsletter rinviano ai provvedimenti: usale per trovarli, non come fonte.
- **Indirizzo del provvedimento**: `https://www.garanteprivacy.it/web/guest/home/docweb/-/docweb-display/docweb/<numero>`. È una pagina web, quindi `formato` = html e `url_documento` = lo stesso indirizzo.
- **robots.txt**: le pagine docweb sono permesse, i PDF no (`/*.pdf`). Usa sempre la pagina web, che contiene il testo integrale.
- **Testo**: in testa ci sono menu, "Vedi anche" e pulsanti; il provvedimento comincia dopo il titolo ripetuto. I paragrafi sono numerati ("4.1", "4.2"), quindi la posizione dei passaggi esce come "par. 4.1".
- **Estremi**: il numero del registro dei provvedimenti è nel testo ("Registro dei provvedimenti n. … del …"); il numero docweb è nel titolo. Il collegio si legge in testa (Presidente, componenti) e il relatore in fondo.
- **Attenzione**: nei titoli si trovano refusi ("17 luglio 20204"); vale la data nel testo, e il refuso va segnalato in `lacune`. Spesso una sanzione unica copre più violazioni: non attribuirla per intero alla questione.
