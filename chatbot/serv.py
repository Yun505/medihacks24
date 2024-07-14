from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from rag import execute_query
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from main import talk, check,advice,dispatch,emotion
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv('GOOGLE_API_KEY')

app = Flask(__name__)
CORS(app)  # Enable CORS

llm = ChatGoogleGenerativeAI(model="gemini-pro")


@app.route('/talk', methods=['POST'])
def talk():
    req_data = request.get_json()
    user_input = req_data['user_input']
    user_input = input("you: ")
    if(check()=="YES" and emotion()>0.8):
        print("1")
        msg = advice(user_input)
    elif(check()=="YES"):
        print("2")
        msg = dispatch(user_input)
    else:
        print("3")
        msg = talk(user_input) 
    return jsonify({"messages": msg})
        

if __name__ == '__main__':
    app.run(debug=True)