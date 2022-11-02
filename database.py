import os
from unicodedata import name

from deta import Deta #pip install deta
from dotenv import load_dotenv

#Load the environment variables
load_dotenv(".env")
DETA_KEY = os.getenv("DETA_KEY")

#Initialize with a project key
deta = Deta(DETA_KEY)

#this is how to create\connect a database
db = deta.Base("work_reports")

def insert_profile(daytime, name, date, work, time, switch):
    """Returns the report on a successful creation, otherwise raises an error"""
    return db.put({"key": daytime, "name":name, "date":date, "work":work, "time":time, "switch":switch})

def fetch_all_profile():
    """Returns a dict of all of name"""
    res = db.fetch()
    return res.items

def get_private(daytime):
    """if not found, the function will return None"""
    return db.get(daytime)

