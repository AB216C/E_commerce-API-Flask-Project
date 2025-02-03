
#pip install Flask Flask-SQLAlchemy Flask-Marshmallow mysql-connector-python marshmallow-sqlalchemy

from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import ValidationError
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey,Table, String, Column,DateTime, func, select, Date
from typing import List
from datetime import date

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Mahirane231995@localhost/E_COMMERCE'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)
ma = Marshmallow(app)


class User(Base):
  __tablename__ = "users"
  user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  name: Mapped[str] = mapped_column(String(100))
  address: Mapped[str] = mapped_column(String(100))
  email: Mapped[str] = mapped_column(String(100), unique= True)

  orders:Mapped[List["Order"]] = relationship(back_populates="buyer")

order_product = Table(
  "order_product",
  Base.metadata,
  Column("product_id", ForeignKey("products.product_id")),
  Column("order_id", ForeignKey("orders.order_id"))
)

class Order(Base):
  __tablename__ = "orders"
  order_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  order_date:Mapped[date] = mapped_column(Date, nullable=False)
  user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'))
  
  buyer: Mapped["User"] = relationship(back_populates="orders")

  products: Mapped[List["Product"]] =relationship( secondary="order_product", back_populates="purchase_orders")


class Product(Base):
  __tablename__ = "products"
  product_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  product_name: Mapped[str] = mapped_column(String(100))
  price: Mapped[float] = mapped_column(nullable=False)

  purchase_orders: Mapped[List["Order"]] = relationship(secondary="order_product", back_populates = "products")


class UserSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = User

class OrderSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = Order
class ProductSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = Product


user_schema = UserSchema()
users_schema = UserSchema(many=True)
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

#==============USER END POINT =====================================
@app.route("/user", methods=['POST'])

#This function can be used to add multiple users to the API
def create_user():
  try:
    new_user = user_schema.load(request.json)
  except ValidationError as e:
    return jsonify(e.messages),400

  user = User(name=new_user['name'], address=new_user['address'], email=new_user['email'])
  db.session.add(user)
  db.session.commit()

  return user_schema.dumps(new_user),201

#The route/function below has ability to retrieve all users added to the API in JSON format.
@app.route("/users", methods = ['GET'])

def get_users():
  query = select(User)
  users = db.session.execute(query).scalars().all()
  return users_schema.dump(users),200

#This route and function has ability to retrive a specific user information using id.
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = db.session.get(User, id)
    return user_schema.jsonify(user), 200

#This route and function has ability to update name, address, or email of a specific user based on the assigned id
@app.route('/users/<int:id>', methods=['PUT'])

def update_user(id):
  user = db.session.get(User,id)

  if not user:
    return jsonify({"message":"Invalid user id"}),400
  
  try:
    user_data = user_schema.load(request.json)
  except ValidationError as e:
    return jsonify(e.messages),400
  
  user.name =user_data['name']
  user.address = user_data['address']
  user.email = user_data['email']
  
  db.session.commit()
  return user_schema.jsonify(user),200

@app.route('/users/<int:id>', methods=['DELETE'])

def delete_user(id):
    user = db.session.get(User,id)

    if not user:
      return jsonify({"message":"Invalid user id"}),400
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({"Messagge":f"Deleted user: {id}"}),200

#=============== PRODUCT END POINTS =========================
#This function can be used to add multiple products to the API

@app.route("/product", methods=['POST'])
def create_product():
  try:
    new_product = product_schema.load(request.json)
  except ValidationError as e:
    return jsonify(e.messages),400

  product = Product(product_name=new_product['product_name'], price=new_product['price'])
  db.session.add(product)
  db.session.commit()

  return product_schema.dumps(new_product),201


#The route/function below has ability to retrieve all products added to the API in JSON format.
@app.route("/products", methods = ['GET'])

def get_products():
  query = select(Product)
  products = db.session.execute(query).scalars().all()
  return products_schema.dump(products),200


#This route and function has ability to retrieve a product using specific id.
@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = db.session.get(Product, id)
    return product_schema.jsonify(product), 200


#This route and function has ability to update product's name and price using id
@app.route('/product/<int:id>', methods=['PUT'])

def update_product(id):
  product= db.session.get(Product,id)

  if not product:
    return jsonify({"message":"Invalid product id"}),400
  
  try:
    product_data = product_schema.load(request.json)
  except ValidationError as e:
    return jsonify(e.messages),400
  
  product.product_name =product_data['product_name']
  product.price = product_data['price']

  db.session.commit()
  return product_schema.jsonify(product),200

#Deleting products based on product id
@app.route('/products/<int:id>', methods=['DELETE'])

def delete_product(id):
    product = db.session.get(Product,id)

    if not product:
      return jsonify({"message":"Invalid product id"}),400
    
    db.session.delete(product)
    db.session.commit()
    return jsonify({"Messagge":f"Deleted product: {id}"}),200



# #=======ORDER END POINTS=====================
# POST /orders: Create a new order (requires user ID and order date)

# @app.route("/order", methods=['POST'])

# def create_order():
#   try:
#     new_order = order_schema.load(request.json)
#   except ValidationError as e:
#     return jsonify(e.messages),400

#   order = Order(order_date=new_order['order_date'])
#   db.session.add(order)
#   db.session.commit()

#   return user_schema.dumps(new_order),201



# # GET /orders/<order_id>/add_product/<product_id>: Add a product to an order (prevent duplicates)

# @app.route("/orders", methods = ['GET'])

# def add_product():
#   query = select(Order)
#   orders = db.session.execute(query).scalars().all()
#   return orders_schema.dump(orders),200



# #GET /orders/user/<user_id>: Get all orders for a user

# @app.route('/orders/<int:id>', methods=['GET'])
# def get_orders(id):
#     order = db.session.get(Order, id)
#     return order_schema.jsonify(order), 200



# #GET /orders/<order_id>/products: Get all products for an order

# @app.route('/orders/<int:id>', methods=['GET'])
# def get_products(id):
#     order = db.session.get(Order, id)
#     return order_schema.jsonify(order), 200




# #DELETE /orders/<order_id>/remove_product: Remove a product from an order
# @app.route('/orders/<int:id>', methods=['DELETE'])

def delete_product(id):
    order= db.session.get(Product,id)

    if not order:
      return jsonify({"message":"Invalid product id"}),400
    
    db.session.delete(order)
    db.session.commit()
    return jsonify({"Messagge":f"Deleted product: {id}"}),200

if __name__ == "__main__":
  with app.app_context():
    db.create_all()
  app.run(debug=True)



