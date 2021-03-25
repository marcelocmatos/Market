from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField


class RegisterForm(FlaskForm):
    username = StringField(label='Usuário:')
    email_address = StringField(label='Endereço de E-mail:',)
    password1 = PasswordField(label='Senha:')
    password2 = PasswordField(label='Confirme a Senha:')
    submit = SubmitField(label='Criar Conta')
