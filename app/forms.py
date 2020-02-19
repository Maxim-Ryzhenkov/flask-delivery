from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User


class MailForm(FlaskForm):
    """ Форма отправки сообщения """
    subject = StringField('Тема сообщения',
                          validators=[DataRequired(message="Невежливо игнорировать тему сообщения"),
                                      Length(min=2, max=50,
                                             message="Тема должна быть не короче 2 и не длиннее 50 символов")])
    email = StringField('Почта',
                        validators=[Email(message='Введите правильный адрес почты'),
                                    DataRequired()])
    body = TextAreaField('Сообщение',
                         validators=[DataRequired(),
                                     Length(min=4, message='Ваше сообщение слишком короткое')])
    # recaptcha = RecaptchaField()
    submit = SubmitField('Отправить')


class RegistrationForm(FlaskForm):
    """ Форма регистрации аккаунта """
    username = StringField('Имя пользователя',
                           validators=[DataRequired(message="Имя не может быть пустым или состоять из пробелов"),
                                       Length(min=2, max=25,
                                              message="Имя должно быть не короче 2 и не длиннее 25 символов")])
    email = StringField('Почта',
                        validators=[DataRequired(message="Email не может быть пустым или состоять из пробелов"),
                                    Email(message="Введите корректный email в формате your@email.address")])
    password = PasswordField('Придумайте пароль длиной от 4 до 20 символов',
                             validators=[DataRequired(),
                                         Length(min=4, max=20)])
    password2 = PasswordField('Повторите пароль',
                              validators=[DataRequired(),
                                          EqualTo('password')])
    submit = SubmitField('Зарегистрировать')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Имя уже занято. Пожалуйста, используйте другое.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Адрес уже зарегистрирован на сайте. Пожалуйста, используйте другой.')


class LoginForm(FlaskForm):
    """ Форма входа в аккаунт """
    username = StringField('Имя или почта',
                           validators=[DataRequired(), ])
    password = PasswordField('Пароль',
                             validators=[DataRequired(message='Пожалуйста, введите пароль')])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Вход')


class OrderForm(FlaskForm):
    """ Форма регистрации заказа """
    username = StringField('Имя',
                           validators=[DataRequired(message="Имя не может быть пустым или состоять из пробелов"),
                                       Length(min=2, max=25,
                                              message="Имя должно быть не короче 2 и не длиннее 25 символов")])
    email = StringField('Почта',
                        validators=[DataRequired(message="Email не может быть пустым или состоять из пробелов"),
                                    Email(message="Введите корректный email в формате your@email.address")])
    address = StringField('Адрес',
                          validators=[DataRequired(),
                                      Length(min=6, message='Введите полный адрес')])
    body = TextAreaField('Сообщение')
    # recaptcha = RecaptchaField()
    submit = SubmitField('Отправить')
