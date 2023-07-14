import os 
from dotenv import load_dotenv
from langchain.llms import OpenAI
import streamlit as st

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')



