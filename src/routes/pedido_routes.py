# routes/pedido_routes.py
from flask import Blueprint, request, redirect, render_template, url_for, flash
from flask_login import login_required
from model.pedido import Pedido
from controler.pedidoControler import PedidoControler

pedido_bp = Blueprint('pedido', __name__, url_prefix='/pedidos')

@pedido_bp.get('/')
@login_required
def listar_pedidos():
    try:
        rows = PedidoControler.select_all_pedidos('pizzamais.db')
    except Exception:
        # fallback direto no model (se o controller não tiver esse método)
        rows = Pedido.search_in_pedidos_all('pizzamais.db')

    # rows = [(IdPedido, Status, Delivery, Endereco, Data, ValorTotal), ...]
    pedidos = [
        {
            "id": r[0],
            "status": r[1],
            "delivery": bool(r[2]),
            "endereco": r[3] or "",
            "data": r[4] or "",
            "valor_total": r[5] or 0.0,
        }
        for r in rows or []
    ]
    return render_template('pedidos/listar.html', pedidos=pedidos)

@pedido_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def criar():
    if request.method == 'POST':
        status = request.form['status']
        delivery = request.form.get('delivery', 'false').lower() == 'true'
        endereco = request.form.get('endereco', '')
        date = request.form.get('date', '')
        valor_total = float(request.form.get('valor_total', 0) or 0)

        pedido = Pedido(status, delivery, endereco, date, valor_total)
        PedidoControler.insert_into_pedidos('pizzamais.db', pedido)
        flash('Pedido criado com sucesso!', 'success')
        return redirect(url_for('pedido.listar_pedidos'))

    return render_template('pedidos/form.html')
