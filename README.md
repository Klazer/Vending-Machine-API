## Vending Machine API

### **Info**

***Version***: 0.6

***Maintainers***: Isaiah Herr

***Description***: This API is designed for the CM Group Interview using the Flask and Flask_Restful libraries in Python. There will be two solutions, one is a simpler solution in which a simple API is created that represents a vending machine. This vending machine is a very simple API where mostly everything is stored in memory.

A more complex solution, which is still being developed for fun, will have this vending machine be put into a Postgres database with a larger inventory of drinks and more operations. In addition to this, it is still in the planning process of how this will currently be tested and deployed. 

### **Important Variables**
| Variable | Description |
| :------- | :---------- |
| inventory | A simple inventory that contains 3 items with a quantity of 5 each using an array
| coinCount | Variable containing the number of coins a user has put into the vending machine
| add_coins | Variable containing the data passed in when executing an api call for adding coins
| app | Associated with the Flask class to indicate we're building a flask application
| api | Associated with the API class from the flask_restful library to indicate we're building a REST API

### ** Vending Machine API Endpoints **

| Verb | URI | Request Body | Response Code | Response Headers | Response Body |
| :--- | :-- | :----------- |:------------- | :--------------- | :------------ |
| PUT | / | {"coin": 1} | 204 | X-Coins: *[# of coins accepted] |{"coins": *[# of coins]|
| DELETE | / | | 204 | X-Coins: *[# of coins returned] |{"coins_returned": *[# of coins returned]|
| GET | /inventory || 200 || An array representing the inventory of remaining items|
| GET | /inventory/:id | | 200 || Remaining quantity of specific item associated with id |
| PUT | /inventory/:id || 200 |X-Coins: *[# of coins accepted], X-Inventory-Remaining: *[# of items remaining] | {"quantity": *[Number of items vended], "change": *[Number of coins returned]}|
| PUT | /inventory/:id || 404 | X-Coins: *[# of coins accepted] ||
| PUT | /inventory/:id || 403 | X-Coins: *[0 or 1] ||

**Note**: *[something] represents a dynamic value



### **How to Use**
This code can be executed from the vending_api.py file. Queries to the API can only be done after this file has been executed and can be done via Postman or through Python's builtin requests library. Currently, as the simple_api process is currently functional, this walkthrough will only focus on simple_api. A more detailed explanation will be below:

1. Clone this repository. Can be done using "git clone https://github.com/Klazer/Vending-Machine-API.git" through the command prompt if you have git installed.
    a. If you prefer to do this via the CLI or GUI, please go to these links respectively for instructions on how to do so: https://cli.github.com/manual/gh_repo_clone or https://docs.github.com/en/desktop/contributing-and-collaborating-using-github-desktop/adding-and-cloning-repositories/cloning-a-repository-from-github-to-github-desktop
2. Go to the simple_api folder and look for the requirements.txt file. Using the file, you can install all the necessary dependencies to allow the API to properly function locally on your workstation.
    a. A python virtual environment would be recommended to do this process if you would rather keep the dependencies separate.
3. Once dependencies have been installed, you can execute the webserver by simply executing the vending_api.py file.
    a. This can be done through your IDE of choice. In the case of this project, this api was developed in Visual Studio Code.
4. Once code has been executed and the webserver has been started on your localhost, you can now execute queries to the vending machine API using the address that is given to you. 
    a. The web server will usually give this message: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
  Running on ***http://localhost:port***
    b. Use the bolded section given to you as the base URI that you will be using to query endpoints from the API

### **Known Errors and Limitations***
- Code is only used for a development environment only!