from flask import Flask, g  
from flask_cors import CORS  
from endpoints import query_bot_endpoint
from utilities import initialize_tools  
from embedding_generator import create_embeddings
from dotenv import load_dotenv
import os

load_dotenv()

DEPLOYMENT_ENV = os.environ.get('DEPLOYMENT_ENV', 'DEVELOPMENT')
if DEPLOYMENT_ENV == 'PRODUCTION':
	# these lines swap the stdlib sqlite3 lib with the pysqlite3 package
	__import__('pysqlite3')
	import sys
	sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')	

app = Flask(__name__)
CORS(app)

create_embeddings()
initialize_tools()

app.add_url_rule('/query_bot', 'query_bot', query_bot_endpoint, methods=['GET'])

if __name__ == '__main__':
    app.run(debug=False)
