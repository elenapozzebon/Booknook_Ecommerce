import hashlib
from datetime import datetime

import sqlalchemy
from flask import Flask, render_template, flash, request, redirect, url_for, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from psycopg2 import IntegrityError
from sqlalchemy import create_engine, Table, MetaData, Column, Integer, String, ForeignKey, Boolean, Float, Date, \
    BigInteger, func, text
from sqlalchemy.orm import aliased, relationship
from flask_migrate import Migrate

app = Flask(__name__)  # Crea un'istanza dell'app Flask
app.config['SECRET_KEY'] = 'usersecret'  # Imposta la chiave segreta per la sessione e la protezione CSRF
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:basi@localhost/progetto_basi'  # configurazione db

db = SQLAlchemy(app)  # Inizializza SQLAlchemy con l'app Flask
migrate = Migrate(app, db)  # Configura Flask-Migrate per la gestione delle migrazioni del db

login_manager = LoginManager()  # Crea un'istanza di LoginManager per la gestione dell'autenticazione
login_manager.init_app(app)  # inizializzazione LoginManager per gestire l'autenticazione degli utenti


class Utente(db.Model, UserMixin):
    __tablename__ = 'utente'
    email = Column(String(50), primary_key=True, nullable=False)
    nome = Column(String(50))
    cognome = Column(String(50))
    telefono = Column(BigInteger)
    password = Column(String(200), nullable=False)
    venditore = Column(Boolean, nullable=False)
    data_nascita = Column(Date)
    indirizzo = Column(String(100))

    def __init__(self, email, nome, cognome, telefono, password, venditore, data_nascita, indirizzo):
        self.email = email
        self.nome = nome
        self.cognome = cognome
        self.telefono = telefono
        self.password = password
        self.venditore = venditore
        self.data_nascita = data_nascita
        self.indirizzo = indirizzo

    def get_id(self):
        return self.email


class Libri(db.Model):
    __tablename__ = 'libri'
    id_libro = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    edizione = Column(Integer)
    anno = Column(Integer)
    titolo = Column(String(50), nullable=False)
    descrizione = Column(String(400))
    casa_editrice = Column(String(50))
    id_autore = Column(Integer, ForeignKey('autore.id_autore'), nullable=False)
    autore = relationship("Autore")
    nome_categoria = Column(String(50), ForeignKey('categoria.nome_categoria'), nullable=False)


class Autore(db.Model):
    __tablename__ = 'autore'
    id_autore = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    anno_nascita = Column(Integer)
    nome = Column(String(50))
    cognome = Column(String(50))
    descrizione = Column(String(400))

    def __init__(self, nome, cognome, anno_nascita, descrizione):
        self.nome = nome
        self.cognome = cognome
        self.anno_nascita = anno_nascita
        self.descrizione = descrizione


class Categoria(db.Model):
    __tablename__ = 'categoria'
    nome_categoria = Column(String(50), primary_key=True, nullable=False)


class Ordini(db.Model):
    __tablename__ = 'ordini'
    id_ordine = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    data = Column(Date, nullable=False)
    id_utente = Column(String(50), ForeignKey('utente.email'), nullable=False)
    indirizzo_spedizione = Column(String(100), nullable=False)
    id_libro = Column(Integer, ForeignKey('libri.id_libro'), primary_key=True, nullable=False)
    id_venditore = Column(String(50), ForeignKey('utente.email'), nullable=False)
    stato = Column(String(50), nullable=False)
    quantita = Column(Integer, nullable=False)
    metodo_pagamento = Column(String(100), nullable=False)
    notifica_attiva = Column(Boolean, nullable=False, default=False)

    def __init__(self, data, id_utente, indirizzo_spedizione, id_libro, id_venditore, stato, quantita,
                 metodo_pagamento):
        self.data = data
        self.id_utente = id_utente
        self.indirizzo_spedizione = indirizzo_spedizione
        self.id_libro = id_libro
        self.id_venditore = id_venditore
        self.stato = stato
        self.quantita = quantita
        self.metodo_pagamento = metodo_pagamento


class Venditore_Libro(db.Model):
    __tablename__ = 'venditore_libro'
    id_libro = Column(Integer, ForeignKey('libri.id_libro'), primary_key=True, nullable=False)
    id_venditore = Column(String(50), ForeignKey('utente.email'), primary_key=True, nullable=False)
    quantita = Column(Integer, nullable=False)
    prezzo = Column(Float, nullable=False)
    stato_nuovo = Column(Boolean, nullable=False)  # nuovo = true


class Carrello(db.Model):
    __tablename__ = 'carrello'
    id_carrello = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    id_utente = Column(String(50), ForeignKey('utente.email'), nullable=False)


