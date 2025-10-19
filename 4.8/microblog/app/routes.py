from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from app import app
from app.models import alquimias
from app.models.models import User

@app.route('/')
@login_required
def index():
    posts = alquimias.get_timeline()
    return render_template('index.html', title='Página Inicial', user=current_user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].lower()
        password = request.form['password']
        if alquimias.validate_user_password(username, password):
            user = User.query.filter_by(username=username).first()
            login_user(user)
            flash('Login bem-sucedido!')
            return redirect(url_for('index'))
        else:
            flash('Usuário ou senha inválidos!')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso!')
    return redirect(url_for('login'))

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        foto = request.form.get('foto')
        bio = request.form.get('bio')
        if alquimias.user_exists(username):
            flash('Usuário já existe!')
        else:
            alquimias.create_user(username, password, foto=foto, bio=bio)
            flash('Usuário cadastrado com sucesso!')
            return redirect(url_for('login'))
    return render_template('cadastro.html')

@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    if request.method == 'POST':
        body = request.form['body']
        alquimias.create_post(body, current_user)
        flash('Post publicado!')
        return redirect(url_for('index'))
    return render_template('post.html')
