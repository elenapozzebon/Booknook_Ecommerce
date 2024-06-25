# Progetto-Basi-di-Dati
Progetto di basi di dati 2024, secondo anno università. E-commerce di libri.

# 1. Pianificazione
Crea una directory per il progetto con sottocartelle per il front-end, back-end, database, e documentazione.

# 2. Progettazione del Database
Schema concettuale e logico:
Disegna un diagramma E-R (Entity-Relationship) per il database.
Identifica le entità principali (Utenti, Libri, Ordini, Carrello, Recensioni).
Definisci le relazioni tra le entità (es. un utente può avere più ordini, un libro può avere più recensioni).

Definizione delle tabelle:
Crea tabelle per ogni entità con i relativi attributi.
Definisci chiavi primarie e straniere, vincoli di integrità, e indici.

# 3. Creazione del Database
Scripting SQL:
Scrivi script SQL per creare le tabelle e popolare il database con dati di esempio.
Utilizzo di SQLAlchemy:
Configura SQLAlchemy per interfacciarsi con il DBMS scelto.
Definisci i modelli Python per le tabelle del database.

# 4. Implementazione del Back-End
Configurazione Flask:
Installa Flask e Flask-SQLAlchemy.
Configura l'app Flask e collega il database.
Gestione degli utenti:

Implementa l'autenticazione e l'autorizzazione (es. Flask-Login).
Crea modelli e viste per la registrazione, login, e gestione del profilo.
Gestione dei prodotti (Libri):

Crea modelli per i libri con attributi come titolo, autore, descrizione, prezzo, disponibilità.
Implementa CRUD (Create, Read, Update, Delete) per i libri.
Carrello della spesa e gestione degli ordini:

Implementa la funzionalità del carrello della spesa.
Crea modelli per gli ordini e gestisci lo stato degli ordini.

# 5. Implementazione del Front-End
Struttura delle pagine:
Crea le pagine principali: home, catalogo libri, dettaglio libro, carrello, profilo utente, ecc.
Utilizzo di Bootstrap o altro framework CSS:

Utilizza Bootstrap per stilizzare le pagine.
Implementa funzionalità di ricerca e filtri.
JavaScript (opzionale):

Migliora l'esperienza utente con JavaScript (es. aggiornamento dinamico del carrello).

# 6. Miglioramenti e Ottimizzazioni
Integrità dei dati:
Definisci trigger e transazioni per garantire l'integrità dei dati.
Sicurezza:
Implementa misure di sicurezza (protezione contro XSS, SQL injection).
Performance:
Ottimizza il database con indici.
Astrazione dal DBMS:
Usa ORM di SQLAlchemy per mantenere l'astrazione dal DBMS.

# 7. Documentazione
Relazione PDF:
Descrivi le funzionalità principali, la progettazione del database, le query principali, e le scelte progettuali.
Documenta le scelte tecnologiche e il contributo dei membri del gruppo.
Commenti nel codice:
Assicurati che il codice sia ben commentato per facilitare la manutenzione.

# 8. Consegna
Preparazione del file ZIP:
Includi il codice sorgente, le risorse, la documentazione, e il video di demo.
Video demo:
Registra un video di circa 10 minuti che mostri l'applicazione funzionante.

# Esempio di Timeline
1 - Pianificazione e progettazione del database.
2 - Implementazione del back-end e gestione degli utenti.
3 - Implementazione del front-end e gestione dei prodotti.
4 - Miglioramenti, ottimizzazioni e documentazione.
5 - Preparazione del file ZIP e registrazione del video demo.
