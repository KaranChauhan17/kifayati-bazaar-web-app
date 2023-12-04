from flask import Flask, render_template, request, redirect, session, jsonify, flash, url_for
from flask_pymongo import PyMongo
from passlib.hash import pbkdf2_sha256


app = Flask(__name__)
app.secret_key = "sashdjkasgdkjahdjklsad"


app.config["MONGO_URI"] = "mongodb://localhost:27017/users"
db = PyMongo(app).db



@app.route('/')
def index():
    return render_template("index.html")


@app.route('/goToRegister')
def goToRegister():
      return render_template('register.html')

@app.route('/goToLogin')
def goToLogin():
      return render_template('login.html')

@app.route('/admin')
def admin():
      return render_template('admin.html')

@app.route('/profile', methods=['POST', 'GET'])
def profile():
        if not session.get('logged_in'):
            return redirect('/login')
        
        products = db.product.find()

        return render_template('profile.html', products=products)

  



@app.route('/register', methods=['GET','POST']) 
def register():
      if request.method == 'POST':
            username = request.form['username']
            password =  request.form['password']
            confirm_password = request.form['confirm_password']
            full_name = request.form['full_name']
            phone_number = request.form['phone_number']
            hostel = request.form['hostel']
            user_type = request.form['user_type']

            user_data = {
                  "_id":username,
                  "password":password,
                  "confirm_password":confirm_password,
                  "full_name":full_name,
                  "phone_number":phone_number,
                  "hostel":hostel,
                  "user_type":user_type
            }

            try:
                  db.user_info.insert_one(user_data)
                  return redirect(url_for('login'))
            except Exception as e:
                  return jsonify({"error" : str(e)})
            
      return render_template('register.html')




@app.route('/login', methods=['GET', 'POST'])
def login():
      if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user_type = request.form['user_type']

            login_user = db.user_info.find_one({'_id': username})

            if login_user is None:
                  return render_template('register.html')
            
            elif username == 'admin':
                  return render_template('admin.html')

            else:
                  session['logged_in'] = True
                  return redirect(url_for('profile'))
            
      return render_template('login.html')


@app.route('/logout')
def logoutUser():
      flash("You have been successfully logged out!", "info")
      session.pop('username', None)
      return redirect(url_for('/'))



@app.route('/pastPurchases', methods=["POST", "GET"])
def ppastPurchases():
      if not session.get('logged_in'):
            return redirect('/login')
        
      orders = db.orders.find()

      return render_template('pastPurchases.html', orders=orders)


@app.route('/presentOrders', methods=["POST", "GET"])
def presentOrders():
      if not session.get('logged_in'):
            return redirect('/login')
        
      orders = db.orders.find()

      return render_template('presentOrders.html', orders=orders)


@app.route('/completed')
def completedOrders():

      return redirect('/pastPurchases')
      



@app.route('/createProduct', methods=['GET', 'POST'])
def createNewProduct():
      if request.method == 'POST':
            product_id = request.form['product_id']
            product_name = request.form['product_name']
            seller_name = request.form['seller_name']
            price = request.form['price']
            description = request.form['description']
            image=request.form['image']

            product_data = {
                  "_id":product_id,
                  "product_name": product_name,
                  "seller_name": seller_name,
                  "price": price,
                  "description":description,
                  "image":image
            }

            try:
                  db.product.insert_one(product_data)
                  return redirect(url_for('createNewProduct'))
            except Exception as e:
                  return jsonify({"error" : str(e)})

      return render_template('createProduct.html')


@app.route('/goToCheckout', methods=['POST', 'GET'])
def goAToCheckout():
      if request.method == 'POST':
            product_id = request.form['product_id']
            username = request.form['username']
            phone_number = request.form['phone_number']
            room_number = request.form['room_number']

            ordered_product = db.product.find_one({"_id": product_id})

            product_name = ordered_product['product_name']
            seller_name = ordered_product['seller_name']
            price = ordered_product['price']

            order_data = {
                  "product_id":product_id,
                  "product_name":product_name,
                  "price":price,
                  "seller_name":seller_name,
                  "username": username,
                  "phone_number":phone_number,
                  "room_number":room_number
            }


            try:
                  db.orders.insert_one(order_data)
                  db.product.delete_one({"_id": product_id})
                  return redirect(url_for('profile'))
            except Exception as e:
                  return jsonify({"error" : str(e)})
            

      return render_template('/checkout.html')



@app.route('/checkout')
def checkout():
      return render_template('/checkout.html')
                  



if __name__ == '__main__':
	app.run(debug=True, port=5001)