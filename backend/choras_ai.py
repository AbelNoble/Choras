import streamlit as st
from langchain.chains import LLMChain, SimpleSequentialChain
from langchain.llms import OpenAI 
from langchain.prompts import PromptTemplate
from langchain import Langchain

# Initialize the Langchain model
model = Langchain()

# Set the prompt for text generation
prompt = "Once upon a time"

# Generate text using Langchain
response = model.generate(prompt)

# Print the generated text
print(response.text)
