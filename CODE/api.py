from flask import Blueprint, request, jsonify
from models import db, GroceryItem, User

api_bp = Blueprint('api', __name__)



def is_admin():
    try:
        return request.get_json()["key"]=="admin"
    except:
        return False
    

@api_bp.route('/grocery_items', methods=['GET'])
def get_grocery_items():
    items = GroceryItem.query.all()
    if items:
        data = [{"id": item.id, "name": item.name, "price": item.price, "category": item.category, "quantity": item.quantity} for item in items]
        return jsonify(data)
    return jsonify({"message": "Item not found"}), 404


@api_bp.route('/grocery_items/<int:item_id>', methods=['GET'])
def get_grocery_item(item_id):
    item = GroceryItem.query.get(item_id)
    if item:
        data = {"id": item.id, "name": item.name, "price": item.price, "category": item.category, "quantity": item.quantity}
        return jsonify(data)
    return jsonify({"message": "Item not found"}), 404

@api_bp.route('/grocery_items', methods=['POST'])
def create_grocery_item():
    if not is_admin():
        return jsonify({"message": "Only admin can add grocery items"}), 403

    data = request.get_json()


    prev_name_hai = GroceryItem.query.filter_by(name=data["name"].title()).first()
    if prev_name_hai:
        return jsonify({"Error": "Item already present!"}), 403
    
    
    new_item = GroceryItem(name=data['name'].title(), price=data['price'], category=data['category'].title(), quantity=data['quantity'])
    db.session.add(new_item)
    db.session.commit()
    return jsonify({"message": "Item created successfully"}), 201

@api_bp.route('/grocery_items/<int:item_id>', methods=['PUT'])
def update_grocery_item(item_id):
    if not is_admin():
        return jsonify({"message": "Only admin can update grocery items"}), 403

    data = request.get_json()
    item = GroceryItem.query.get(item_id)
    if item:
        item.name = data['name'].title()
        item.price = data['price']
        item.category = data['category'].title()
        item.quantity = data['quantity']
        db.session.commit()
        return jsonify({"message": "Item updated successfully"})
    return jsonify({"message": "Item not found"}), 404

@api_bp.route('/grocery_items/<int:item_id>', methods=['DELETE'])
def delete_grocery_item(item_id):
    if not is_admin():
        return jsonify({"message": "Only admin can delete grocery items"}), 403

    item = GroceryItem.query.filter_by(id = item_id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        return jsonify({"message": "Item deleted successfully"})
    return jsonify({"message": "Item not found"}), 404



#__________User API__________#

@api_bp.route("/user", methods= ["GET"])
def user():
    all_users = User.query.all()
    if all_users:
        return (jsonify([
            {"id" : u.id,
            "name" : u.name,
            "email" : u.email}  for u in all_users]))
    return jsonify({"error": "No user found."}), 404
