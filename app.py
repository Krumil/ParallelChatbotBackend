from flask import Flask
from flask_cors import CORS  
from endpoints import query_bot_endpoint

app = Flask(__name__)
CORS(app)

app.add_url_rule('/query_bot', 'query_bot', query_bot_endpoint, methods=['GET'])
# app.add_url_rule('/query_bot_stream', 'query_bot_stream', sse_stream_endpoint, methods=['GET'])

if __name__ == '__main__':
	app.run(debug=False)
