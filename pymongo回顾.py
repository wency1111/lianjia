import pymongo
conn=pymongo.MongoClient(host='localhost',
                   port=27017)
db=conn.testpymongo

myset=db.t1
myset.insert({"name":"Tom"})
