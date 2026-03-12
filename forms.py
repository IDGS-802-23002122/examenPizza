from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, RadioField, SelectMultipleField, widgets
from wtforms.validators import DataRequired

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class PizzeriaForm(FlaskForm):
    
    nombre = StringField('Nombre', validators=[DataRequired()])
    direccion = StringField('Dirección', validators=[DataRequired()])
    telefono = StringField('Teléfono', validators=[DataRequired()])
    
    tamano = RadioField('Tamaño Pizza', choices=[
        ('40', 'Chica $40'),
        ('80', 'Mediana $80'),
        ('120', 'Grande $120')
    ], validators=[DataRequired()])
    
    ingredientes = MultiCheckboxField('Ingredientes', choices=[
        ('10', 'Jamón $10'),
        ('10', 'Piña $10'),
        ('10', 'Champiñones $10')
    ])
    
    num_pizzas = IntegerField('Num. de Pizzas', validators=[DataRequired()])