class Libri_Carrello(db.Model):
    __tablename__ = 'libri_carrello'
    id_libro = Column(Integer, ForeignKey('venditore_libro.id_libro'), primary_key=True, nullable=False)
    id_venditore = Column(String(50), ForeignKey('venditore_libro.id_venditore'), primary_key=True, nullable=False)
    id_carrello = Column(Integer, ForeignKey('carrello.id_carrello'), primary_key=True, nullable=False)
    quantita = Column(Integer, nullable=False)

    def __init__(self, id_libro, id_venditore, id_carrello, quantita):
        self.id_libro = id_libro
        self.id_venditore = id_venditore
        self.id_carrello = id_carrello
        self.quantita = quantita


class Recensioni(db.Model):
    __tablename__ = 'recensioni'
    id_recensione = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    valutazione = Column(Integer, nullable=False)
    id_libro = Column(Integer, ForeignKey('libri.id_libro'), nullable=False)
    id_utente = Column(String(50), ForeignKey('utente.email'), nullable=False)
    id_venditore = Column(String(50), ForeignKey('utente.email'), nullable=False)
    descrizione = Column(String(400))

    def __init__(self, valutazione, id_libro, id_utente, descrizione, id_venditore):
        self.valutazione = valutazione
        self.id_libro = id_libro
        self.id_utente = id_utente
        self.descrizione = descrizione
        self.id_venditore = id_venditore


# Per la view
class Media_Valutazioni_Libro_Venditore(db.Model):
    __tablename__ = 'media_valutazioni_libro_venditore'  # Nome della vista in PostgreSQL
    id_libro = db.Column(db.Integer, primary_key=True)
    id_venditore = db.Column(db.String, primary_key=True)
    media_valutazione = db.Column(db.Float)


# specifica come recuperare l'utente dalla sessione attiva
@login_manager.user_loader
def load_user(email):
    return Utente.query.get(email)


@app.route('/')
def start():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Recupera l'utente dal database
        user = Utente.query.get(email)

        # Verifica se l'utente esiste e la password è corretta
        if user:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            # Controlla l'hash della password
            if hashed_password == user.password:
                login_user(user)
                if user.venditore:
                    return redirect(url_for('solo_venditore'))
                else:
                    return redirect(url_for('solo_compratore'))
            else:
                error = "Password errata."
        else:
            error = "Utente non trovato."
    return redirect(url_for('start'))  # log-in nella pagina iniziale


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        # Recupera i valori dal form e imposta a None se sono stringhe vuote
        email = request.form.get('email')
        password = request.form.get('password')
        venditore = (request.form.get('venditore') == 'Si')
        indirizzo = request.form.get('indirizzo')

        # Campi opzionali: se vuoti, assegnare None
        nome = request.form.get('nome') or None
        cognome = request.form.get('cognome') or None
        telefono = request.form.get('telefono') or None
        data_nascita = request.form.get('data_nascita') or None

        # Se telefono è una stringa vuota, impostarlo a None
        telefono = telefono if telefono else None

        # Hash della password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Crea il nuovo utente
        new_user = Utente(
            email=email,
            nome=nome,
            cognome=cognome,
            telefono=telefono,
            password=hashed_password,
            venditore=venditore,
            data_nascita=data_nascita,
            indirizzo=indirizzo
        )

        # Verifica se l'email è già presente nel database
        if Utente.query.get(new_user.email):
            error = "Questa email risulta già utilizzata!"  # da gestire meglio
        else:
            db.session.add(new_user)
            db.session.commit()
            # Crea l'utente nel database PostgreSQL
            try:
                # Crea l'utente e assegna il ruolo appropriato
                db.session.execute(text(f'CREATE USER "{email}" WITH PASSWORD \'{hashed_password}\';'))

                # Assegnazione del ruolo in base al flag venditore
                if venditore:
                    db.session.execute(text(f'GRANT venditore TO "{email}";'))
                else:
                    db.session.execute(text(f'GRANT compratore TO "{email}";'))

                db.session.commit()  # Commita i permessi

                # Effettua il login dell'utente
                login_user(new_user)

                if new_user.venditore:
                    return redirect(url_for('solo_venditore'))
                else:
                    return redirect(url_for('solo_compratore'))
            except IntegrityError:
                db.session.rollback()
                error = "Si è verificato un errore durante la creazione dell'utente nel database."

    return render_template('register.html', error=error)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('start'))


