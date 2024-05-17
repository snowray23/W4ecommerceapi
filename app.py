from flask import Flask, jsonify, request 
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
from connect_db import connect_db, Error

app = Flask(__name__) 
app.config['JSON_SORT_KEYS'] = False
ma = Marshmallow(app)


class CustomerSchema(ma.Schema):
    name = fields.String(required=True)
    email = fields.String(required=True)
    phone = fields.String(required=True)

    class Meta:      
        
        fields = ("name", "email", "phone")
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)


@app.route("/") 
def home():
    return "Welcome to our super cool ecommerce api! yippee"

@app.route('/customers', methods=['GET'])
def get_customers(): 
    print("hello from the get")  
    try:
        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = conn.cursor(dictionary=True)
       
        query = "SELECT * FROM Customer"

    
        cursor.execute(query)

     
        customers = cursor.fetchall()

        
        return customers_schema.jsonify(customers)
    
    except Error as e:
       
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
    finally:
     
        if conn and conn.is_connected():
            cursor.close()
            conn.close() 



@app.route('/customers', methods = ['POST']) 
def add_customer():
    try:
       
        customer_data = customer_schema.load(request.json)

    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    try:
        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()

       
        new_customer = (customer_data['name'], customer_data['email'], customer_data['phone'])

    
        query = "INSERT INTO Customer (name, email, phone) VALUES (%s, %s, %s)"

      
        cursor.execute(query, new_customer)
        conn.commit()

        return jsonify({"message":"New customer added succesfully"}), 201
    
    except Error as e:
        print(f"error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close() 

@app.route('/customers/<int:id>', methods= ["PUT"])
def update_customer(id):
    print("hello")
    try:
        customer_data = customer_schema.load(request.json)
        print(customer_data)

    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    try:
        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()

        
        updated_customer = (customer_data['name'], customer_data['email'], customer_data['phone'], id)

       
        query = "UPDATE Customer SET name = %s, email = %s, phone = %s WHERE customer_id = %s"

     
        cursor.execute(query, updated_customer)
        conn.commit()

       
        return jsonify({"message":"Customer details were succesfully updated!"}), 200
    
    except Error as e:
        print(f"error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
    finally:
        
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/customers/<int:id>', methods=["DELETE"])
def delete_customer(id):
    try:
        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()
       
        customer_to_remove = (id,)
        

        
        query = "SELECT * FROM Customer WHERE customer_id = %s"
     
        cursor.execute(query, customer_to_remove)
        customer = cursor.fetchone()
        if not customer:
            return jsonify({"error": "User does not exist"}), 404
        
      
        del_query = "DELETE FROM Customer where customer_id = %s"
        cursor.execute(del_query, customer_to_remove)
        conn.commit()

       
        return jsonify({"message":"Customer Removed succesfully"}), 200   



    except Error as e:
        print(f"error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close() 

class OrderSchema(ma.Schema):
    order_id = fields.Int(dump_only=True)
    customer_id = fields.Int(required=True)
    date = fields.Date(required=True)
    class Meta:  
        
        fields = ("order_id", "customer_id", "date")

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

    

@app.route("/orders", methods = ["GET"])
def get_orders():
    try:
        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM orders"
        cursor.execute(query)
        orders = cursor.fetchall()  

        return orders_schema.jsonify(orders)
    
    
    except Error as e:
        print(f"error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
    finally:
        
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            


@app.route('/orders', methods=["POST"])
def add_order():
    try:
        order_data = order_schema.load(request.json)

    except ValidationError as e:
        return jsonify(e.messages), 400

    try:
        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()
        
        query = "INSERT INTO orders (date, customer_id) VALUES (%s,%s)"
        cursor.execute(query, (order_data['date'], order_data['customer_id']))
        conn.commit()
        return jsonify({"message": "Order was succesfully added"}),201


    

    except Error as e:
        print(f"error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close() 


@app.route('/orders/<int:order_id>', methods= ["PUT"])
def update_order(order_id):
    try:

        order_data = order_schema.load(request.json)

    except ValidationError as e:
        return jsonify(e.messages), 400
    
    try:
        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()
        query = "UPDATE ORDERS SET date = %s, customer_id = %s WHERE order_id = %s"
        cursor.execute(query, (order_data['date'], order_data['customer_id'], order_id))
        conn.commit()
        return jsonify({"message": "order updated successfully"}), 200
    
    except Error as e:
        print(f"error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

    finally:
   
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
    

@app.route("/orders/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
    try:
        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()

       
        query = "SELECT * FROM Orders WHERE order_id = %s"
      
        cursor.execute(query, (order_id,))
        order = cursor.fetchone()
        if not order:
            return jsonify({"error": "Order does not exist"}), 404
        
        
        del_query = "DELETE FROM Orders where order_id = %s"
        cursor.execute(del_query, (order_id,))
        conn.commit()
        return jsonify({"message": f"Succesfully delete order_id {order_id}"})     

    except Error as e:
        print(f"error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

    finally:
   
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


    


       

    








if __name__ == "__main__":
    app.run(debug=True)
