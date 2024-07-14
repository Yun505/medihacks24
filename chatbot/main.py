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
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)
from sent import analyze_emotions

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv('GOOGLE_API_KEY')
OPENAI_KEY=os.getenv("OPENAI_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", )
llm2= ChatGoogleGenerativeAI(model="gemini-pro", )
parser = StrOutputParser()
messages = {"human": [], "ai":[]}


def talk(user_input):
    temp= """You are an emergency dispatcher chatbot. You are talking to an user and this is what you know about the user so far based on your previous conversation;; {messages};;  
        This is the user's latest input;; {input};; 
        You have been trained thorougly and your primarly goal is to extract as much 
        information as possible from the user while consoling them. The things that you need to ask in order of importance are:;;
        1. Where are you located and what is your name?;; 2. What is the emergency?;; 3. What is your name?;; 4. Are there any victims and if so what are their conditions?;;
        
       
        If you think a question has already been answered based on the user's previous questions you don't need to ask them again and move on to the next question
        Take your time and make sure you get all the information by asking questions
        While keeping the above in mind, respond to the user with a message that will help you extract more information from them.;;
        """
    prompt = ChatPromptTemplate.from_template(temp)
    
    
    chain = prompt | llm | parser
    messages["human"].append(user_input)
    
    ai_response = chain.invoke({"input":user_input, "messages": messages["human"]})
    print(ai_response)
    messages["ai"].append(ai_response)
    return messages

def check():
    temp="""You are part of an emergency dispatch team. Your colleague has been talking to a user and 
    this is what they know about the user so far based on their previous conversation;; {messages};;
    Your job is to determine if the user has provided enough information for the emergency dispatch team to send help.
    The things that you need to check for are:;; 1. User's location and name;; 2. Nature of the emergency;;
    
    Return YES if you think the user has provided enough information for the emergency dispatch team to send help and NO if you think they haven't provided enough information.
    Take your time and make sure you check all the information provided by the user. You can returm YES if you think almost all of the info has been provided
    
    
    NOTE - ONLY RETURN YES OR NO
    """
    prompt = ChatPromptTemplate.from_template(temp)
    chain = prompt | llm2 | parser
    response= chain.invoke({"messages": messages})
    print(response)
    return response

def emotion():
    avg_sadness=0
    for message in messages["human"]:
        scores =analyze_emotions(message)
        sadness=0
        for emotion in scores[0]:
            if emotion['label']=="sadness":
                sadness=emotion['score']
        avg_sadness+=sadness
    avg_sadness=avg_sadness/len(messages)
    print(avg_sadness)
    return avg_sadness

def advice(user_input):
    
    temp= """You are part of an emergency dispatch service. The user has found to be sad and is facing some issue. 
         This is what you know about the user so far based on your previous conversation;; {messages};;
         You will talk to the user and help them with their issue based on this {input}. 
         IF NECESSARY You will also suggest people to talk to based on the provided information {ppl}
         
         NOTE - Only return one response
        """
    prompt = ChatPromptTemplate.from_template(temp)
    chain = prompt | llm | parser
    str1=""
    cons=execute_query(str1.join(messages["human"]))
    print(cons)
    ai_response = chain.invoke({"input":user_input, "messages": messages["human"], "ppl":cons})
    messages["human"].append(user_input)
    messages["ai"].append(ai_response)
    return messages
    
def dispatch(user_input):
    temp="""You are part of an emergency dispatch team. Your colleague has been talking to a user and this is what they know about the user so far based on their previous conversation;; {messages};;
            They have determined that the user has provided enough information for the emergency dispatch team to send help. 
            This is the user's latest input {input}. 
          
            You need to respond to this input and let the user know that help is on the way and how long it will take for help to arrive.
            If this has already been done you need to keep talking to user and help them make feel better until help arrives.
           
            """ 
    prompt = ChatPromptTemplate.from_template(temp)
    chain = prompt | llm | parser
    ai_response = chain.invoke({"input":user_input, "messages": messages["human"]})
    messages["human"].append(user_input)
    messages["ai"].append(ai_response)
    print(ai_response)
    return messages
               

if __name__ == "__main__":
    while True:
        user_input = input("you: ")
        if(check(messages)=="YES" and emotion()>0.8):
            print("1")
            advice(user_input)
        elif(check(messages)=="YES"):
            print("2")
            dispatch(user_input)
        else:
            print("3")
            talk(user_input) 
        print(messages)