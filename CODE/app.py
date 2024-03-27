from flask import Flask, flash, request, redirect, url_for, render_template, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from sqlalchemy import or_
from flask_bcrypt import Bcrypt
from api import api_bp 
from models import db, User, GroceryItem, Order, OrderItem, CartItem

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"
app.config['SECRET_KEY'] = 'pleasedonthack'
login_manager = LoginManager(app)
login_manager.login_view = 'user_login'
login_manager.login_message_category = 'info'
bcrypt = Bcrypt(app)

db.init_app(app)




@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user



###############<--!APP DOT ROUTES!-->################


##___________HOME / PRODUCT PAGE__________##
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method =="POST":
        grouped_iteems = {}
        search_keyword = request.form.get("Searchkeyword")
        searchwala = GroceryItem.query.filter(or_(GroceryItem.name == search_keyword.title(), GroceryItem.category == search_keyword.title())).all()
        if searchwala:
            for iteem in searchwala:
                if iteem.category not in grouped_iteems:
                    grouped_iteems[iteem.category] = []
                grouped_iteems[iteem.category].append(iteem)
            return render_template("product_page.html", items=grouped_iteems, user = current_user)
        else:
            flash("Enter valid search words")
            return redirect("/")
        
    all_items = GroceryItem.query.all()
    grouped_items = {}
    for item in all_items:
        if item.category not in grouped_items:
            grouped_items[item.category] = []
        grouped_items[item.category].append(item)
    return render_template("product_page.html", items= grouped_items, user = current_user)


##___________USER/ADMIN LOGIN START__________##
@app.route("/user/login", methods=["GET", "POST"])
def user_login():
    if request.method=="POST":
        email= request.form["input_field1"]
        password= request.form["password_field_1"]
        t = User.query.filter_by(email= email).first()
        if t:
            ###### admin #####
            if t.is_admin:
                if password == t.password or bcrypt.check_password_hash(t.password, password):
                    login_user(t)
                    return redirect("/admin/dashboard")
            ##### user ######
            if bcrypt.check_password_hash(t.password, password) and t.is_admin==False:
                login_user(t)
                return redirect("/")        
        else:
            flash('Email or password incorrect. Retry!')
            return redirect("/user/login")


    return render_template("user_login.html")

@app.route("/user/signup", methods=["GET", "POST"])
def user_signup():
    if request.method =="POST":
        email= request.form["input_field1"]
        name= request.form["input_field_name"]
        phone=request.form["input_field_phone"]
        address=request.form["input_field_address"]
        password= request.form["password_field_1"]
        if len(password)==0:
            flash("Password can't be empty!")
            return redirect("/user/signup")

      
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
       
        if not phone.isdigit():
            flash("Phone number must contain only numeric characters.")
            return redirect("/user/signup")
        
        if User.query.filter_by(email=email).first() or User.query.filter_by(phone=phone).first():
            flash('Email or Phone number already exists! Please choose a different one.')
            return redirect("/user/signup")

        try:
            t = User(email= email,name=name, phone = phone, address=address, password = hashed_password)
            db.session.add(t)
            db.session.commit()
            return redirect("/user/login")
        except:
            flash("Please Enter Valid Details")
            return redirect("/user/signup")

    return render_template("user_signup.html")
##___________USER/ADMIN LOGIN END__________##



##___________ADMIN DASHBOARD SAGA STARTS__________##
@app.route("/admin/dashboard", methods=['GET', 'POST'])
@login_required
def admin_dashboard():

    #AdminValidation
    if not current_user.is_admin:
        flash("Only the Admin can access the Admin Dashboard")
        return redirect("/user/login")
    
    if request.method=="POST":
        name= request.form['name'].title()
        price= request.form['price']
        category=request.form['category'].title()
        quantity= request.form['quantity']

        if GroceryItem.query.filter_by(name=name).first():
            flash(f"{name} already exists, please update it.")
            return redirect("/admin/dashboard")
        
        try:
            t = GroceryItem(name= name, price= price, category = category, quantity= quantity)
            db.session.add(t)
            db.session.commit()
        except:
            flash("Please enter valid detials!")
            return redirect("/admin/dashboard")
    # REtrun the all the items in the GroceryItems to display
    items = GroceryItem.query.all()
    return render_template("admin_dashboard.html", items= items)

