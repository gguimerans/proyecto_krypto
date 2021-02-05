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
    from_quantity = FloatField(u'Cantidad origen', validators=[DataRequired(message="El valor debe ser un número (p.e.1234.56)")])
    to_currency = SelectField(u'Moneda destino', 
                                choices=[("EUR"),("BTC"), ("ETH"), ("XRP"), ("LTC"), ("BCH"), ("BNB"), ("USDT"), ("EOS"), ("BSV"), ("XLM"), ("ADA"), ("TRX")],
                                validators=[notEquals(nameFieldToCompare="from_currency", message="Las monedas no pueden coincidir")])
    to_quantity = StringField(u'Cantidad destino')
    precio_unitario = StringField(u'Precio unitario crypto')

    monedaOrigen = StringField(u'Moneda origen')
    monedaDestino = StringField(u'Moneda destino')
    importeOrigen = StringField(u'Importe origen')
    importeDestino = StringField(u'Importe destino')
    precioUnitario = StringField(u'Precio unitario')

    calc = SubmitField(" ")
    submit = SubmitField("Aceptar")


