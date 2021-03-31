from market import app, db
from flask import render_template, redirect, url_for, flash, request
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
@app.route('/index')
def pagina_inicial():
	return render_template('index.html')


@app.route('/loja', methods=['GET', 'POST'])
@login_required
def loja():
	formulario_compra = PurchaseItemForm()
	if request.method == 'POST':
		item_comprado = request.form.get('item_comprado')
		c_item_object = Item.query.filter_by(name=item_comprado).first()
		if c_item_object:
			if current_user.pode_comprar(c_item_object):
				c_item_object.owner = current_user.id
				current_user.budget -= c_item_object.price
				db.session.commit()
				flash(f'Parabéns! Você acabou de adquirir: {c_item_object.name} por {c_item_object.price}', category='success')
			else:
				flash(f'O seu saldo não é suficiente para comprar {c_item_object.name}', category='danger')
		return redirect(url_for('loja'))

	if request.method == 'GET':
		items = Item.query.filter_by(owner=None)
		return render_template('loja.html', items=items, formulario_compra=formulario_compra)


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
	form = RegisterForm()
	if form.validate_on_submit():
		criar_usuario = User(username=form.username.data, email_address=form.email_address.data, password=form.password1.data)
		db.session.add(criar_usuario)
		db.session.commit()
		login_user(criar_usuario)
		flash(f'Conta criada com sucesso e você está acessando como: {criar_usuario.username}', category='success')
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
			flash(f'Bem vindo a Curitibread. Você está acessando como {tentiva_usuario.username}', category='success')
			return redirect(url_for('loja'))
		else:
			flash('Usuário ou senha incorretos, tente novamente', category='danger')

	return render_template('acesso.html', form=form)


@app.route('/desconectar', methods=['GET', 'POST'])
def desconectar():
	logout_user()
	flash('Você foi desconectado!', category='info')
	return redirect(url_for('pagina_inicial'))


@app.route('/sobre')
def sobre():
	return render_template('sobre.html')
