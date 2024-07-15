from flask import Flask, render_template, flash, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Table, MetaData, Column, Integer, String, ForeignKey, Boolean, Float, Date
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'usersecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:basi@localhost/progettoBasi'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)


class Utente(db.Model, UserMixin):
    __tablename__ = 'utente'
    email = Column(String(50), primary_key=True, nullable=False)
    nome = Column(String(50))
    cognome = Column(String(50))
    telefono = Column(Integer)
    password = Column(String(50), nullable=False)
    venditore = Column(Boolean, nullable=False)
    data_nascita = Column(Date)

    def __init__(self, email, nome, cognome, telefono, password, data_nascita):
        self.email = email
        self.nome = nome
        self.cognome = cognome
        self.telefono = telefono
        self.password = password
        self.data_nascita = data_nascita


class Libri(db.Model):
    __tablename__ = 'libri'
    id_libro = Column(Integer, primary_key=True, nullable=False)
    edizione = Column(Integer)
    anno = Column(Integer)
    titolo = Column(String(50), nullable=False)
    descrizione = Column(String(400))
    casa_editrice = Column(String(50))


class Autore(db.Model):
    __tablename__ = 'autore'
    id_autore = Column(Integer, primary_key=True, nullable=False)
    anno_nascita = Column(Integer)
    nome = Column(String(50))
    cognome = Column(String(50))
    descrizione = Column(String(400))


class Autore_Libro(db.Model):
    __tablename__ = 'autore_libro'
    id_libro = Column(Integer, ForeignKey('libri.id_libro'), primary_key=True, nullable=False)
    id_autore = Column(Integer, ForeignKey('autore.id_autore'), primary_key=True, nullable=False)


class Categoria(db.Model):
    __tablename__ = 'categoria'
    nome_categoria = Column(String(50), primary_key=True, nullable=False)


class Categoria_Libro(db.Model):
    __tablename__ = 'categoria_libro'
    id_libro = Column(Integer, ForeignKey('libro.id_libro'), primary_key=True, nullable=False)
    id_categoria = Column(String(50), ForeignKey('categoria.nome_categoria'), primary_key=True, nullable=False)


class Ordini(db.Model):
    __tablename__ = 'ordini'
    id_ordini = Column(Integer, primary_key=True, nullable=False)
    data = Column(Date, nullable=False)
    id_utente = Column(String(50), ForeignKey('utente.id_utente'), nullable=False)


class Stato_Ordine(db.Model):
    __tablename__ = 'stato_ordine'
    id_stato = Column(String(50), primary_key=True, nullable=False)


class Composizione_Ordine(db.Model):
    __tablename__ = 'composizione_ordine'
    id_ordine = Column(Integer, primary_key=True, nullable=False)
    id_libro = Column(Integer, ForeignKey('libro.id_libro'), primary_key=True, nullable=False)
    quantita = Column(Integer, nullable=False)
    id_stato = Column(String(50), ForeignKey('stato_ordine.id_stato'), nullable=False)


class Venditore_Libro(db.Model):
    __tablename__ = 'venditore_libro'
    id_libro = Column(Integer, ForeignKey('libro.id_libro'), primary_key=True, nullable=False)
    id_venditore = Column(String(50), ForeignKey('utente.email'), primary_key=True, nullable=False)
    quantita = Column(Integer, nullable=False)
    prezzo = Column(Float, nullable=False)


class Carrello(db.Model):
    __tablename__ = 'carrello'
    id_carrello = Column(Integer, primary_key=True, nullable=False)
    id_utente = Column(String(50), ForeignKey('utente.id_utente'), nullable=False)


class Libri_Carello(db.Model):
    __tablename__ = 'libri_carello'
    id_libro = Column(Integer, ForeignKey('libro.id_libro'), primary_key=True, nullable=False)
    id_carrello = Column(Integer, ForeignKey('carrello.id_carrello'), primary_key=True, nullable=False)
    quantita = Column(Integer, nullable=False)


class Recensioni(db.Model):
    __tablename__ = 'recensioni'
    id_recensioni = Column(Integer, primary_key=True, nullable=False)
    valutazione = Column(Integer, nullable=False)
    id_libro = Column(Integer, ForeignKey('libro.id_libro'), nullable=False)
    id_utente = Column(String(50), ForeignKey('utente.id_utente'), nullable=False)
    descrizione = Column(String(400))


@login_manager.user_loader
def load_user(email):
    return Utente.query.get(email)


@app.route('/')
def start():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
