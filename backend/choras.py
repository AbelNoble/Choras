import os 
from dotenv import load_dotenv
from langchain.llms import OpenAI
# text stuff
from langchain.document_loaders import TextLoader
from langchain.text_splitter import NLTKTextSplitter
from langchain.embeddings import OpenAIEmbeddings
# vector store stuff
from langchain.vectorstores import Chroma
from langchain.agents.agent_toolkits import (create_vectorstore_agent, VectorStoreToolkit, VectorStoreInfo)
# ui stuff
import streamlit as st



#### PRELIMINARY ####

# initialize key
load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

# sets llm **creativity**
llm = OpenAI(temperature=1, verbose=True)
embeddings = OpenAIEmbeddings()

# loads cleaned text file
file_path = '/Users/abelnoble/Desktop/Choras/database/university_of_michigan/text_fall2023.txt'
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

with open(file_path, "w", encoding="utf-8") as f:
    f.write(text) 
loader = TextLoader(file_path)
documents = loader.load()

nltk_text_splitter = NLTKTextSplitter(chunk_size=1000)

docs = nltk_text_splitter.create_documents([text])

vectordb = Chroma.from_documents(documents=docs, embedding=embeddings)

# calling an agent to help out
vectorstore_info = VectorStoreInfo(name='ChorasDB', description='Course Data', vectorstore=vectordb)
toolkit = VectorStoreToolkit(vectorstore_info=vectorstore_info)
agent = create_vectorstore_agent(llm=llm, toolkit=toolkit, verbose=True)



#### MAIN ####

st.title('🌸 Choras: Your AI Academic Advisor')
st.divider()

prompt = st.text_input('Let me help you find a class:')
st.caption('Ask \"What\'s a 4 credit class about Architecture that I can take in the mornings?\"')

if prompt:
    print("Prompt length:", len(prompt))
    response = agent.run(prompt)
    st.write(response)

    # with st.expander('Similarity Search'):
    #     search = vectordb.similarity_search_with_score(prompt)
    #     st.write(search[0][0].page_content)
