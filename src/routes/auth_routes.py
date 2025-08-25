# routes/auth_routes.py
from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import login_user, logout_user
from model.user import User

auth = Blueprint('auth', __name__)

# usuário de teste (ou busque do banco)
users = {'admin': User(1, 'admin', '1234')}

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)

        if user and user.password == password:
            login_user(user)
            next_url = request.args.get('next')
            return redirect(next_url or url_for('home_bp.index'))
        else:
            flash('Credenciais inválidas.', 'error')

    return render_template('login.html')

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