@app.route('/solo_compratore')
@login_required
def solo_compratore():
    notifiche_attive = Ordini.query.filter_by(id_utente=current_user.email, notifica_attiva=True).first()

    editori = db.session.query(Libri.casa_editrice).distinct().all()
    categorie = db.session.query(Categoria.nome_categoria).all()

    top_books = (
        db.session.query(Libri, func.count(Recensioni.id_recensione).label('total_reviews'))
        .join(Recensioni, Libri.id_libro == Recensioni.id_libro)
        .group_by(Libri.id_libro)
        .order_by(func.count(Recensioni.id_recensione).desc())
        .limit(4)
        .all()
    )

    top_recensioni = db.session.query(
        Libri.id_libro,
        Libri.titolo,
        Venditore_Libro.id_venditore,
        Utente.nome.label('nome_venditore'),
        Utente.cognome.label('cognome_venditore'),
        Media_Valutazioni_Libro_Venditore.media_valutazione  # Media delle valutazioni dalla vista
    ).join(
        Venditore_Libro, Libri.id_libro == Venditore_Libro.id_libro
    ).join(
        Media_Valutazioni_Libro_Venditore,
        (Libri.id_libro == Media_Valutazioni_Libro_Venditore.id_libro) &
        (Venditore_Libro.id_venditore == Media_Valutazioni_Libro_Venditore.id_venditore)
    ).join(
        Utente, Venditore_Libro.id_venditore == Utente.email
    ).order_by(
        Media_Valutazioni_Libro_Venditore.media_valutazione.desc()  # Ordina per media valutazione decrescente
    ).limit(4).all()

    return render_template('solo_compratore.html', editori=editori, categorie=categorie, top_books=top_books,
                           top_recensioni=top_recensioni, notifiche_attive=notifiche_attive)


# noinspection LanguageDetectionInspection
@app.route('/search_books', methods=['POST'])
@login_required
def search_books():
    editori = db.session.query(Libri.casa_editrice).distinct().all()
    categorie = db.session.query(Categoria.nome_categoria).all()
    query = request.form.get('query', '').strip()
    editore = request.form.get('editore', '').strip()
    categoria = request.form.get('categoria', '').strip()
    prezzo_min = request.form.get('prezzo_min', '').strip()
    prezzo_max = request.form.get('prezzo_max', '').strip()

    filters = []

    if query:
        # Ricerca parziale nel titolo
        filters.append(Libri.titolo.ilike(f"%{query}%"))

    if editore:
        # Filtra per casa editrice
        filters.append(Libri.casa_editrice.ilike(f"%{editore}%"))

    if categoria:
        # Filtra per categoria
        filters.append(Libri.nome_categoria.ilike(f"%{categoria}%"))

    if prezzo_min:
        # Filtra per prezzo minimo
        filters.append(Venditore_Libro.prezzo >= float(prezzo_min))

    if prezzo_max:
        # Filtra per prezzo massimo
        filters.append(Venditore_Libro.prezzo <= float(prezzo_max))

    # Costruzione della query
    results = db.session.query(
        Libri.id_libro,
        Libri.titolo,
        Libri.casa_editrice,
        Libri.anno,
        Utente.nome,
        Utente.cognome,
        Utente.email,
        Venditore_Libro.prezzo,
        Venditore_Libro.quantita,
        Venditore_Libro.stato_nuovo,
        Venditore_Libro.id_venditore,
        Media_Valutazioni_Libro_Venditore.media_valutazione  # Assicurati che questa colonna esista nella vista
    ).join(
        Venditore_Libro, Libri.id_libro == Venditore_Libro.id_libro
    ).join(
        Utente, Venditore_Libro.id_venditore == Utente.email
    ).outerjoin(
        Media_Valutazioni_Libro_Venditore,  # Utilizza il nome della vista corretta
        (Libri.id_libro == Media_Valutazioni_Libro_Venditore.id_libro) &
        (Venditore_Libro.id_venditore == Media_Valutazioni_Libro_Venditore.id_venditore)
        # Usa & per combinare le condizioni
    ).filter(
        Venditore_Libro.quantita != 0,
        Venditore_Libro.id_venditore != current_user.email
    ).filter(*filters).all()

    return render_template('search_results.html', query=query, results=results, editori=editori, categorie=categorie,
                           cosa_sono=current_user.venditore)


@app.route('/info_product/<int:id_libro>/<string:id_venditore>', methods=['GET', 'POST'])
@login_required
def info_libro(id_libro, id_venditore):
    cosa_sono = current_user.venditore

    libro_selezionato = db.session.query(
        Venditore_Libro.stato_nuovo,
        Venditore_Libro.prezzo,
        Venditore_Libro.quantita,
        Libri.edizione,
        Libri.titolo,
        Libri.casa_editrice,
        Libri.anno,
        Libri.descrizione,
        Libri.nome_categoria,
        Autore.nome,
        Autore.cognome,
        Libri.id_libro,
        Venditore_Libro.id_venditore,
        Utente.nome.label('nome_venditore'),
        Utente.cognome.label('cognome_venditore'),
        Media_Valutazioni_Libro_Venditore.media_valutazione  # Aggiungi la media delle valutazioni
    ).join(
        Libri, Libri.id_libro == Venditore_Libro.id_libro
    ).join(
        Autore, Autore.id_autore == Libri.id_autore
    ).join(
        Utente, Venditore_Libro.id_venditore == Utente.email
    ).outerjoin(
        Media_Valutazioni_Libro_Venditore,  # Utilizza il nome della vista corretta
        (Libri.id_libro == Media_Valutazioni_Libro_Venditore.id_libro) &
        (Venditore_Libro.id_venditore == Media_Valutazioni_Libro_Venditore.id_venditore)
        # Usa & per combinare le condizioni
    ).filter(
        Venditore_Libro.id_libro == id_libro,
        Venditore_Libro.id_venditore == id_venditore
    ).first()

    recensioni_libro = db.session.query(
        Recensioni
    ).filter(
        Recensioni.id_libro == id_libro, Recensioni.id_venditore == id_venditore
    )
    return render_template('info_product.html', libro=libro_selezionato, cosa_sono=cosa_sono,
                           recensioni_libro=recensioni_libro)


