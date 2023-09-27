from flask import jsonify, request, stream_with_context, Response
from queue import Queue
from utilities import initialize_bot
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.callbacks.base import BaseCallbackHandler
from utilities import initialize_bot
import os
import uuid
import threading
import json

load_dotenv()

users = {}  # Dictionary to store user queues based on user_id
openai_api_key = os.environ["OPENAI_API_KEY"]

class StreamingHandler(BaseCallbackHandler):
	def __init__(self, user_queue):
		self.user_queue = user_queue

	def on_llm_new_token(self, token: str, **kwargs) -> None:
		# self.user_queue.put(token)  # Push the token to the user's queue
		json_token = json.dumps(token)
		self.user_queue.put(json_token)

def query_bot_endpoint():
	llm = ChatOpenAI(streaming=True)

	user_id = str(uuid.uuid4())
	user_queue = Queue()
	users[user_id] = user_queue  # Store the user's queue in the dictionary

	llm.callbacks = [StreamingHandler(user_queue)]  # Initialize the callback with the user's queue

	agent = initialize_bot(llm)

	user_input = request.args.get('prompt', '')
	if not user_input:
		return jsonify({"error": "User input is required"}), 400

	def process_input():
		agent({"input": user_input})

	# Start the agent function in a separate thread
	threading.Thread(target=process_input).start()

	def sse_stream():
		while True:
			token = user_queue.get()
			yield f"data: {token}\n\n"

	return Response(stream_with_context(sse_stream()), content_type='text/event-stream')
