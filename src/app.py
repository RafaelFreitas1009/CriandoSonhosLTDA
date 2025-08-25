from flask import Flask, redirect, url_for
from flask_login import LoginManager
from routes.auth_routes import auth
from routes.pedido_routes import pedido_bp
from routes.home_routes import home_bp

# opcional: quando você criar as rotas de itens, isso passa a registrar automaticamente
try:
    from routes.item_routes import item_bp
except Exception:
    item_bp = None

from model.user import User
from model.database import Database
from controler.databaseControler import DatabaseControler

# cria app Flask
app = Flask(__name__)
app.secret_key = 'pizza-secreta'

# login manager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

# usuários fixos (teste)
users = {'admin': User(1, 'admin', '1234')}

@login_manager.user_loader
def load_user(user_id):
    for user in users.values():
        if str(user.id) == str(user_id):
            return user
    return None

# registra rotas (blueprints)
app.register_blueprint(home_bp)
app.register_blueprint(pedido_bp)
app.register_blueprint(auth)
if item_bp:
    app.register_blueprint(item_bp)

# helper para os templates
@app.context_processor
def inject_has_endpoint():
    def has_endpoint(endpoint_name: str) -> bool:
        try:
            url_for(endpoint_name)
            return True
        except Exception:
            return False
    return dict(has_endpoint=has_endpoint)

# rota inicial
@app.route('/')
def index():
    return redirect(url_for('home_bp.index'))

# inicializa banco
def inicializar_banco():
    database = Database('pizzamais.db')
    cursor = DatabaseControler.conect_database(database.name)
    DatabaseControler.create_table_itens(cursor)
    DatabaseControler.create_table_pedidos(cursor)
    DatabaseControler.create_table_itens_pedidos(cursor)

if __name__ == '__main__':
    inicializar_banco()
    app.run(debug=True)
