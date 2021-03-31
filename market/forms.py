from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User


class RegisterForm(FlaskForm):
    def validate_username(self, checa_usuario):
        usuario = User.query.filter_by(username=checa_usuario.data).first()
        if usuario:
            raise ValidationError('Usuário já existente. Escolha outro usuário.')

    def validate_email_address(self, checa_email):
        email = User.query.filter_by(email_address=checa_email.data).first()
        if email:
            raise ValidationError('Este e-mail já está em uso. Escolha outro e-mail.')

    username = StringField(label='Usuário:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Endereço de E-mail:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Senha com no mínimo 6 caracteres:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirme a Senha:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Criar Conta')


class ProductForm(FlaskForm):
    produto = StringField(label='Usuário:')
    cod_barras = StringField(label='Endereço de E-mail:',)
    preco = StringField(label='Senha:')
    descricao = StringField(label='Confirme a Senha:')
    opcoes = StringField(label='Criar Conta')


class LoginForm(FlaskForm):
    username = StringField(label='Usuário', validators=[DataRequired()])
    password = PasswordField(label='Senha', validators=[DataRequired()])
    submit = SubmitField(label='Entrar')


class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Comprar')


class SellItemForm(FlaskForm):
    submit = SubmitField(label='Vender')
