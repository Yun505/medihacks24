import os
from dotenv import load_dotenv
from langchain_openai.chat_models import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import CharacterTextSplitter
from pinecone import Pinecone
from langchain_community.vectorstores import Pinecone as Pine
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import List, Dict
load_dotenv()
PINECONE_API_KEY=os.getenv("PINECONE_API_KEY")
os.environ["GOOGLE_API_KEY"] = os.getenv('GOOGLE_API_KEY')
OPENAI_KEY=os.getenv("OPENAI_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-pro")
parser = StrOutputParser()
chain = llm | parser
user_input = ""
def load_data():
    loader = TextLoader(r"comms.md")
    documents = loader.load()
    text_splitter = CharacterTextSplitter(
        separator=";",
         chunk_size=100,
        chunk_overlap=50,
        length_function=len,
        is_separator_regex=False, )
    docs=text_splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings( model="text-embedding-3-small", openai_api_key=OPENAI_KEY)
    index_name="dd"
    Pinecone=PineconeVectorStore.from_documents(docs,embeddings,index_name=index_name)
    print(Pinecone.similarity_search("depression", k=3))
    
def execute_query(query):
    
    pc=Pinecone(api_key=PINECONE_API_KEY)
    embeddings = OpenAIEmbeddings( model="text-embedding-3-small", openai_api_key=OPENAI_KEY)
    index=pc.Index("dd")
    vectorstore=PineconeVectorStore(index, embeddings)
    out=vectorstore.similarity_search(query, k=3)
    temp="You have to return the data in a list like format which can be read by a program {in}"
    fin =parse_info(out)
    return fin
    
def parse_info(documents: List[Dict]) -> List[Dict]:
    parsed_data = []

    for doc in documents:
        content = doc.page_content
        lines = content.split('\n')
        person_dict = {}
      
        first_line = lines[0].strip()
        if '**' in first_line:
            person_dict['Name'] = first_line.split('**')[1].strip()

        for line in lines[1:]:
            if 'Overcame:' in line:
                person_dict['Overcame'] = line.split(': ')[1].strip()
            elif 'Specialty:' in line:
                person_dict['Specialty'] = line.split(': ')[1].strip()
            elif 'Support Area:' in line:
                person_dict['Support Area'] = line.split(': ')[1].strip()
            elif 'Expertise:' in line:
                person_dict['Expertise'] = line.split(': ')[1].strip()
            elif 'Story:' in line:
                person_dict['Story'] = line.split(': ')[1].strip()
        
        parsed_data.append(person_dict)

    return parsed_data
    