@app.route('/recensioni/<int:id_libro>/<string:id_venditore>', methods=['GET'])
@login_required
def tutte_recensioni_libro(id_libro, id_venditore):
    cosa_sono = current_user.venditore
    # Esegui la query per ottenere tutte le recensioni del libro specificato e del venditore specificato
    recensioni_libro = db.session.query(
        Recensioni,
        Libri
    ).join(
        Libri, Recensioni.id_libro == Libri.id_libro
    ).filter(
        Recensioni.id_libro == id_libro,
        Recensioni.id_venditore == id_venditore
    ).all()

    # Verifica se ci sono recensioni
    if not recensioni_libro:
        flash("Nessuna recensione trovata per questo libro", "warning")
        return redirect(url_for('info_libro', id_libro=id_libro, id_venditore=id_venditore))

    # Prendi le informazioni del libro (presente in tutte le tuple)
    libro_info = recensioni_libro[0][1]  # Il secondo elemento della tupla contiene l'oggetto 'Libri'

    return render_template('tutte_recensioni_libro.html', recensioni_libro=recensioni_libro, libro=libro_info,
                           cosa_sono=cosa_sono, id_venditore=id_venditore)


@app.route('/user_profile')
@login_required
def user_profile():
    # Qui metti la logica per il rendering della pagina user_profile.html
    return render_template('user_profile.html', user=current_user, cosa_sono=current_user.venditore)


@app.route('/solo_venditore')
@login_required
def solo_venditore():
    notifiche_attive = Ordini.query.filter_by(id_utente=current_user.email, notifica_attiva=True).first()

    editori = db.session.query(Libri.casa_editrice).distinct().all()
    categorie = db.session.query(Categoria.nome_categoria).all()

    if current_user.venditore:
        # Recupera le ultime 3-4 vendite del venditore
        vendite_recenti = db.session.query(
            Ordini.id_ordine,
            Ordini.id_libro,
            Ordini.quantita,
            Ordini.data,
            Libri.titolo,
            Utente.nome,
            Utente.cognome
        ).join(Libri, Ordini.id_libro == Libri.id_libro) \
            .join(Utente, Ordini.id_utente == Utente.email) \
            .filter(Ordini.id_venditore == current_user.email) \
            .order_by(Ordini.data.desc()) \
            .limit(4) \
            .all()
    else:
        vendite_recenti = None

    libri_vetrina = db.session.query(
        Venditore_Libro.quantita,
        Venditore_Libro.prezzo,
        Venditore_Libro.id_venditore,
        Libri.titolo,
        Autore.nome,  # Nome dell'autore
        Autore.cognome  # Cognome dell'autore
    ).join(Libri, Venditore_Libro.id_libro == Libri.id_libro) \
        .join(Autore, Libri.id_autore == Autore.id_autore) \
        .filter(Venditore_Libro.quantita > 0) \
        .filter(Venditore_Libro.id_venditore == current_user.email) \
        .limit(4) \
        .all()

    top_books = (
        db.session.query(Libri, func.count(Recensioni.id_recensione).label('total_reviews'))
        .join(Recensioni, Libri.id_libro == Recensioni.id_libro)
        .group_by(Libri.id_libro)
        .order_by(func.count(Recensioni.id_recensione).desc())
        .limit(4)
        .all()
    )

    top_recensioni = db.session.query(
        Libri.id_libro,
        Libri.titolo,
        Venditore_Libro.id_venditore,
        Utente.nome.label('nome_venditore'),
        Utente.cognome.label('cognome_venditore'),
        Media_Valutazioni_Libro_Venditore.media_valutazione  # Media delle valutazioni dalla vista
    ).join(
        Venditore_Libro, Libri.id_libro == Venditore_Libro.id_libro
    ).join(
        Media_Valutazioni_Libro_Venditore,
        (Libri.id_libro == Media_Valutazioni_Libro_Venditore.id_libro) &
        (Venditore_Libro.id_venditore == Media_Valutazioni_Libro_Venditore.id_venditore)
    ).join(
        Utente, Venditore_Libro.id_venditore == Utente.email
    ).order_by(
        Media_Valutazioni_Libro_Venditore.media_valutazione.desc()  # Ordina per media valutazione decrescente
    ).limit(4).all()

    return render_template('solo_venditore.html', vendite_recenti=vendite_recenti, editori=editori, categorie=categorie,
                           libri_vetrina=libri_vetrina, top_books=top_books, top_recensioni=top_recensioni, notifiche_attive=notifiche_attive)


