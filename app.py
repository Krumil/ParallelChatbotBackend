from flask import Flask, g  
from flask_cors import CORS  
from endpoints import query_bot_endpoint
from utilities import initialize_tools  

app = Flask(__name__)
CORS(app)

@app.before_first_request
def setup_tools():
    app.tools = initialize_tools()

app.add_url_rule('/query_bot', 'query_bot', query_bot_endpoint, methods=['GET'])

if __name__ == '__main__':
    app.run(debug=False)
