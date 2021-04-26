from wtforms import Form, SubmitField,IntegerField,FloatField,StringField,TextAreaField,validators,DecimalField
from flask_wtf.file import FileField,FileRequired,FileAllowed

class Addproducts(Form):
    name = StringField('Name', [validators.DataRequired()])
    price = DecimalField('Price', [validators.DataRequired()])
    discount = IntegerField('Discount', default=0)
    model = StringField('model', [validators.DataRequired()])
    watt = StringField('watt', [validators.DataRequired()])
    cutout = StringField('cutout', [validators.DataRequired()])
    outer = StringField('outer', [validators.DataRequired()])
    height = StringField('height', [validators.DataRequired()])
    stock = IntegerField('Stock', [validators.DataRequired()])
    colors = StringField('Color', [validators.DataRequired()])
    discription = TextAreaField('Discription', [validators.DataRequired()])
    image_1 = FileField('Image 1',
                        validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif', 'jpeg'], 'Images only please')])
    image_2 = FileField('Image 2',
                        validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif', 'jpeg'], 'Images only please')])
    image_3 = FileField('Image 3',
                        validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif', 'jpeg'], 'Images only please')])

