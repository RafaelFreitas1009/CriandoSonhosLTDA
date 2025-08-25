# src/routes/home_routes.py
from flask import Blueprint, render_template
home_bp = Blueprint('home_bp', __name__)

@home_bp.route('/')
def index():
    return render_template('home.html')