@app.route('/vendite')
@login_required
def vendite():
    if not current_user.venditore:
        flash('Solo i venditori possono vedere le loro vendite.')
        return redirect(url_for('solo_compratore'))

    # Recupera le vendite effettuate dal venditore
    vendite = db.session.query(
        Ordini.id_ordine,
        Ordini.id_libro,
        Ordini.quantita,
        Ordini.stato,
        Libri.titolo,
        Ordini.data,
        Utente.nome,
        Utente.cognome
    ).join(Libri, Ordini.id_libro == Libri.id_libro) \
        .join(Utente, Ordini.id_utente == Utente.email) \
        .filter(Ordini.id_venditore == current_user.email) \
        .all()

    return render_template('vendite.html', vendite=vendite)


def crea_o_trova_autore(nome, cognome, anno_nascita=None, descrizione=None):
    autore = Autore.query.filter_by(nome=nome, cognome=cognome).first()
    if not autore:
        autore = Autore(nome=nome, cognome=cognome, anno_nascita=anno_nascita, descrizione=descrizione)
        db.session.add(autore)
        db.session.commit()
    return autore


def crea_o_trova_categoria(nome_categoria):
    categoria = Categoria.query.filter_by(nome_categoria=nome_categoria).first()
    if not categoria:
        categoria = Categoria(nome_categoria=nome_categoria)
        db.session.add(categoria)
        db.session.commit()
    return categoria


@app.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    if not current_user.venditore:
        flash('Solo i venditori possono aggiungere libri.')
        return redirect(url_for('solo_compratore'))

    # Recupera tutti gli autori e categorie dal database
    libri = db.session.query(Libri).all()
    autori = Autore.query.all()
    categorie = Categoria.query.all()

    if request.method == 'POST':
        titolo = request.form.get('titolo')
        edizione = request.form.get('edizione', type=int)
        anno = request.form.get('anno', type=int)
        descrizione = request.form.get('descrizione')
        casa_editrice = request.form.get('casa_editrice')
        quantita = request.form.get('quantita', type=int)
        prezzo = request.form.get('prezzo', type=float)
        stato_nuovo = request.form.get('stato_nuovo') == 'Si'
        autore_nome = request.form.get('autore_nome')
        autore_cognome = request.form.get('autore_cognome')
        autore_anno_nascita = request.form.get('autore_anno_nascita', type=int)
        autore_descrizione = request.form.get('autore_descrizione')
        categoria_nome = request.form.get('categoria_nome')

        # Usa la funzione per creare o trovare l'autore
        autore = crea_o_trova_autore(
            nome=autore_nome,
            cognome=autore_cognome,
            anno_nascita=autore_anno_nascita,
            descrizione=autore_descrizione
        )

        # Usa la funzione per creare o trovare la categoria
        categoria = crea_o_trova_categoria(nome_categoria=categoria_nome)

        # Verifica se esiste già un libro con le stesse specifiche (titolo, edizione, anno, casa editrice)
        libro = Libri.query.filter_by(
            titolo=titolo,
            edizione=edizione,
            anno=anno,
            casa_editrice=casa_editrice
        ).first()

        if libro:
            # Se il libro esiste, controlla che l'autore sia lo stesso
            if libro.id_autore != autore.id_autore:
                flash(
                    'Esiste già un libro con questo titolo, edizione, anno e casa editrice, ma con un autore diverso.')
                return redirect(url_for('add_book'))

            # Controlla se questo venditore ha già messo in vendita questo libro con le stesse specifiche
            venditore_libro = Venditore_Libro.query.filter_by(
                id_libro=libro.id_libro,
                id_venditore=current_user.email,
                prezzo=prezzo,
                stato_nuovo=stato_nuovo
            ).first()

            if venditore_libro:
                # Se il venditore ha già una vendita per questo libro con le stesse specifiche, aggiorna la quantità
                venditore_libro.quantita += quantita
                db.session.commit()
                flash('Quantità aggiornata per il libro esistente!')
            else:
                # Se il venditore non ha ancora una vendita per questo libro, crea una nuova voce
                venditore_libro = Venditore_Libro(
                    id_libro=libro.id_libro,
                    id_venditore=current_user.email,
                    quantita=quantita,
                    prezzo=prezzo,
                    stato_nuovo=stato_nuovo
                )
                db.session.add(venditore_libro)
                db.session.commit()
        else:
            # Se il libro non esiste, crea una nuova voce per il libro e per la vendita
            libro = Libri(
                titolo=titolo,
                edizione=edizione,
                anno=anno,
                descrizione=descrizione,
                casa_editrice=casa_editrice,
                id_autore=autore.id_autore,
                nome_categoria=categoria.nome_categoria
            )
            db.session.add(libro)
            db.session.commit()

            # Aggiungi il nuovo libro al venditore
            venditore_libro = Venditore_Libro(
                id_libro=libro.id_libro,
                id_venditore=current_user.email,
                quantita=quantita,
                prezzo=prezzo,
                stato_nuovo=stato_nuovo
            )
            db.session.add(venditore_libro)
            db.session.commit()

        return redirect(url_for('solo_venditore'))

    return render_template('add_book.html', autori=autori, categorie=categorie, libri=libri)


