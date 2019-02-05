# myRetail Case Study

**Author:**  Kelly Erskine

**Start Date:**  Jan 30, 2019

## API Details

### GET

/products/{int:itemID}  - Get product details, requires matching item ID

Returns product ID, product name and product price in the following json format:

    {
    "ProductID": 51591640,
    "ProductName": "Cheetos Paws Cheese Flavored Snacks - 7.5oz",
    "ProductRetailPrice": "$3.79"
    }


## Assumptions:
 -  Mongodb is installed locally 
              datafile to import data is provided in GitHub: kaje28/myRetail/itemPriceInfoCollectionImport.crud.json
 -  Homebrew is installed


## Software used:
 -  MongoDB (installed locally on my Mac)
 -  Python 3.7.2 (default, Jan 13 2019, 12:51:54)

 
 ##  Installations and Setup:

  ####  Install MongoDB
      $ brew install mongodb
      
  ####  Install python 3.7.2
      $ brew install python3
 
  #### Python libraries installed
      $ pip3 install pymongo
      $ pip3 install flask
      $ pip3 install requests
      $ pip3 install pytest


  ####  Load datafile into MongoDB
  #####  Start database
      $ mongod
      
 ##### In another terminal create collection and run data import
  #####  Start MongoDB shell
     $ mongo
 #####  Switch database from default "test" to "myRetail"
     >  use myRetail
 ##### Create collection
     >  db.createCollection('itemPriceInfo')
 #####  You can exit MongoDB shell at this point
     >  quit()
     
  ###### *Download file from GitHub: itemPriceInfoCollectionImport.crud.json*
  
      $ mongoimport --db myRetail --collection itemPriceInfo --drop --file itemPriceInfoCollectionImport.crud.json
      
      
  #### Run web server locally (flask)
      $ python3 -m flask run
      
 ###  Testing
 ####  Run test script.  Tests the following:
 1.  The itemPriceInfo collection exists in the db
 2.  Runs the app for a valid Product ID
 3.  Runs the app for an invalid Product ID
 
 ###### *Be sure to download the pytest.ini file and the test_data folder with the itemPriceInfo.json file
 #### Run the test script.
     $ pytest myRetail_tests.py -v
