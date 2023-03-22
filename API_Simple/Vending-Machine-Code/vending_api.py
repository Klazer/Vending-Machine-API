from flask import Flask, Response, json
from flask_restful import Api, Resource, abort, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event

app = Flask(__name__)  # Creates our app within flask
# Will wrap our app in an API and initializes the fact we're using a restful API
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' #We want to config the database uri to be whatever the name of the database is and creates the database based on the current path it is in
db = SQLAlchemy(app) #Initialize our database with our api

class inventoryModel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    itemName = db.Column(db.String(50), nullable = False, unique = True) #nullable indicates that this field must always contain something
    quantity = db.Column(db.Integer, nullable = False)
    
    def __repr__(self):
        return f"Item(name={itemName}, quantity={quantity})"

@event.listens_for(inventoryModel.__table__, 'after_create') #Monitors the creation of the inventoryModel database. When it gets created, it initialized default values into the database
def create_items(*args, **kwargs):
    db.session.add(inventoryModel(id = 1, itemName='Coca Cola', quantity=5))
    db.session.add(inventoryModel(id = 2, itemName='Mountain Dew', quantity=5))
    db.session.add(inventoryModel(id = 3, itemName='Potato Chips', quantity=5))
    db.session.commit()
    print("success")

with app.app_context():
    db.create_all() #Creates database. Only have to do this once unless we want to reinitialize the database

# inventory = [5, 5, 5]
coinCount = 0

add_coins = reqparse.RequestParser() #Allows us to parse items that are inputted into body of api
add_coins.add_argument(
    "coin", type=int, help="Must include a coin to be added. Please try again", required = True) #Here, we are initializing what arguments will be required when calling for add_coins
inventory_items = reqparse.RequestParser()
inventory_items.add_argument(
    "id", type=int, required = True)
inventory_items.add_argument(
    "itemName", type=str, help="Please give a name", required = True)
inventory_items.add_argument(
    "quantity", type=int, help="Please include a quantity", required = True)

resource_fields = {
    "id": fields.Integer,
    "itemName": fields.String,
    "quantity": fields.Integer
}



class addCoins(Resource):
    '''PURPOSE: This class is used to allow the associated root endpoint, "/", to enable users
    to add coins to the vending machine or delete the coins and get them back.'''
    
    def put(self):
        '''PUT method to enable users to add coins
        
        Users can add coins to the vending machine to be able to get items from
        the vending machine inventory. Negative numbers or adding 0 coins will throw
        an error back to the user
        '''
        
        # Parse arguments passed in from the body to be readable
        arguments = add_coins.parse_args()
        global coinCount  # Grab the global coinCount variable. Will not seem to work if this is not called like this
        
        if arguments.coin != 1:
            return {"message": "Can only put in 1 coin at a time. Please check if the value passed in the body was correct and try again"}, 403, {"X-Coins": coinCount}
        
        coinCount += arguments.coin
        return "", 204, {"X-Coins": coinCount}

    def delete(self):
        '''DELETE method to return all coins to the user
        
        Users can call this method to have the vending machines return all their coins to them.
        '''
        
        global coinCount
        returnedCoins = coinCount #Keep returned coins in a temp variable to return to the user
        coinCount = 0
        return "", 200, {"X-Coins": returnedCoins}


# Create a class that inherits from Resource object to allow the creation of resources
class vendingInventoryGeneral(Resource):
    '''PURPOSE: This class a general endpoint, "/inventory" to be called with a GET Method
    
    This class allows the endpoint "/inventory" to be called without having to specify an ID.
    By doing this, the class will show users what is currently left in the inventory for the vending machine.
    '''
    @marshal_with(resource_fields)
    def get(self):
        result = inventoryModel.query.all()
        return result
    
    @marshal_with(resource_fields)
    def put(self):
        args = inventory_items.parse_args()
        test = inventoryModel(id= args.id, itemName= args.itemName, quantity= args.quantity)
        db.session.add(test)
        db.session.commit()
        return test, 201

# Create a class that inherits from Resource object to allow the creation of resources
class vendingInventory(Resource):
    '''PURPOSE: This class allows the use of the "/inventory/<id> endpoint for several actions
    
    Users can get the current inventory of an item with a specific ID or buy that item
    as long as they put enough coins into the vending machine. If not enough coins are given,
    it will throw an error and allow users to continue putting in more coins as needed. Otherwise,
    coins are returned after a purchase is complete
    
    '''
    @marshal_with(resource_fields)
    def get(self, inputId):
        '''Returns the remaining quantity of a specific item associated with the ID'''
        
        result = inventoryModel.query.filter_by(id = inputId).first()
        if not result: #If user tries to access id outside of the range of the array
            response = Response(response = json.dumps({"message": "Unable to find item. Please try again"}), content_type="application/json", status = 404)
            response.headers["X-Coins"] = coinCount
            abort(response) #The abort function can also take Response objects
        return result

    def put(self, inputId):
        '''Action to buy a drink. Extra coins will be returned after transaction.
        Otherwise, users will have ability to still add in coins if not enough'''
        
        global coinCount
        # numDrinks = 2 % coinCount if coinCount > 0 else 0
        result = inventoryModel.query.filter_by(id = inputId).first()

        if not result:
            response = Response(response = json.dumps({"message": "Unable to find item. Please try again"}), content_type="application/json", status = 404)
            response.headers["X-Coins"] = coinCount
            abort(response) #The abort function can also take Response objects
        elif result.quantity == 0:
            response = Response(response = json.dumps({"message": "Item of id " + str(inputId) + " is out of stock. Please select another drink"}), content_type="application/json", status = 404)
            response.headers["X-Coins"] = coinCount
            abort(response) #The abort function can also take Response objects
            # return {'message': "Item of id " + str(id) + " is out of stock. Please select another drink"}, 404, {"X-Coins": coinCount}
        elif coinCount < 2:
            response = Response(response = json.dumps({"message": "Not enough coins. Please add more coins and try again"}), content_type="application/json", status = 403)
            response.headers["X-Coins"] = coinCount
            abort(response) #The abort function can also take Response objects

        # while (inventory[id] - numDrinks < 0 or coinCount - numDrinks*2 < 0) and numDrinks > 0:
        #     numDrinks -= 1

        returnedCoins = coinCount - 2
        coinCount = 0
        result.quantity -= 1
        db.session.commit() #Push new changes to value to database

        return {"quantity": 1, "change": returnedCoins}, {"X-Coins": returnedCoins, str(inputId)+"-Inventory-Remaining": result.quantity}


api.add_resource(vendingInventoryGeneral, "/inventory")
api.add_resource(vendingInventory, "/inventory/<int:inputId>")
api.add_resource(addCoins, "/")


if __name__ == "__main__":  # If this is the main, run this code
    app.run(debug=True)
