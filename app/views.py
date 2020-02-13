from flask import render_template, url_for, request, redirect, flash
from app import app


@app.route('/')
def main():
    render_template(url_for('main'))


@app.route('/login/')
def login():
    render_template(url_for('auth'))


@app.route('/logout/')
def logout():
    render_template(url_for('main'))


@app.route('/cart/')
def cart():
    render_template(url_for('cart'))


@app.route('/ordered/')
def ordered():
    render_template(url_for('ordered'))


@app.route('/account/')
def account():
    render_template(url_for('account'))
