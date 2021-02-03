from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField, StringField, HiddenField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length
from datetime import date

def notEquals(nameFieldToCompare, message=None):
    if not message:
        message = u'Los campos no deben ser iguales'    
    
    def _notEquals(form, field):
        if field.data == form[nameFieldToCompare].data:
            raise ValidationError(message)

    return _notEquals

class MovementForm(FlaskForm):
    
    from_currency = SelectField(u'Moneda origen')
    from_quantity = FloatField('Cantidad origen', validators=[DataRequired(message="El valor debe ser un número (p.e.1234.56)")])
    to_currency = SelectField(u'Moneda destino', 
                                choices=[("EUR"),("BTC"), ("ETH"), ("XRP"), ("LTC"), ("BCH"), ("BNB"), ("USDT"), ("EOS"), ("BSV"), ("XLM"), ("ADA"), ("TRX")],
                                validators=[notEquals(nameFieldToCompare="from_currency", message="Las monedas no pueden coincidir")])
    to_quantity = StringField('Cantidad destino')
    precio_unitario = StringField('Precio unitario crypto')

    submit = SubmitField("Aceptar")
    calc = SubmitField("Calcular")

