from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, DateField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, URL


class MessageForm(FlaskForm):
    """ Форма отправки сообщения """
    name = StringField('Имя', [DataRequired()])
    email = StringField('Почта', [Email(message='Введите правильный адрес почты'), DataRequired()])
    body = TextAreaField('Сообщение', [DataRequired(), Length(min=4, message='Ваше сообщение слишком короткое')])
    recaptcha = RecaptchaField()
    submit = SubmitField('Отправить')


class SignupForm(FlaskForm):
    """ Форма регистрации аккаунта """
    name = StringField('Имя', [DataRequired()])
    email = StringField('Почта', [Email(message='Введите правильный адрес почты'), DataRequired()])
    password = PasswordField('Пароль', [DataRequired(message="Пожалуйста, введите пароль")])
    confirmPassword = PasswordField('Подтверждение пароля', [EqualTo(password, message='Пароль должны совпадать')])
    title = SelectField('Роль', [DataRequired()],
                        choices=[('Фермер', 'farmer'),
                                 ('Оборотень', 'werewolf'),
                                 ('Полицейский', 'cop'),
                                 ('Космонавт', 'astronaut'), ])
    website = StringField('Вебсайт', validators=[URL()])
    birthday = DateField('Дата рождения')
    #recaptcha = RecaptchaField()
    submit = SubmitField('Регистрация')


class SigninForm(FlaskForm):
    """ Форма входа в аккаунт """
    name = StringField('Имя или почта', [DataRequired()])
    password = PasswordField('Пароль', [DataRequired(message="Пожалуйста, введите пароль")])
    submit = SubmitField('Вход')


class ContactForm(FlaskForm):
    """ Форма отправки контактов """
    name = StringField('Имя', [DataRequired()])
    email = StringField('Почта', [Email(message='Введите правильный адрес почты'), DataRequired()])
    address = StringField('Адрес', [DataRequired(), Length(min=6, message='Введите полный адрес')])
    body = TextAreaField('Сообщение', [DataRequired(), Length(min=4, message='Ваше сообщение слишком короткое')])
    #recaptcha = RecaptchaField()
    submit = SubmitField('Отправить')
