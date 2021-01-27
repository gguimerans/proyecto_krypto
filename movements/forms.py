from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length
from datetime import date


class MovementForm(FlaskForm):

    from_currency = SelectField(u'Moneda origen', choices=[("EUR"),("BTC"), ("ETH"), ("XRP"), ("LTC"), ("BCH"), ("BNB"), ("USDT"), ("EOS"), ("BSV"), ("XLM"), ("ADA"), ("TRX")])
    from_quantity = FloatField('Cantidad origen', validators=[DataRequired()])
    to_currency = SelectField(u'Moneda destino', choices=[("EUR"),("BTC"), ("ETH"), ("XRP"), ("LTC"), ("BCH"), ("BNB"), ("USDT"), ("EOS"), ("BSV"), ("XLM"), ("ADA"), ("TRX")])
    to_quantity = FloatField('Cantidad destino', validators=[DataRequired()])    

    submit = SubmitField('Aceptar')
