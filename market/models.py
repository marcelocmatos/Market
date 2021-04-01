from market import db, bcrypt, login_manager
from flask_login import UserMixin
import locale


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship('Item', backref='owned_user', lazy=True)

    @property
    def corrige_formato_dinheiro(self):
        if self.budget:
            locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
            valor = locale.currency(self.budget, grouping=True)
            return valor
        else:
            locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
            valor = locale.currency(self.budget, grouping=True)
            return valor

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, texto_password):
        self.password_hash = bcrypt.generate_password_hash(texto_password).decode('utf-8')

    def verifica_password(self, tentiva_acesso):
        return bcrypt.check_password_hash(self.password_hash, tentiva_acesso)

    def pode_comprar(self, item_obj):
        return self.budget >= item_obj.price

    def pode_devolver(self, item_obj):
        return item_obj in self.items


class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=100), nullable=False, unique=False)
    price = db.Column(db.Integer(), nullable=False, unique=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=False)
    description = db.Column(db.String(length=4096), nullable=False, unique=False)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Item{self.name}'

    def comprar(self, usuario):
        self.owner = usuario.id
        usuario.budget -= self.price
        db.session.commit()

    def vender(self, usuario):
        self.owner = None
        usuario.budget += self.price
        db.session.commit()


class Corrigir:
    def __init__(self, dinheiro):
        self.dinheiro = dinheiro

    def corrige_formato_dinheiro(self):
        valor = self
        valor = int(valor)
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        valor = locale.currency(valor, grouping=True)
        return valor
