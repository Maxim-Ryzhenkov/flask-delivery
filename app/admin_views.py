from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, Admin, AdminIndexView, expose
from flask_login import current_user, login_required
from app import db, app, mail
from flask_mail import Message
from app.models import User, Order, Meal
from flask import abort, request, flash
from app.forms import MessageForm


class DashboardView(AdminIndexView):
    @expose('/')
    @login_required
    def index(self):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(404)

        return self.render('admin/dashboard.html')


class MailerView(BaseView):
    @expose('/', methods=['GET', 'POST'])
    @login_required
    def mailer(self):
        form = MessageForm()

        if request.method == 'POST':
            # отправка письма
            subject = form.subject.data
            recipient = form.recipient.data
            text_body = form.message.data
            msg = Message(
                subject,
                sender='ryzhenkov.maksim@yandex.ru',
                recipients=[recipient, ]
            )
            msg.body = text_body
            mail.send(msg)
            flash("Сообщение отправлено")
            return self.render('admin/mail_sender/sanded.html')
        return self.render('admin/mail_sender/send.html', form=form)


class UserView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    column_exclude_list = ['password_hash']
    column_searchable_list = ['username', 'email']
    column_filters = ['email']


class MealView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    column_filters = ['title']
    column_labels = dict(title='Название', description='Описание', category='Категория', price='Цена')
    column_list = ['title', 'category', 'price', 'description']
    column_sortable_list = ['title', ('category', 'category.meals'), 'price']


class OrderView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

   # column_searchable_list = ['user']
    column_labels = dict(date='Дата/время', user='Клиент', state='Статус', amount='Сумма', meals='Блюда')
    column_list = ['date', 'user', 'state', 'amount', 'meals']
  #  column_sortable_list = ['date', ('user', 'user.username'), ('state', 'state.title'), 'amount']


admin = Admin(app, template_mode='bootstrap3', name='Админка', index_view=DashboardView(name='Статистика'))
admin.add_view(UserView(User, db.session, name='Пользователи'))
admin.add_view(MealView(Meal, db.session, name='Меню'))
admin.add_view(OrderView(Order, db.session, name='Заказы'))
admin.add_view(MailerView(name='Отправить письмо', endpoint='mail_sender'))