@app.route("/admin/dashboard/delete/<int:id>", methods=['GET', 'POST'])
@login_required
def admin_delete(id):
    try:
        d = GroceryItem.query.filter_by(id=id).first()
        db.session.delete(d)
        db.session.commit()
        return redirect("/admin/dashboard")
    except:
        flash("User is making transaction, cannot delete")
        return redirect("/admin/dashboard")

@app.route("/admin/dashboard/update/<int:id>", methods=['GET', 'POST'])
@login_required
def admin_update(id):
    if request.method=="POST":
        u = GroceryItem.query.filter_by(id=id).first()
        u.name = request.form['name'].title()
        u.price= request.form['price']
        u.category=request.form['category'].title()
        u.quantity=request.form['quantity']

        db.session.add(u)
        db.session.commit()
        return redirect("/admin/dashboard")
    item= GroceryItem.query.filter_by(id=id).first()
    return render_template("admin_update.html" ,item=item )
##___________ADMIN DASHBOARD SAGA ENDS__________##


##___________CART SAGA START__________##
@app.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    if request.method == 'POST':
        flash('Cart updated / Order placed!', 'success')
        return redirect(url_for('cart'))
    
    # Fetch cart items for the current user
    cart_items = current_user.cart_items
    total_price = sum(item.item.price * item.quantity for item in cart_items)
    
    prev_order_itemsfirst = Order.query.join(OrderItem).join(GroceryItem).filter(Order.user_id == current_user.id).all()
    prev_list = []
    if prev_order_itemsfirst:
        prev_order_items= prev_order_itemsfirst[-1]
        # Get his last order. 
        for i in prev_order_items.items:
            each_item_id = i.grocery_item_id
            x = GroceryItem.query.filter_by(id= each_item_id).first()
            prev_list.append((x, i))
        return render_template('cart.html',cart_items=cart_items, total_price=total_price, user=current_user, prev_list= prev_list , prev_order_total_price = prev_order_itemsfirst[-1].total_price)
    return render_template('cart.html', cart_items=cart_items, total_price=total_price, user=current_user, prev_list= prev_list)
        


@app.route('/add_to_cart/<int:item_id>', methods=["GET", "POST"])
@login_required
def add_to_cart(item_id):
    prodpageqty = int(request.form["prodpageqty"])
    # Find the grocery item by ID
    grocery_item = GroceryItem.query.get(item_id)

    cart_item = CartItem.query.filter_by(user_id=current_user.id, item_id=item_id).first()

    if prodpageqty <=0 or prodpageqty > int(grocery_item.quantity):
        flash(f"Not enough {grocery_item.name}!")
        return redirect("/")
        
    if cart_item:
        # If the item is already in the cart, increment the quantity
        cart_item.quantity += prodpageqty
        grocery_item.quantity -= prodpageqty
            
    else:
        # If the item is not in the cart, add it with quantity 1
        cart_item = CartItem(user_id=current_user.id, item_id=item_id, quantity= prodpageqty)
        grocery_item.quantity -= prodpageqty
    db.session.add(cart_item)
    db.session.commit()

    flash('Item added to cart!', 'success')
    return redirect(url_for('cart'))


@app.route('/remove_from_cart/<int:item_id>')
@login_required
def remove_from_cart(item_id):
    grocery_item = GroceryItem.query.get(item_id)

    # Find the cart item for the user and item
    cart_item = CartItem.query.filter_by(user_id=current_user.id, item_id=item_id).first()

    if cart_item:
        db.session.delete(cart_item)
        grocery_item.quantity +=cart_item.quantity
        db.session.commit()
        flash('Item removed from cart!', 'success')

    return redirect(url_for('cart'))
##___________CART SAGA END__________##



