import google.generativeai as genai
from dotenv import load_dotenv
import google.ai.generativelanguage as glm
from google.generativeai.types.content_types import *
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.schema import AIMessage,HumanMessage,SystemMessage
from langchain_core.output_parsers import StrOutputParser
from rag import execute_query
import os

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv('GOOGLE_API_KEY')
OPENAI_KEY=os.getenv("OPENAI_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-pro")
temp= """You are a general health counselling bot you will talk to the user and help them with their issue based on this {Input}. 
         IF NECESSARY You will also suggest people to talk to based on the provided information {ppl}
         
         NOTE - Only return one response
        """
prompt = ChatPromptTemplate.from_template(temp)
messages = {"human": [], "ai":[]}
parser = StrOutputParser()
chain = prompt | llm | parser
user_input = ""


def talk(user_input):
    user_input = input("you: ")
    messages["human"].append(user_input)
    str1=""
    cons=execute_query(str1.join(messages["human"]))
    print(cons)
    ai_response = chain.invoke({"ppl" : cons, "Input": user_input})
    print(ai_response)
    messages["ai"].append(ai_response)