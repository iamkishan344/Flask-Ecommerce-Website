from flask import render_template, request, redirect, url_for, flash, session, current_app
from src import app, db, photos
import secrets
from flask_login import login_required
from .models import Category, Addproduct, Sliders
from .forms import Addproducts
from src.admin.routes import is_admin
from flask_login import login_required, current_user, logout_user, login_user
from src.admin.models import User
import os


def categories():
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    return categories


def sliders():
    slider_images = Sliders.query.all()
    print('slider_images: ', slider_images)
    return slider_images


def remove_slider_images():
    db.session.query(Sliders).delete()
    db.session.commit()


@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    products = Addproduct.query.filter(Addproduct.stock > 0).order_by(Addproduct.id.desc()).paginate(page=page,
                                                                                                     per_page=8)
    return render_template('products/index.html', products=products, categories=categories(), sliders=sliders())


@app.route('/product/search', methods=['GET', 'POST'])
def search():
    page = request.args.get('page', 1, type=int)
    keyword = request.form.get('search')
    if keyword == '':
        return render_template('products/search.html',
                               categories=categories())
    elif keyword is not None:
        search = "%{}%".format(keyword)
        keywords = Addproduct.query.filter(Addproduct.name.like(search)).all()
        return render_template('products/search.html',
                               categories=categories(), keywords=keywords, keyword=keyword)
    else:
        return render_template('products/search.html',
                               categories=categories(), keywords=keyword)


@app.route('/product/id/<int:id>')
def product_detail(id):
    product = Addproduct.query.get_or_404(id)
    product_id = id
    print('product_id:', product_id)
    print('product-name:', product.name)
    category = Category.query.filter_by(id=product.category_id).first_or_404()
    print('category', category)
    products = Addproduct.query.filter_by(category=category).limit(4).all()
    print('products:', products)
    return render_template('products/product_detail.html', product=product,
                           categories=categories(), products=products, product_id=product_id)


@app.route('/category/id/<int:id>')
def get_categories(id):
    page = request.args.get('page', 1, type=int)
    category = Category.query.filter_by(id=id).first_or_404()
    category_pages = Addproduct.query.filter_by(category=category).paginate(page=page, per_page=8)
    return render_template('products/index.html', category_pages=category_pages,
                           categories=categories(), category=category, sliders=sliders())


@app.route('/upload/slide/images', methods=['GET', 'POST'])
@login_required
def upload_slide_images():
    if is_admin() is False:
        return app.errorhandler(404, page_not_found)
    if request.method == "POST":
        remove_slider_images()
        # Sliders
        update_photo1 = request.files.get('slide_image_1')
        update_photo2 = request.files.get('slide_image_2')
        update_photo3 = request.files.get('slide_image_3')
        image_1 = photos.save(update_photo1, name=secrets.token_hex(10) + ".")
        image_2 = photos.save(update_photo2, name=secrets.token_hex(10) + ".")
        image_3 = photos.save(update_photo3, name=secrets.token_hex(10) + ".")
        

        add_slide_images = Sliders(slide_image_1=image_1, slide_image_2=image_2, slide_image_3=image_3)

        flash(f"Home Slide images have been updated", "success")
        db.session.add(add_slide_images)
        db.session.commit()
        return redirect(url_for('upload_slide_images'))

    return render_template('products/upload_slide_images.html')


@app.route('/add/category', methods=['GET', 'POST'])
@login_required
def add_category():
    if is_admin() is False:
        return app.errorhandler(404, page_not_found)

    if request.method == "POST":
        getcat = request.form.get('category')
        cat = Category(name=getcat)
        db.session.add(cat)
        flash(f'The category {getcat} was added successfully.', 'success')
        db.session.commit()
        return redirect(url_for('categories'))
    return render_template('products/add_apparel.html')


