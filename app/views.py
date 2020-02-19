from flask import render_template, url_for, request, redirect, flash, session
from app import app, db
from app.forms import ContactForm, LoginForm, RegistrationForm
from app.models import Meal, Category, Order, OrderState, User
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


@app.route('/')
def main():
    categories = Category.query.all()
    my_cart = session.get('cart', [])
    cart_info = ""
    if my_cart:
        products = [Meal.query.get(product_id) for product_id in my_cart]
        total_amount = sum(product.price for product in products)
        cart_info = f"(товаров: {len(my_cart)} на {total_amount} рублей)"
    return render_template('main.html', categories=categories, cart_info=cart_info)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    form = LoginForm()

    if form.validate_on_submit():
        user_query = db.session.query(User).filter(
            db.or_(User.username == form.username.data, User.email == form.username.data))
        user = user_query.first()
        if user is None or not user.check_password(form.password.data):
            flash('Неверное имя или пароль.')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main')
        return redirect(next_page)

    return render_template('auth.html', form=form)


@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('main'))


@app.route('/register/', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Поздравляем, вы зарегистрированы!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/cart/', methods=['GET', 'POST'])
def cart():
    form = ContactForm()

    my_cart = session.get('cart', [])
    title = f"Блюд в корзине: {len(my_cart)}" if my_cart else "Ваша корзина пуста"
    products = [Meal.query.get(product_id) for product_id in my_cart]
    total_amount = sum(product.price for product in products)
    total_amount_msg = f"Всего товаров на {total_amount} рублей"

    if not form.validate_on_submit():
        print('Форма не принята!')

    if request.method == 'POST':
        print(form.data)
        new_order = Order()
        new_order.amount = total_amount
        new_order.state = OrderState.query.filter(OrderState.title == 'новый').first()
        new_order.user = User.query.get(1)
        db.session.add(new_order)
        for item in my_cart:
            meal = Meal.query.get(item)
            new_order.meals.append(meal)
        print(new_order)
        db.session.commit()
        session['cart'] = []
        return redirect('/ordered/')
    return render_template('cart.html', form=form, products=products, title=title, total_amount=total_amount_msg)


@app.route('/cart/add/<int:product_id>')
def cart_add(product_id):
    purchases = session.get('cart', [])
    product = Meal.query.get_or_404(product_id)
    print(product_id)
    print(type(product_id))
    print(product)
    purchases.append(product_id)
    session['cart'] = purchases
    flash(f'Товар "{product.title}" добавлен в корзину.')
    return redirect(url_for('cart'))


@app.route('/cart/remove/<int:product_id>')
def cart_remove(product_id):
    purchases = session.get('cart', [])
    if product_id in purchases:
        purchases.remove(product_id)
    session['cart'] = purchases
    product = Meal.query.get_or_404(product_id)
    flash(f'Товар "{product.title}" удалён из корзины.')
    return redirect(url_for('cart'))


@app.route('/ordered/')
def ordered():
    return render_template('ordered.html')


@app.route('/account/<username>/')
@login_required
def account(username):
    user = User.query.filter(User.username == str(username)).first_or_404()
    return render_template('account.html', user=user)
