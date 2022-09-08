from flask import Flask
from flask_restful import Api, Resource, abort, reqparse
from sqlalchemy import Integer

app = Flask(__name__)  # Creates our app within flask
# Will wrap our app in an API and initializes the fact we're using a restful API
api = Api(app)

inventory = [5, 5, 5]
coinCount = 0

add_coins = reqparse.RequestParser()
add_coins.add_argument(
    "coin", type=int, help="Must include a coin to be added. Please try again", required = True)


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
    
    def get(self):
        return {"inventory": inventory}

# Create a class that inherits from Resource object to allow the creation of resources
class vendingInventory(Resource):
    '''PURPOSE: This class allows the use of the "/inventory/<id> endpoint for several actions
    
    Users can get the current inventory of an item with a specific ID or buy that item
    as long as they put enough coins into the vending machine. If not enough coins are given,
    it will throw an error and allow users to continue putting in more coins as needed. Otherwise,
    coins are returned after a purchase is complete
    
    '''

    def get(self, id):
        '''Returns the remaining quantity of a specific item associated with the ID'''
        
        if id > len(inventory)-1:
            return {'message': "Item of id " + str(id) + " not found. Please try again"}, 404, {"X-Coins": coinCount}
        return {"item_" + str(id) + "_quantity": inventory[id]}

    def put(self, id):
        '''Action to buy a drink. Extra coins will be returned after transaction.
        Otherwise, users will have ability to still add in coins if not enough'''
        
        global coinCount
        # numDrinks = 2 % coinCount if coinCount > 0 else 0

        if id > len(inventory)-1:
            return {'message': "Item of id " + str(id) + " not found. Please try again"}, 404, {"X-Coins": coinCount}
        if coinCount < 2:
            return {'message': "Not enough coins. Please add more coins and try again"}, 403, {"X-Coins": coinCount}

        # while (inventory[id] - numDrinks < 0 or coinCount - numDrinks*2 < 0) and numDrinks > 0:
        #     numDrinks -= 1

        returnedCoins = coinCount - 2
        coinCount = 0
        inventory[id] -= 1

        return {"quantity": 1, "change": returnedCoins}, {"X-Coins": returnedCoins, str(id)+"-Inventory-Remaining": inventory[id]}


api.add_resource(vendingInventoryGeneral, "/inventory")
api.add_resource(vendingInventory, "/inventory/<int:id>")
api.add_resource(addCoins, "/")


if __name__ == "__main__":  # If this is the main, run this code
    app.run(debug=True)
