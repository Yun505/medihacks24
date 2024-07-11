from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from rag import execute_query
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv('GOOGLE_API_KEY')

app = Flask(__name__)
CORS(app)  # Enable CORS

llm = ChatGoogleGenerativeAI(model="gemini-pro")

temp = """You are a general health counselling bot you will talk to the user and help them with their issue based on this {Input}. 
         IF NECESSARY You will also suggest people to talk to based on the provided information {ppl}
         
         NOTE - Only return one response
        """
prompt = ChatPromptTemplate.from_template(temp)
parser = StrOutputParser()
chain = prompt | llm | parser
messages = {"human": [], "ai": []}

@app.route('/talk', methods=['POST'])
def talk():
    global messages
    req_data = request.get_json()
    print(req_data)
    user_input = req_data['user_input']

    messages["human"].append(user_input)

    #concatenated_input = " ".join(messages["human"])
    
    cons = execute_query(user_input)
    ai_response = chain.invoke({"ppl": cons, "Input": user_input})
    messages["ai"].append(ai_response)

    print(ai_response)
    response_data = {"messages": messages, "people": cons}
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)