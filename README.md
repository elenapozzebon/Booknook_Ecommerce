# BookNook - E-commerce di Libri

Progetto universitario per il corso di Basi di Dati (Anno Accademico 2023-2024). 
BookNook è una piattaforma web dedicata agli appassionati di libri, progettata per permettere agli utenti di acquistare e vendere testi in modo semplice e sicuro. L'applicazione utilizza Flask per il back-end e PostgreSQL per il database.

---

## Struttura del Progetto

Il progetto è organizzato con la seguente struttura di file e cartelle:

* **`app.py`**: Il file principale del back-end contenente le rotte Flask, i modelli SQLAlchemy e la logica applicativa.
* **`templates/`**: Cartella contenente tutti i file HTML per l'interfaccia utente (es. login, carrello, profilo).
* **`static/img/`**: Cartella dedicata alle risorse statiche, come il logo e le immagini utilizzate nel sito web.
* **`db/schema_booknook_db.sql`**: File di backup contenente lo schema strutturale del database PostgreSQL (tabelle, viste, trigger e ruoli), privo di dati personali per motivi di privacy.

---

## Funzionalità Principali

L'applicazione distingue due tipologie di utenti tramite un campo booleano nel database, offrendo funzionalità mirate:

**Area Compratori**
* **Ricerca e Filtri:** Barra di ricerca avanzata per trovare libri tramite titolo, casa editrice, categoria e prezzo. I risultati escludono automaticamente i libri venduti dall'utente stesso.
* **Gestione Carrello:** Aggiunta di prodotti al carrello con controllo dinamico in tempo reale della quantità effettivamente rimanente in magazzino.
* **Ordini e Notifiche:** Completamento dell'acquisto e ricezione di notifiche automatiche ogni volta che il venditore aggiorna lo stato dell'ordine (es. "In Preparazione", "Spedito").
* **Recensioni:** Sistema di feedback per valutare i libri acquistati, con calcolo automatico della media delle valutazioni.

**Area Venditori**
* **Gestione Catalogo:** Inserimento di nuovi libri o aggiunta di copie a titoli esistenti (con funzione di auto-completamento tramite JavaScript) specificando quantità, prezzo e usura.
* **Rimozione Prodotti:** Eliminazione logica di un libro dalla vetrina impostando semplicemente la sua quantità a zero.
* **Dashboard Vendite:** Schermata dedicata per visualizzare gli ordini ricevuti dai compratori e aggiornarne lo stato di spedizione.

**Dietro le quinte (Database e Sicurezza)**
* **Sicurezza Password:** Tutte le password sono crittografate tramite algoritmo SHA-256 prima del salvataggio.
* **Gestione Ruoli PostgreSQL:** La registrazione crea fisicamente un utente nel database PostgreSQL, assegnandogli i permessi formali (`GRANT`) appropriati al suo ruolo.
* **Trigger di Integrità:** Un *Before Trigger* impedisce l'aggiunta al carrello di quantità non disponibili, mentre un *After Trigger* gestisce l'attivazione automatica delle notifiche per gli ordini.
* **Viste Ottimizzate:** Utilizzo di una View SQL per pre-calcolare e aggregare le medie delle recensioni dei libri.

---

## Come Usare il Progetto (Installazione ed Esecuzione da Terminale)

Segui questi passaggi per avviare l'applicazione in locale sul tuo computer utilizzando la riga di comando.

### 1. Configurazione del Database (Schema Vuoto)
Essendo una repository pubblica, il database fornito contiene solo la struttura logica e non i dati sensibili. Assicurati di avere **PostgreSQL** installato e configurato nelle variabili di ambiente del tuo sistema.

1. Apri il terminale e crea un nuovo database vuoto chiamato `"progetto_basi"` eseguendo questo comando:
   ```bash
   createdb -U postgres progettoBasi
   ```
2. Ripristina lo schema strutturale importando il file SQL fornito nella repository:
   ```bash
    psql -U postgres -d progettoBasi -f schema_booknook_db.sql
   ```
3. Nota: Avviando l'app, il database sarà inizialmente vuoto. Registrati come nuovo utente dall'interfaccia web per iniziare a popolarlo!

### 2. Configurazione dell'Ambiente Python

1. Assicurati di avere Python installato sul sistema.
2. Apri il terminale nella cartella principale del progetto (dove si trova il file app.py).
3. Installa tutte le dipendenze necessarie eseguendo:
   ```bash
    pip install Flask Flask-SQLAlchemy Flask-Login Flask-Migrate psycopg2 sqlalchemy
   ```
(Consiglio: è buona pratica creare prima un ambiente virtuale con ```python -m venv venv``` e attivarlo, per poi eseguire il ```pip install```).

### 3. Connessione e Avvio

1. Apri il file app.py con il tuo editor di testo preferito (es. VS Code, PyCharm o Blocco Note).
2. Alla riga 14, verifica che la stringa di connessione URI corrisponda alla password del tuo server PostgreSQL locale:
   ```Python
   app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:latuapassword@localhost/progettoBasi'
   ```
3. Torna sul terminale e avvia il server eseguendo:
   ```bash
   python app.py
   ```
4. Apri il browser e collegati all'indirizzo ```http://127.0.0.1:5000```.
