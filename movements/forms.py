from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length
from datetime import date


class MovementForm(FlaskForm):

    from_currency = SelectField(u'Moneda origen')
    from_quantity = FloatField('Cantidad origen', validators=[DataRequired(message="El valor debe ser un número (p.e.1234.56)")])
    to_currency = SelectField(u'Moneda destino', choices=[("EUR"),("BTC"), ("ETH"), ("XRP"), ("LTC"), ("BCH"), ("BNB"), ("USDT"), ("EOS"), ("BSV"), ("XLM"), ("ADA"), ("TRX")])
    to_quantity = FloatField('Cantidad destino', validators=[DataRequired(message="El  debe ser un número (p.e.1234.56)")])    

    submit = SubmitField('Aceptar')
    calc = SubmitField("Calcular")