##___________CHECKOUT__________##
@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    if request.method == 'POST':
        # Process the order here, save it to the database, and clear the user's cart
        order = Order(user_id=current_user.id, total_price=current_user.cart_items_total_price())
        db.session.add(order)
        db.session.commit()

        for cart_item in current_user.cart_items:
            order_item = OrderItem(
                order_id=order.id,
                grocery_item_id=cart_item.item_id,
                quantity=cart_item.quantity,
                price=cart_item.item.price,
                total_price=cart_item.item.price * cart_item.quantity
            )
            db.session.add(order_item)

        l = current_user.cart_items
        for li in l:
            x = CartItem.query.filter_by(id=li.id).first()
            if x:
                db.session.delete(x)
                db.session.commit()

        db.session.commit()
        flash('Order placed successfully!', 'success')
        return redirect("/")

    # Fetch cart items for the current user
    cart_items = current_user.cart_items
    return render_template('checkout.html', cart_items=cart_items, total_price=current_user.cart_items_total_price(), user=current_user)
    



@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        session.clear()
        flash("Logged out", "info")
        return redirect("/user/login")
    flash("Please log in first.")
    return redirect("/user/login")






#_____________Chart Analysis_____________#
import matplotlib.pyplot as plt
@app.route('/analysis')
@login_required
def analysis():
    if current_user.is_admin:
        with app.app_context():
            sales_and_revenue_analysis()
            pie_charts_items()
            pie_charts_category()
        return render_template('analysis.html')
    flash("Only Admin can access the Analysis Dashboard!")
    return redirect("/user/login")



def sales_and_revenue_analysis():
    all_orders = Order.query.order_by(Order.purchase_date).all()
    purchase_dates = [order.purchase_date for order in all_orders]
    revenues = [order.total_price for order in all_orders]
    #daily salesssssss
    daily_sales = [sum(order.total_price for order in all_orders if order.purchase_date.date() == date.date()) for date in purchase_dates]
    # Calculate cumulative revenue
    cumulative_revenue = [sum(revenues[:i+1]) for i in range(len(revenues))]
    # Plot daily sales
    plt.figure(figsize=(6, 9))
    plt.plot(purchase_dates, daily_sales, label='Daily Sales')
    plt.xticks(rotation='vertical')
    plt.xlabel('Date')
    plt.ylabel('Sales')
    plt.title('Daily Sales')
    plt.legend()
    plt.grid(True)
    plt.savefig('static/daily_sales.png')

    # Plot cumulative revenue
    plt.figure(figsize=(6, 9))
    plt.plot(purchase_dates, cumulative_revenue, label='Cumulative Revenue')
    plt.xticks(rotation='vertical')
    plt.xlabel('Date')
    plt.ylabel('Revenue')
    plt.title('Cumulative Revenue')
    plt.legend()
    plt.grid(True)
    plt.savefig('static/cumulative_revenue.png')

# Most popular items analysis function
def pie_charts_items():
    grocery_ke_items = GroceryItem.query.all()
    item_names = [i.name for i in grocery_ke_items]
    item_quantity =[i.quantity for i in grocery_ke_items]

    plt.figure(figsize=(6, 6))
    plt.pie( item_quantity, labels=item_names, autopct='%1.1f%%')
    plt.title('Items by Size')
    plt.savefig('static/pchart_items.png')

def pie_charts_category():
    grocery_ke_items = GroceryItem.query.all()
    item_category = {}

    for i in grocery_ke_items:
        # category lao
        if i in item_category:
        # agar uss category ke aur mile toh add krdo quantity 
            item_category[i.quantity] += i.quantity
        item_category[i.category]=i.quantity

    plt.figure(figsize=(6, 6))
    plt.pie( list(item_category.values()), labels=list(item_category.keys()), autopct='%1.1f%%')
    plt.title('Category by Size')
    plt.savefig('static/pchart_category.png')

#_____________Chart Analysis Ends Finally_____________#












 
 

app.register_blueprint(api_bp, url_prefix='/api')

with app.app_context():
    db.create_all()
if __name__=="__main__":
    app.run(debug=True,  port=5001)