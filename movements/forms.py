from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length
from datetime import date

"""def notEquals(fieldToCompare, message=None):
    if not message:
        message = u'Los campos no deben ser iguales'

    def _notEquals(form, field):
        if field.data == fieldToCompare.data:
            raise ValidationError(message)

    return _notEquals"""

"""def notEquals(form, field, fieldToCompare):
    if field.data == fieldToCompare.data:
        raise ValidationError("Las monedas no puede coincidir")"""
    


class MovementForm(FlaskForm):
    
    from_currency = SelectField(u'Moneda origen')
    from_quantity = FloatField('Cantidad origen', validators=[DataRequired(message="El valor debe ser un número (p.e.1234.56)")])
    to_currency = SelectField(u'Moneda destino', 
                                choices=[("EUR"),("BTC"), ("ETH"), ("XRP"), ("LTC"), ("BCH"), ("BNB"), ("USDT"), ("EOS"), ("BSV"), ("XLM"), ("ADA"), ("TRX")], 
                                validators=[notEquals(fieldToCompare=from_currency)]
                            )
    to_quantity = FloatField('Cantidad destino', validators=[DataRequired(message="El  debe ser un número (p.e.1234.56)")])    

    submit = SubmitField('Aceptar')
    calc = SubmitField("Calcular")

