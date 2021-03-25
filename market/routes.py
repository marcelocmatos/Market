from market import app
from flask import render_template
from market.models import Item
from market.forms import RegisterForm


@app.route('/')
@app.route('/index')
def pagina_inicial():
    return render_template('index.html')


@app.route('/loja')
def loja():
    items = Item.query.all()
    return render_template('loja.html', itens=items)

@app.route('/register')
def register_page():
    form = RegisterForm()
    return render_template('register.html', form=form)