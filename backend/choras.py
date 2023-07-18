import os 
from dotenv import load_dotenv
from langchain.llms import OpenAI
# text stuff
from langchain.document_loaders import TextLoader
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.text_splitter import CharacterTextSplitter
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
llm = OpenAI(temperature=0.9)

# loads cleaned text file
file_path = '/Users/abelnoble/Desktop/Choras/database/university_of_michigan/text_fall2023.txt'
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

with open(file_path, "w", encoding="utf-8") as f:
    f.write(text) 
loader = TextLoader(file_path)
documents = loader.load()

# chunkz
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

# random open source embedding transformer (may need to change)
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# stored into chroma
db = Chroma.from_documents(docs, embedding_function)

# calling an agent to help out
vectorstore_info = VectorStoreInfo(name='ChorasDB', description='Course Data', vectorstore=db)
toolkit = VectorStoreToolkit(vectorstore_info=vectorstore_info)
agent = create_vectorstore_agent(llm=llm, toolkit=toolkit, verbose=True)



#### MAIN ####

st.title('🌸 Choras: Your AI Academic Advisor')
st.divider()

prompt = st.text_input('Let me help you find a class:')
st.caption('Ask \"What\'s a 4 credit class about Architecture that I can take in the mornings?')

if prompt:
    response = agent.run(prompt)
    st.write(response)

    with st.expander('Similarity Search'):
        search = db.similarity_search_with_score(prompt)
        st.write(search[0][0].page_content)
