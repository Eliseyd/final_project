from flask import Flask, render_template, request, redirect, jsonify, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/restaurant/JSON')
def restaurantsJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(restaurants=[r.serialize for r in restaurants])

@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id,menu_id):
    Menu_Item = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(Menu_Item=Menu_Item.serialize)

@app.route('/')
@app.route('/restaurant/')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    # return 'This page will show all restaurants'
    return render_template('restaurants.html',restaurants = restaurants)

@app.route('/restaurant/new/',methods=['GET','POST'])
def newRestaurant():
    # return 'This page will be for making a new restaurant'
    if request.method == 'POST':
        newRestaurant = Restaurant(name=request.form['name'])
        session.add(newRestaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newRestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/edit/',methods=['GET','POST'])
def editRestaurant(restaurant_id):
    # return 'This page will be for editing restaurant %s' % restaurant_id
    editRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editRestaurant.name = request.form['name']
        session.add(editRestaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('editRestaurant.html',restaurant = editRestaurant)

@app.route('/restaurant/<int:restaurant_id>/delete/',methods=['GET','POST'])
def deleteRestaurant(restaurant_id):
    # return 'This page will be for deleting restaurant %s' % restaurant_id
    restaurantToDelete = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(restaurantToDelete)
        session.commit()
        return redirect(url_for('showRestaurants'))
    return render_template('deleteRestaurant.html',restaurant = restaurantToDelete)

@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/',methods=['GET','POST'])
def showMenu(restaurant_id):
    # return 'This page is the menu for restaurant %s' % restaurant_id
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return render_template('menu.html',restaurant = restaurant,items = items)

@app.route('/restaurant/<int:restaurant_id>/menu/new/',methods=['GET','POST'])
def newMenuItem(restaurant_id):
    # return 'This page is for making a new menu item for restaurant %s' % restaurant_id
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'],description=request.form['description'],
                            price=request.form['price'],course=request.form['course'],restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('showMenu',restaurant_id=restaurant_id))
    else:
        return render_template('newMenuItem.html',restaurant_id = restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/',methods=['GET','POST'])
def editMenuItem(restaurant_id,menu_id):
    # return 'This page is for editing menu item %s' % menu_id
    editItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editItem.name = request.form['name']
        if request.form['description']:
            editItem.description = request.form['description']
        if request.form['price']:
            editItem.price = request.form['price']
        if request.form['course']:
            editItem.course = request.form['course']
        session.add(editItem)
        session.commit()
        return redirect(url_for('showMenu',restaurant_id=restaurant_id))
    else:
        return render_template('editMenuItem.html',restaurant_id = restaurant_id,menu_id=menu_id,item=editItem)

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/',methods=['GET','POST'])
def deleteMenuItem(restaurant_id,menu_id):
    # return 'This page is for deleting menu item %s' % menu_id
    itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('showMenu',restaurant_id=restaurant_id))
    else:
        return render_template('deleteMenuItem.html',restaurant_id= restaurant_id,menu_id=menu_id,item=itemToDelete)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0',port=5000)




