# myRetail Case Study

**Author:**  Kelly Erskine

**Start Date:**  Jan 30, 2019

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
  
   ###### *modify file location in command below if different than listed*
      $ mongoimport --db myRetail --collection itemPriceInfo --drop --file ~/myRetail/itemPriceInfoCollectionImport.crud.json
      
      
  #### Run web server locally (flask)
      $ python3 -m flask run
