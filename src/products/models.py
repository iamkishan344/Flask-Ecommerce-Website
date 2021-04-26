from src import db


from datetime import datetime


class Addproduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    discount = db.Column(db.Integer, default=0)
    colors = db.Column(db.Text(20), nullable=False,default='none')
    desc = db.Column(db.Text(200), nullable=False)
    model = db.Column(db.String(80), nullable=False)
    watt = db.Column(db.Integer, nullable=False, default=0)
    cutout = db.Column(db.String(80), nullable=False, default="XX*XX")
    outer = db.Column(db.String(80), nullable=False, default="00*00")
    height = db.Column(db.String(80), nullable=False, default=1)
    stock = db.Column(db.Integer, nullable=False, default="Yes")
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('categories', lazy=True))
    image_1 = db.Column(db.String(150), nullable=False,default='image.jpg')
    image_2 = db.Column(db.String(150), nullable=False,default='image.jpg')
    image_3 = db.Column(db.String(150), nullable=False,default='image.jpg')

    def __repr__(self):
        return '<Addproduct %r>' % self.name



class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)


class Sliders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slide_image_1 = db.Column(db.String(150), nullable=False, default='image1.jpg')
    slide_image_2 = db.Column(db.String(150), nullable=False, default='image2.jpg')
    slide_image_3 = db.Column(db.String(150), nullable=False, default='image3.jpg')


db.create_all()
# db.drop_all()