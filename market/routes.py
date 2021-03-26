from market import app, db
from flask import render_template, redirect, url_for, flash
from market.models import Item, User
from market.forms import RegisterForm, LoginForm
from flask_login import login_user


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
    if form.errors != {}:  # se não tiver erro de validação
        for err_msg in form.errors.values():
            flash(f'Houve um erro na criação do usuário: {err_msg}', category='danger')
    return render_template('cadastro.html', form=form)


@app.route('/acesso', methods=['GET', 'POST'])
def acesso():
    form = LoginForm()
    if form.validate_on_submit():
        tentiva_usuario = User.query.filter_by(username=form.username.data).first()
        if tentiva_usuario and tentiva_usuario.verifica_password(tentiva_acesso=form.password.data):
            login_user(tentiva_usuario)
            flash(f'Bem vindo a Curitibread. Voce está acessando como {tentiva_usuario.username}', category='success')
            return redirect(url_for('loja'))
        else:
            flash('Usuário ou senha incorretos, tente novamente', category='danger')

    return render_template('acesso.html', form=form)