@app.route('/delete/category/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_category(id):
    if is_admin() is False:
        return register_error_handler(404, page_not_found)
    category = Category.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(category)
        flash(f'The category {category.name} was deleted successfully.', 'success')
        db.session.commit()
        return redirect(url_for('category'))

    flash(f'The category {category.name} cant be deleted', 'warning')
    return render_template(url_for('products'))


@app.route('/update/category/<int:id>', methods=['GET', 'POST'])
@login_required
def update_category(id):
    if is_admin() is False:
        return register_error_handler(404, page_not_found)
    update_category = Category.query.get_or_404(id)
    category = request.form.get('category_update')
    if request.method == "POST":
        update_category.name = category
        flash(f'The Category {update_category.name} was updated successfully.', 'success')
        db.session.commit()
        return redirect(url_for('category'))
    return render_template('products/update_apparel.html', title='Update category Page',
                           update_category=update_category)


@app.route('/add/product', methods=['POST', 'GET'])
@login_required
def add_product():
    if is_admin() is False:
        return register_error_handler(404, page_not_found)

    # apparels=Apparel.query.all()

    categories = Category.query.all()
    form = Addproducts(request.form)
    if request.method == "POST":
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        model = form.model.data
        colors = form.colors.data
        watt = form.watt.data
        cutout = form.cutout.data
        outer = form.outer.data
        height = form.height.data
        stock = form.stock.data
        desc = form.discription.data

        category = request.form.get('category')
        image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        # image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
        # image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
        # image_2=image_2, image_3=image_3

        addproduct = Addproduct(name=name, price=price, discount=discount, model=model, colors=colors, watt=watt,
                                cutout=cutout, outer=outer, height=height, stock=stock, desc=desc, category_id=category,
                                image_1=image_1)
        db.session.add(addproduct)

        flash(f'The product {name} was added successfully.', 'success')

        db.session.commit()

        return redirect(url_for('products'))

    return render_template('products/add_product.html', title='Add products page', form=form, categories=categories)


@app.route('/update/product/id/<int:id>', methods=['GET', 'POST'])
@login_required
def update_product(id):
    if is_admin() is False:
        return register_error_handler(404, page_not_found)

    # apparels = Apparel.query.all()

    categories = Category.query.all()
    product = Addproduct.query.get_or_404(id)

    category = request.form.get('category')
    form = Addproducts(request.form)

    if request.method == "POST":
        product.name = form.name.data
        product.price = form.price.data
        product.model = form.model.data
        product.discount = form.discount.data
        product.colors = form.colors.data
        product.watt = form.watt.data
        product.cutout = form.cutout.data
        product.outer = form.outer.data
        product.height = form.height.data
        product.desc = form.discription.data
        product.category_id = category
        product.stock = form.stock.data

        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
                print(product.image_1)
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
            except:
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        # if request.files.get('image_2'):
        #     try:
        #         os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
        #         product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
        #     except:
        #         product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
        # if request.files.get('image_3'):
        #     try:
        #         os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
        #         product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
        #     except:
        #         product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")

        flash('The product was updated', 'success')
        db.session.commit()
        return redirect(url_for('products'))

    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.discription.data = product.desc
    form.model.data = product.model
    form.colors.data = product.colors
    form.watt.data = product.watt
    form.cutout.data = product.cutout
    form.outer.data = product.outer
    form.height.data = product.height
    category = product.category_id
    return render_template('products/update_product.html', form=form, title="Update Product", categories=categories,
                           product=product)


@app.route('/delete/product/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_product(id):
    if is_admin() is False:
        return app.errorhandler(404, page_not_found)

    product = Addproduct.query.get_or_404(id)

    if request.method == "POST":
        try:
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
            # os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
            # os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
        except Exception as e:
            print(e)

        db.session.delete(product)
        flash(f'The product {product.name} was deleted successfully.', 'success')
        db.session.commit()
        return redirect(url_for('products'))

    flash(f'The product {product.name} cant be deleted', 'warning')
    return render_template(url_for('products'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', user=current_user, categories=categories()), 404