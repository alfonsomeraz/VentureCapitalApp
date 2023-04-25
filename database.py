import streamlit as st
import pymongo

# Initialize connection.
@st.cache_resource()
def init_connection():
  return pymongo.MongoClient(**st.secrets["mongo"])

client = init_connection()

# Pull data from the collection.
@st.cache_data(ttl=60)
def get_data():
  db = client["venture_capital"]
  items = db["deals"].find()
  items = list(items)
  return items

def add_data(data):
  db = client["venture_capital"]
  db["deals"].insert_one(data)