@app.route('/libri_in_vendita')
@login_required
def libri_in_vendita():
    if not current_user.venditore:
        flash('Solo i venditori possono accedere a questa pagina.')
        return redirect(url_for('solo_compratore'))

    libri = (db.session.query(
        Venditore_Libro,
        Libri,
        Autore.nome.label('nome_autore'),  # Nome dell'autore
        Autore.cognome.label('cognome_autore')  # Cognome dell'autore
    ).join(Libri, Venditore_Libro.id_libro == Libri.id_libro)
             .join(Autore, Libri.id_autore == Autore.id_autore)
             .filter(Venditore_Libro.id_venditore == current_user.email)
             .filter(Venditore_Libro.quantita != 0)
             .all())

    return render_template('libri_in_vendita.html', libri_in_vendita=libri)


def crea_o_trova_carrello(user_id):
    carrello = Carrello.query.filter_by(id_utente=user_id).first()
    if not carrello:
        carrello = Carrello(id_utente=user_id)
        db.session.add(carrello)
        db.session.commit()
    return carrello


@app.route('/aggiungi_al_carrello', methods=['POST'])
@login_required
def aggiungi_al_carrello():
    cosa_sono = current_user.venditore
    id_libro = request.form.get('id_libro')
    id_venditore = request.form.get('id_venditore')
    quantita = request.form.get('quantita', type=int)

    carrello = crea_o_trova_carrello(current_user.email)

    aggiungi = Libri_Carrello.query.filter_by(id_carrello=carrello.id_carrello, id_venditore=id_venditore,
                                              id_libro=id_libro).first()
    libro_vendita = Venditore_Libro.query.filter_by(id_libro=id_libro).first()

    if aggiungi:
        if quantita + aggiungi.quantita <= libro_vendita.quantita:
            aggiungi.quantita += quantita
        else:
            flash('Quantità non disponibile!', 'error')
    else:
        aggiungi = Libri_Carrello(id_libro=id_libro, id_carrello=carrello.id_carrello, id_venditore=id_venditore,
                                  quantita=quantita)
        db.session.add(aggiungi)

    db.session.commit()
    return redirect(url_for('info_libro', id_libro=id_libro, id_venditore=id_venditore))


@app.route('/carrello')
@login_required
def carrello():
    cosa_sono = current_user.venditore
    carrello_corrente = Carrello.query.filter_by(id_utente=current_user.email).first()

    if carrello_corrente:
        libri_carrello = db.session.query(
            Libri_Carrello.id_libro,
            Libri_Carrello.id_venditore,
            Libri_Carrello.quantita,
            Libri.titolo,
            Venditore_Libro.prezzo,
            (Venditore_Libro.quantita - Libri_Carrello.quantita).label('qta_rimasta')
        ).join(
            Libri, Libri_Carrello.id_libro == Libri.id_libro
        ).join(
            Venditore_Libro, (Libri_Carrello.id_libro == Venditore_Libro.id_libro) & (
                    Libri_Carrello.id_venditore == Venditore_Libro.id_venditore)
        ).filter(
            Libri_Carrello.id_carrello == carrello_corrente.id_carrello
        ).all()
    else:
        libri_carrello = []

    # Recupera l'indirizzo di spedizione dell'utente
    utente = db.session.query(Utente).filter_by(email=current_user.email).first()
    if not utente:
        flash("Errore: utente non trovato.")
        return redirect(url_for('index'))

    indirizzo_spedizione_predefinito = utente.indirizzo

    return render_template('carrello.html', libri_carrello=libri_carrello,
                           indirizzo_spedizione_predefinito=indirizzo_spedizione_predefinito, cosa_sono=cosa_sono)


@app.route('/elimina_libro_carrello/<int:id_libro>/<string:id_venditore>', methods=['GET', 'POST'])
@login_required
def elimina_libro_carrello(id_libro, id_venditore):
    # Trova il carrello dell'utente corrente
    carrello = db.session.query(Carrello).filter_by(id_utente=current_user.email).first()

    if carrello:
        # Trova il libro nel carrello da eliminare
        libro_carrello = db.session.query(Libri_Carrello).filter_by(
            id_libro=id_libro,
            id_venditore=id_venditore,
            id_carrello=carrello.id_carrello
        ).first()

        # Elimina il libro dal carrello
        db.session.delete(libro_carrello)
        db.session.commit()

    return redirect(url_for('carrello'))  # Redireziona alla pagina del carrello


