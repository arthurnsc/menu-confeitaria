from flask import Flask, request, render_template, redirect
import sqlite3
app = Flask(__name__)

def criartabela():
    conexao = sqlite3.connect('pedidos.db')
    cursor = conexao.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente TEXT,
        tamanho TEXT,
        massa TEXT,
        recheio TEXT,
        valor REAL,
        status TEXT DEFAULT 'recebido'
    )
    """)
    conexao.commit()
    conexao.close()

criartabela()

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/admin')
def admpage():
    conexao = sqlite3.connect('pedidos.db')
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM pedidos WHERE status = 'recebido'")
    pedidosproducao = cursor.fetchall()
    cursor.execute("SELECT * FROM pedidos WHERE status = 'concluido'")
    pedidosconcluidos = cursor.fetchall()
    conexao.close()
    return render_template('admin.html', pedidosproducao=pedidosproducao, pedidosconcluidos=pedidosconcluidos, num_pedidosproducao=len(pedidosproducao), num_pedidosconcluidos=len(pedidosconcluidos))

@app.route('/concluirpedido/<int:pedido_id>', methods=['POST'])
def concluirpedido(pedido_id):
    conexao = sqlite3.connect('pedidos.db')
    cursor = conexao.cursor()
    cursor.execute("UPDATE pedidos SET status = 'concluido' WHERE id = ?", (pedido_id,))
    conexao.commit()
    conexao.close()
    return redirect('/admin')

@app.route('/editarpedido/<int:pedido_id>', methods=['POST'])
def editarpedido(pedido_id):
    conexao = sqlite3.connect('pedidos.db')
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM pedidos WHERE id = ?", (pedido_id,))
    pedido = cursor.fetchone()
    conexao.close()
    return render_template('editar.html', pedido=pedido)

@app.route('/confirmaralteracoes/<int:pedido_id>', methods=['POST'])
def confirmaralteracoes(pedido_id):
    nome = request.form['nome']
    tamanho = request.form['tamanho']
    massa = request.form['massa']
    recheio = request.form['recheio']   
    if tamanho == 'Pequeno':
        valor = 50
    elif tamanho == 'Medio':
        valor = 70
    else:
        valor = 90
    conexao = sqlite3.connect('pedidos.db')
    cursor = conexao.cursor()
    cursor.execute("""
    UPDATE pedidos
    SET cliente = ?, tamanho = ?, massa = ?, recheio = ?, valor = ?
    WHERE id = ?
    """, (nome, tamanho, massa, recheio, valor, pedido_id))
    conexao.commit()
    conexao.close()
    return redirect('/admin')

@app.route('/deletarpedido/<int:pedido_id>', methods=['POST'])
def deletarpedido(pedido_id):
    conexao = sqlite3.connect('pedidos.db')
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM pedidos WHERE id = ?", (pedido_id,))
    conexao.commit()
    conexao.close()
    return redirect('/admin')

@app.route('/pedido', methods=['POST'])
def pedido():
    nome = request.form['nome']
    tamanho = request.form['tamanho']
    massa = request.form['massa']
    recheio = request.form['recheio']   
    if tamanho == 'Pequeno':
        valor = 50
    elif tamanho == 'Medio':
        valor = 70
    else:
        valor = 90
    return render_template('revisar.html', nome=nome, tamanho=tamanho, massa=massa, recheio=recheio, valor=valor)

@app.route('/confirmar', methods=['POST'])
def confirmar():
    nome = request.form['nome']
    tamanho = request.form['tamanho']
    massa = request.form['massa']
    recheio = request.form['recheio']
    valor = request.form['valor']
    conexao = sqlite3.connect('pedidos.db')
    cursor = conexao.cursor()
    cursor.execute("""
    INSERT INTO pedidos (cliente, tamanho, massa, recheio, valor, status)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (nome, tamanho, massa, recheio, valor, 'recebido'))
    conexao.commit()
    conexao.close()
    return render_template('confirmar.html', nome=nome, tamanho=tamanho, massa=massa, recheio=recheio, valor=valor)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
