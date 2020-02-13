from flask import render_template, url_for, request, redirect, flash
from app import app
from app.forms import ContactForm


@app.route('/')
def main():
    form = ContactForm()
    print(url_for('main'))
    return render_template('main.html', form=form)


@app.route('/login/')
def login():
    return render_template('auth.html')


@app.route('/logout/')
def logout():
    return redirect(url_for('/'))


@app.route('/cart/')
def cart():
    return render_template('cart.html')


@app.route('/ordered/')
def ordered():
    render_template('ordered.html')


@app.route('/account/')
def account():
    render_template('account.html')
