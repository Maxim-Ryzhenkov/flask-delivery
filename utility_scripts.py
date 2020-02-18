import random
from app import db
from app.models import User, Meal, Category, OrderState, Order


def create_test_users(user_list):
    for name in user_list:
        mail = "@".join(name.split(' ')) + '.ru'
        # phone = '+7 (910) '+str(random.randint(1111111, 9999999))
        new_user = User(username=name, email=mail)
        if name == 'admin':
            new_user.is_admin = True
        new_user.set_password('password')
        db.session.add(new_user)
    db.session.commit()
    print_db_table(User)


def print_db_table(model):
    for item in model.query.all():
        print(item)


def clear_db_table(model):
    """ удалить все зхаписи в таблице с указанной моделью данных"""
    for record in db.session.query(model).all():
        db.session.delete(record)
    db.session.commit()
    print_db_table(model)


def create_categories(categories):
    for item in categories:
        new_category = Category()
        new_category.title = item
        db.session.add(new_category)
    db.session.commit()
    print_db_table(Category)


def create_order_states(order_states):
    for item in order_states:
        new_state = OrderState()
        new_state.title = item
        db.session.add(new_state)
    db.session.commit()
    print_db_table(OrderState)


def create_meals(meals):
    for meal in meals:
        new_meal = Meal()
        new_meal.title = meal['title']
        meal_category = Category.query.filter(Category.title == meal['category']).first()
        new_meal.category_id = meal_category.id
        new_meal.picture = meal['picture']
        new_meal.price = int(random.randint(186, 687))
        db.session.add(new_meal)
    db.session.commit()
    print_db_table(Meal)


if __name__ == '__main__':
    users = ['Аврор ﻿Абрамов', 'Инесса Селезнёва', 'Галена Исакова', 'Дорофея Смирнова', 'Донат Матиевский',
             'admin', 'Руслан Карпов', "Василина Селиверстова", 'Анастасия Орехова', 'Герман Устинов']
    categories = ['суши', 'стритфуд', 'пицца', 'новинки']
    order_states = ['новый', 'выполняется', 'выполнен']
    meals = [{'title': 'Ролл "Тьюринг"', 'category': 'суши', 'picture': 'dish1.jpg'},
             {'title': 'Ролл "Хомский"', 'category': 'суши', 'picture': 'dish7.jpeg'},
             {'title': 'Острый ролл "Ада"', 'category': 'суши', 'picture': 'dish9.jpeg'},
             {'title': 'Гриль 500', 'category': 'стритфуд', 'picture': 'dish16.jpeg'},
             {'title': 'Бургер 404', 'category': 'стритфуд', 'picture': 'dish18.jpeg'},
             {'title': 'Ролл 301', 'category': 'стритфуд', 'picture': 'dish17.jpeg'},
             {'title': 'Пицца "Армин"', 'category': 'пицца', 'picture': 'dish10.jpeg'},
             {'title': 'Пицца "Гвидо"', 'category': 'пицца', 'picture': 'dish15.jpeg'},
             {'title': 'Пицца "Марк и Якоб"', 'category': 'пицца', 'picture': 'dish14.jpeg'},
             {'title': 'Ассорти "Степик"', 'category': 'новинки', 'picture': 'dish19.jpeg'},
             {'title': 'Фласковое рагу', 'category': 'новинки', 'picture': 'dish24.jpeg'},
             {'title': 'Шашлычок "Куратор"', 'category': 'новинки', 'picture': 'dish23.jpeg'}]

    # meal = Meal.query.get(2)
    # meal.picture = 'dish1.jpg'
    # db.session.add(meal)
    # db.session.commit()
    # print_db_table(Meal)

    # create_categories(categories)
    # create_order_states(order_states)
    # create_meals(meals)
    # create_test_users(users)
    #clear_db_table(Meal)
    # print_db_table(Order)
