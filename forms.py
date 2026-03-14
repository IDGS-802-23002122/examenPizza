from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, RadioField, SelectMultipleField, widgets, DateField
from wtforms.validators import DataRequired, NumberRange, Length, Regexp 

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class PizzeriaForm(FlaskForm):
    
    nombre = StringField('Nombre', validators=[DataRequired()])
    direccion = StringField('Dirección', validators=[DataRequired()])
    telefono = StringField('Teléfono', validators=[
        DataRequired(),
        Regexp(r'^[0-9]+$', message="El teléfono solo debe contener números"),
        Length(min=10, max=10, message="El teléfono debe tener exactamente 10 dígitos")
    ])
    fecha = DateField('Fecha', format='%Y-%m-%d', validators=[DataRequired()])
    
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
    
    num_pizzas = IntegerField('Num. de Pizzas', validators=[
        DataRequired(message="Ingresa una cantidad"),
        NumberRange(min=1, message="La cantidad mínima es 1 pizza")
    ])