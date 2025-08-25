# routes/item_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from model.item import Item

item_bp = Blueprint('item', __name__, url_prefix='/itens')

@item_bp.get('/')
@login_required
def listar_itens():
    rows = Item.mostrar_itens_menu('pizzamais.db') or []
    # rows = [(IdItens, Nome, Preco, Tipo, Descricao), ...]
    itens = [
        {"id": r[0], "nome": r[1], "preco": r[2], "tipo": r[3], "descricao": r[4] or ""}
        for r in rows
    ]
    return render_template('itens/listar.html', itens=itens)

@item_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def criar_item():
    if request.method == 'POST':
        nome = request.form['nome'].strip()
        preco = float(request.form.get('preco', 0) or 0)
        tipo = request.form.get('tipo', '').strip()
        descricao = request.form.get('descricao', '').strip()

        obj = Item(nome, preco, tipo, descricao)
        ok = Item.insert_into_item('pizzamais.db', obj)
        if ok is True:
            flash('Item criado com sucesso!', 'success')
            return redirect(url_for('item.listar_itens'))
        else:
            flash('Erro ao criar item.', 'error')

    return render_template('itens/form.html', titulo='Novo item', item=None)

@item_bp.route('/<int:item_id>/editar', methods=['GET', 'POST'])
@login_required
def editar_item(item_id):
    # precisa de métodos de leitura/atualização no model
    row = Item.search_item_id('pizzamais.db', item_id)
    item = None
    if row and len(row) > 0:
        r = row[0]  # (Nome, Tipo, Descricao, Preco)
        item = {"id": item_id, "nome": r[0], "tipo": r[1], "descricao": r[2], "preco": r[3]}

    if request.method == 'POST':
        # você ainda não tem update no model; adiciono abaixo
        from sqlite3 import connect
        with connect('pizzamais.db') as conn:
            cur = conn.cursor()
            cur.execute("""
                UPDATE Itens SET Nome=?, Preco=?, Tipo=?, Descricao=? WHERE IdItens=?
            """, (request.form['nome'], float(request.form.get('preco', 0) or 0),
                  request.form.get('tipo',''), request.form.get('descricao',''), item_id))
            conn.commit()
        flash('Item atualizado!', 'success')
        return redirect(url_for('item.listar_itens'))

    return render_template('itens/form.html', titulo='Editar item', item=item)

@item_bp.post('/<int:item_id>/excluir')
@login_required
def excluir_item(item_id):
    from sqlite3 import connect
    with connect('pizzamais.db') as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM Itens WHERE IdItens=?", (item_id,))
        conn.commit()
    flash('Item excluído.', 'success')
    return redirect(url_for('item.listar_itens'))