@app.route('/riepilogo_ordine/<int:id_libro>/<string:id_venditore>', methods=['GET', 'POST'])
@login_required
def riepilogo_ordine(id_libro, id_venditore):
    # Recupera l'utente corrente
    utente = current_user

    # Recupera il libro e il venditore associato
    venditore_libro = Venditore_Libro.query.filter_by(id_libro=id_libro, id_venditore=id_venditore).first()

    if not venditore_libro:
        flash("Libro o venditore non trovato.", "danger")
        return redirect(url_for('carrello'))

    # Recupera il libro dalla tabella Libri
    libro = Libri.query.get(id_libro)

    if not libro:
        flash("Il libro non esiste.", "danger")
        return redirect(url_for('carrello'))

    # Se l'utente ha già un indirizzo, lo usa di default
    indirizzo_spedizione = utente.indirizzo if utente.indirizzo else ''

    # Recupera la quantità che acquisto
    quantita_carrello = db.session.query(
        Libri_Carrello.quantita,
    ).join(
        Carrello, Libri_Carrello.id_carrello == Carrello.id_carrello
    ).filter(
        Carrello.id_utente == current_user.email
    ).first()

    # Mostra la pagina di riepilogo
    return render_template('riepilogo_ordine.html', venditore_libro=venditore_libro, libro=libro, utente=utente,
                           indirizzo_spedizione=indirizzo_spedizione, cosa_sono=current_user.venditore, quantita_carrello=quantita_carrello[0])


@app.route('/crea_ordine/<int:id_libro>/<string:id_venditore>', methods=['POST'])
@login_required
def crea_ordine(id_libro, id_venditore):
    # Recupera l'utente corrente
    utente = current_user

    # Recupera il libro dal carrello
    carrello_corrente = Carrello.query.filter_by(id_utente=utente.email).first()
    libro_carrello = Libri_Carrello.query.filter_by(id_carrello=carrello_corrente.id_carrello,
                                                    id_libro=id_libro,
                                                    id_venditore=id_venditore).first()

    if not libro_carrello:
        flash("Il libro non esiste nel carrello.", "danger")
        return redirect(url_for('carrello'))

    # Recupera il venditore e verifica disponibilità
    venditore_libro = Venditore_Libro.query.filter_by(id_libro=id_libro, id_venditore=id_venditore).first()

    if not venditore_libro or venditore_libro.quantita < libro_carrello.quantita:
        flash("Quantità non disponibile o venditore non trovato.", "danger")
        return redirect(url_for('carrello'))

    # Recupera i dati dal form
    indirizzo_spedizione = request.form.get('indirizzo_spedizione')
    metodo_pagamento = request.form.get('metodo_pagamento')

    # Crea l'ordine
    nuovo_ordine = Ordini(
        data=datetime.today(),
        id_utente=utente.email,
        indirizzo_spedizione=indirizzo_spedizione,
        id_libro=id_libro,
        id_venditore=id_venditore,
        stato='In elaborazione',
        quantita=libro_carrello.quantita,
        metodo_pagamento=metodo_pagamento
    )
    db.session.add(nuovo_ordine)

    # Decrementa la quantità del libro nel database venditore_libro
    venditore_libro.quantita -= libro_carrello.quantita

    # Rimuovi il libro dal carrello
    db.session.delete(libro_carrello)

    # Commit delle operazioni
    db.session.commit()

    return redirect(url_for('visualizza_ordini'))


@app.route('/visualizza_ordini', methods=['GET'])
@login_required
def visualizza_ordini():
    # Recupera l'utente corrente
    utente = current_user

    # Recupera tutti gli ordini effettuati dall'utente corrente
    # ordini = Ordini.query.filter_by(id_utente=utente.email).all()

    ordini = (
        db.session.query(Ordini, Libri)
        .join(Libri, Ordini.id_libro == Libri.id_libro)
        .filter(Ordini.id_utente == utente.email)
        .all()
    )

    recensioni_esistenti = {recensione.id_libro for recensione in
                            Recensioni.query.filter_by(id_utente=utente.email).all()}

    # Mostra la pagina con la lista degli ordini
    return render_template('visualizza_ordini.html', ordini=ordini, cosa_sono=current_user.venditore,
                           recensioni_esistenti=recensioni_esistenti)


