import streamlit as st
import pymongo

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource()
def init_connection():
  return pymongo.MongoClient(**st.secrets["mongo"])

client = init_connection()


# Pull data from the collection.

def get_data():
  db = client["venture_capital"]
  collection = db["deals"]
  return collection

