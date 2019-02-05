#!/usr/bin/env python3

import json
import requests
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, InvalidName
from flask import Flask

app = Flask(__name__)

# For simplicity I left these here but to allow for different environments I would put these values into a config file or config service
dbName = "myRetail"
dbConnectionString = 'mongodb://localhost:27017'
productInfoURL = 'http://redsky.target.com/v2/pdp/tcin/{}?excludes=taxonomy,price,promotion,bulk_ship,rating_and_review_reviews,rating_and_review_statistics,question_answer_statistics'

#  Create a MongoDB client object with a 2 second connect timeout so we quickly return during failures instead of blocking for 30 seconds
client = MongoClient(dbConnectionString, connectTimeoutMS=2000, serverSelectionTimeoutMS=2000)

try:
  client.admin.command('ismaster')
except ConnectionFailure:
  app.logger.info('Unable to connect to MongoDB, subsequent requests will likely fail')

db = client[dbName]

# Getting product info from myRetail (RedSky) API
def getProductName (itemID, myRetailURL):
  req = requests.get(url = myRetailURL)
  if req.status_code == 200:
    itemInfo = req.json()
    productTitle = itemInfo['product']['item']['product_description']['title']

    return (productTitle)
  else:
    app.logger.info('Invalid response received from myRetail.  myRetail is offline or unreachable.')
    return None

#  Getting price from MongoDB data source
def getProductPrice (itemID, db):
  # ismaster is basically a simple no-op command to make sure Mongod is up and working
  try:
    client.admin.command('ismaster')
  except ConnectionFailure:
    app.logger.info('Unable to connect to MongoDB, subsequent requests will likely fail')
    # Return False to whoever called us since we are unable to query the DB
    return False

  try:
    itemPriceInfo = db.itemPriceInfo
  except pymongo.errors.InvalidName:
    app.logger.info('Invalid Collection name')
    return False

  item = itemPriceInfo.find_one({ "itemID": itemID})
  if item:
    if item['isOfferOnSale'] == "Y":
      productPrice = item['salePrice']['formattedPrice']
    else:
      productPrice = item['currentPrice']['formattedPrice']
  else:
    # No matching item found in DB, return None and let the calling function handle it
    return None

  return (productPrice)
  
@app.route('/products/<int:itemID>', methods=['GET'])
def getItemDetails(itemID):

  myRetailURL = productInfoURL.format(itemID) 

  productName = getProductName(itemID, myRetailURL)
  productRetailPrice = getProductPrice(itemID, db)
  
  if productName is None:
    jsonProductData = {'ProductID' : itemID, 'ProductName' : 'Valid Product ID not entered' }
  elif productRetailPrice is None:
    jsonProductData = {'Database Error' : productPrice }
  else:
    jsonProductData = {'ProductID' : itemID, 'ProductName' : productName , 'ProductRetailPrice' : productRetailPrice }

  response = app.response_class(response=json.dumps(jsonProductData), status=200, mimetype='application/json')
  return (response)

# Close the db connection on exit
client.close()

if __name__ == "__main__":
    app.run()