@app.route('/inserisci_recensione/<int:id_libro>/<id_venditore>', methods=['GET', 'POST'])
@login_required
def inserisci_recensione(id_libro, id_venditore):
    cosa_sono = current_user.venditore

    if request.method == 'POST':
        valutazione = request.form['valutazione']
        descrizione = request.form['descrizione']

        # Creazione della recensione
        nuova_recensione = Recensioni(
            valutazione=valutazione,
            id_libro=id_libro,
            id_utente=current_user.email,
            id_venditore=id_venditore,
            descrizione=descrizione
        )
        db.session.add(nuova_recensione)
        db.session.commit()

        return redirect(url_for('visualizza_ordini'))  # Puoi reindirizzare a una pagina di conferma o agli ordini

    libro = Libri.query.get(id_libro)  # Puoi anche ottenere il titolo del libro per mostrarlo nella pagina
    return render_template('crea_recensione.html', libro=libro, cosa_sono=cosa_sono)


@app.route('/le_mie_recensioni', methods=['GET'])
@login_required
def le_mie_recensioni():
    cosa_sono = current_user.venditore
    utente = current_user
    is_venditore = current_user.venditore

    # Recupera le recensioni effettuate dall'utente con il titolo del libro
    mie_recensioni = db.session.query(Recensioni, Libri.titolo).join(Libri,
                                                                     Recensioni.id_libro == Libri.id_libro).filter(
        Recensioni.id_utente == utente.email).all()
    # Se l'utente è un venditore, recupera anche le recensioni ricevute con il titolo del libro
    mie_recensioni_ricevute = []
    if utente.venditore:
        mie_recensioni_ricevute = db.session.query(Recensioni, Libri.titolo).join(Libri,
                                                                                  Recensioni.id_libro == Libri.id_libro).filter(
            Recensioni.id_venditore == utente.email).all()

    return render_template('le_mie_recensioni.html', mie_recensioni=mie_recensioni,
                           mie_recensioni_ricevute=mie_recensioni_ricevute, is_venditore=is_venditore,
                           cosa_sono=cosa_sono)


@app.route('/update_order_status', methods=['POST'])
@login_required
def update_order_status():
    book_id = request.form['id_libro']
    order_id = request.form['id_ordine']
    nuovo_stato = request.form['stato']

    # Aggiorna lo stato ordine nel database
    ordine = Ordini.query.get((order_id, book_id))
    if ordine:
        ordine.stato = nuovo_stato
        db.session.commit()  # Salva le modifiche al database
        flash('Stato ordine aggiornato con successo!', 'success')
    else:
        flash('Ordine non trovato!', 'error')

    return redirect(url_for('vendite'))  # Reindirizza alla pagina principale


@app.route('/check_email')
def check_email():
    email = request.args.get('email')
    exists = db.session.query(Ordini).filter_by(email=email).first() is not None
    return jsonify({'exists': exists})


@app.route('/elimina_libro', methods=['POST'])
@login_required
def elimina_libro():
    id_libro = request.form['id_libro']

    # Trova il libro nel database per il venditore corrente
    libro = Venditore_Libro.query.filter_by(id_libro=id_libro, id_venditore=current_user.email).first()
    if libro:
        libro.quantita = 0  # Imposta la quantità a 0
        db.session.commit()  # Salva le modifiche
        flash('Quantità del libro impostata a 0 con successo!', 'success')
    else:
        flash('Libro non trovato o non sei autorizzato a eliminarlo!', 'error')

    return redirect(url_for('libri_in_vendita'))  # Torna alla pagina dei libri


@app.route('/modifica_profilo', methods=['POST'])
@login_required
def modifica_profilo():
    user = Utente.query.filter_by(email=current_user.email).first()

    if user:
        user.nome = request.form['nome']
        user.cognome = request.form['cognome']

        # Handle empty date field
        data_nascita = request.form.get('data_nascita')
        if data_nascita:  # Only update if not empty
            user.data_nascita = data_nascita
        else:
            user.data_nascita = None  # Set to NULL in the database if empty

        user.indirizzo = request.form.get('indirizzo') or None
        # Gestione del campo telefono
        telefono = request.form.get('telefono')
        if telefono:
            try:
                user.telefono = int(telefono)  # Converti in intero
            except ValueError:
                user.telefono = None  # Imposta a None se la conversione fallisce
        else:
            user.telefono = None  # Imposta a None se vuoto

        db.session.commit()

    return redirect(url_for('user_profile'))


@app.route('/chiudi_notifiche', methods=['POST'])
@login_required
def chiudi_notifiche():
    # Assicurati che l'utente sia autenticato
    if current_user.is_authenticated:
        # Esegui la query per impostare le notifiche attive a False per l'utente
        # Esempio:

        db.session.query(Ordini).filter_by(id_utente=current_user.email).update({"notifica_attiva": False})
        db.session.commit()

        # Puoi anche restituire un redirect per tornare alla pagina corrente
    return redirect(request.referrer)  # Torna alla pagina precedente

if __name__ == '__main__':
    app.run()
