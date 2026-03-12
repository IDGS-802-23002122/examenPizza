from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from models import db, Cliente, Pedido, DetallePedido
from forms import PizzeriaForm
from datetime import datetime
from config import Config

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/pizzeria'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret_key_pizzeria'

app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    form = PizzeriaForm()
    
    if 'pizzas_agregadas' not in session:
        session['pizzas_agregadas'] = []

    if form.validate_on_submit():
        session['cliente_nombre'] = form.nombre.data
        session['cliente_direccion'] = form.direccion.data
        session['cliente_telefono'] = form.telefono.data
        precios_tamano = {'40': 'Chica', '80': 'Mediana', '120': 'Grande'}
        nombres_ing = {'10': 'Jamón', '10': 'Piña', '10': 'Champiñones'} 
        
        p_base = float(form.tamano.data)
        p_ing = len(form.ingredientes.data) * 10
        subtotal = (p_base + p_ing) * form.num_pizzas.data
        
        nueva_pizza = {
            'tamano_nombre': precios_tamano[form.tamano.data],
            'ingredientes_nombres': ", ".join([nombres_ing[i] for i in form.ingredientes.data]),
            'cantidad': form.num_pizzas.data,
            'subtotal': subtotal
        }
        
        temp_list = session['pizzas_agregadas']
        temp_list.append(nueva_pizza)
        session['pizzas_agregadas'] = temp_list
        
        flash("Pizza añadida a la lista.", "info")
        return redirect(url_for('index'))

    return render_template('index.html', form=form, pizzas_agregadas=session['pizzas_agregadas'])



@app.route('/terminar', methods=['POST'])
def terminar():
    pizzas = session.get('pizzas_agregadas', [])
    if not pizzas:
        flash("No hay pizzas en el pedido", "warning")
        return redirect(url_for('index'))

    try:
        nuevo_cliente = Cliente(
            nombre=session.get('cliente_nombre'),
            direccion=session.get('cliente_direccion'),
            telefono=session.get('cliente_telefono')
        )
        db.session.add(nuevo_cliente)
        db.session.flush()

        total_venta = sum(p['subtotal'] for p in pizzas)
        nuevo_pedido = Pedido(
            id_cliente=nuevo_cliente.id_cliente,
            fecha=datetime.now().date(),
            total=total_venta
        )
        db.session.add(nuevo_pedido)
        db.session.flush()

        for p in pizzas:
            detalle = DetallePedido(
                id_pedido=nuevo_pedido.id_pedido,
                tamano=p['tamano_nombre'],
                ingredientes=p['ingredientes_nombres'],
                cantidad=p['cantidad'],
                subtotal=p['subtotal']
            )
            db.session.add(detalle)

        db.session.commit()
        session.clear() 
        flash(f"Venta guardada con éxito por ${total_venta}", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error en BD: {str(e)}", "danger")
        print(e)

    return redirect(url_for('index'))

@app.route('/quitar/<int:index>', methods=['POST'])
def quitar_pizza(index):
    if 'pizzas_agregadas' in session:
        temp_list = session['pizzas_agregadas']
        if 0 <= index < len(temp_list):
            eliminada = temp_list.pop(index)
            session['pizzas_agregadas'] = temp_list
            flash(f"Se quitó la pizza de {eliminada['tamano_nombre']} de la lista.", "info")
    
    return redirect(url_for('index'))

@app.route('/reportes', methods=['GET', 'POST'])
def reportes():
    ventas = []
    # Diccionarios de traducción para que el usuario pueda escribir en español
    dias_es_en = {
        'lunes': 'Monday', 'martes': 'Tuesday', 'miercoles': 'Wednesday',
        'jueves': 'Thursday', 'viernes': 'Friday', 'sabado': 'Saturday', 'domingo': 'Sunday'
    }
    meses_es_en = {
        'enero': 'January', 'febrero': 'February', 'marzo': 'March', 'abril': 'April',
        'mayo': 'May', 'junio': 'June', 'julio': 'July', 'agosto': 'August',
        'septiembre': 'September', 'octubre': 'October', 'noviembre': 'November', 'diciembre': 'December'
    }

    if request.method == 'POST':
        busqueda_dia = request.form.get('dia', '').lower().strip()
        busqueda_mes = request.form.get('mes', '').lower().strip()

        if busqueda_dia in dias_es_en:
            dia_ingles = dias_es_en[busqueda_dia]
            ventas = Pedido.query.filter(db.func.dayname(Pedido.fecha) == dia_ingles).all()
        
        elif busqueda_mes in meses_es_en:
            mes_ingles = meses_es_en[busqueda_mes]
            ventas = Pedido.query.filter(db.func.monthname(Pedido.fecha) == mes_ingles).all()

    return render_template('reportes.html', ventas=ventas)

@app.route('/detalle_pedido/<int:id>')
def detalle_pedido(id):
    pedido = Pedido.query.get_or_404(id)
    detalles = DetallePedido.query.filter_by(id_pedido=id).all()
    
    return render_template('detalle.html', pedido=pedido, detalles=detalles)

if __name__ == '__main__':
    app.run(debug=True)