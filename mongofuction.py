import pymongo

import configparser

config = configparser.ConfigParser()
config.read('config.ini')

username = config.get('mongodb', 'username')
password = config.get('mongodb', 'password')
hostlocation = config.get('mongodb', 'hostlocation')
# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
cluster_url =f"mongodb+srv://{username}:{password}@{hostlocation}/?retryWrites=true&w=majority&appName=GueiMing"
myclient = pymongo.MongoClient(cluster_url, username=username,password=password)

def dbmethod(database : str , collcetion : str):
    mydb = myclient[database]
    mycol =mydb[collcetion]
    
    return mycol


