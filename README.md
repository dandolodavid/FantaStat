# FANTASTAT
 
FantaStat è una piccola web app ad uso personale, nata con lo scopo di agevolare la gestione dell'asta del fantacalcio, creando un tool asta ricco di statistiche, e funzionale a capire quali giocatori prendere per qualità prezzo durante le chiamate.

I dati usati sono il risultato di uno scraping sui siti https://fantacalcio.it (per quanto riguarda i dati su voti, gol, assist e voti/fantavoti) e https://understat.com/league/Serie_A (per quanto riguarda gli xG e gli xA).

Una volta ottenuta per ogni giocatore la serie storica dei voti/fantavoti, bonus, malus, e lo status in ogni giornata (titolare, subentrato, infortunato, inutilizzato), aggreghiamo questi dati con i dati sugli xG e xA, calcoliamo una serie di statistiche utile per capire il valore dei gocatori (% partite con bonus, con malus, con voto, minuti giocati ) ed esaminiamo la distribuzione dei voti per capire la costanza di rendimento del giocatore, ottenendo una tabella dati completa e ricca di informazioni utili.
Inoltre per avere una visione generale della Serie A, è presente la classifica del campionato con in aggiunta gli xG, i nonPenalty_xG e gli xG concessi, oltre che a dei coefficenti che indicano la forza di attacco e di difesa stimati dal calendario risultati tramite il modello Dixon&Coles (https://thesis.unipd.it/bitstream/20.500.12608/27251/1/Dandolo_David.pdf).

# TECNOLOGIE USATE:
- Python
- Plotly
- Flask
- Selenium
- BeautifoulSoup
- jinja2
- HTML
- CSS

# SEZIONI 

# Homepage
![homepage](/img/home_page.png)

# Classifica
Classifica con dati sugli xG,xA,xGA e coefficienti del modello Dixon&Coles per le squadre di Serie A
![homepage](/img/classifica.png)

# Info Giocatore:
Una pagina in cui i può selezionare un giocatore specifico e vedere un riepilogo completo delle statistiche e delle informazioni per ogni giocatore. In fondo alla pagine sono presenti inoltre dei grafici che mostrano l'andamento dei voti/fantavoto per giornata e le partite in cui il giocatore ha portato bonus.
![homepage](/img/player_info.png)


# Listone:
Consente di esplorare il listone, in forma tabulare (ordinabile per colonna) con tutte le statistiche a disposizione per il giocatore, dando la possibilità di selezionare uno slot per ogni calciatore per poterli distinguere meglio in fase d'asta, di aggiungere i giocatori alla lista preferiti cliccando l'immagine del campioncino e di applicare filtri su presenze, squadra, slot indicato e preferiti/non preferiti
![homepage](/img/listone.png)

# ToolAsta
Replica la visuale del Listone, con un conteggio dei giocatori residui per ruolo e per slot assegnato. I preferiti assegnati nella sezione listone sono sempre presenti, stavolta però cliccando il campioncino si indica all'applicazione che il giocatore non è più disponibile (perchè già acqusitato) ed aggiorna i conteggi dei giocatori residui.
![homepage](/img/tool_asta.png)

# TeamBuilder
Seleziona 11 giocatori (tra quelli di cui tutte le statistche sono disponibili, quindi non i nuovi arrivati nel listone), e costruisci una squadra. A questo punto il sistema calcola la media punti a giornata, e riassume in una tabella il numero di bonus/malus per reparto, oltre che la % di partite con voto, la fantamedia voto e la distibuzione dei fantavoti. Infine si mostra l'andamento della squadra con la serie temporale dei punti ottenuti nella 38 giornate e la media voto/fantavoto per reparto nelle 38 giornate.
![homepage](/img/team_builder.png)
![homepage](/img/team_builded.png)