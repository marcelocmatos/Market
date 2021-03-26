from market import app, db
from flask import render_template, redirect, url_for, flash
from market.models import Item, User
from market.forms import RegisterForm


@app.route('/')
@app.route('/index')
def pagina_inicial():
    return render_template('index.html')


@app.route('/loja')
def loja():
    items = Item.query.all()
    return render_template('loja.html', itens=items)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form = RegisterForm()
    if form.validate_on_submit():
        criar_usuario = User(username=form.username.data,
                             email_address=form.email_address.data,
                             password=form.password1.data)
        db.session.add(criar_usuario)
        db.session.commit()
        return redirect(url_for('loja'))
    if form.errors != {}: #se não tiver erro de validação
        for err_msg in form.errors.values():
            flash(f'Houve um erro na criação do usuário: {err_msg}', category='danger')
    return render_template('cadastro.html', form=form)

@app.route('/acesso', methods=['GET', 'POST'])
def acesso():

    return render_template('acesso.html')