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
import threading
import time


load_dotenv()

users = {}  # Dictionary to store user queues based on user_id
agents = {}  # Dictionary to store agents based on user_id
openai_api_key = os.environ["OPENAI_API_KEY"]

class StreamingHandler(BaseCallbackHandler):
	def __init__(self, user_queue):
		self.user_queue = user_queue

	def on_llm_new_token(self, token: str, **kwargs) -> None:
		json_token = json.dumps(token)
		self.user_queue.put(json_token)

def query_bot_endpoint():
	llm = ChatOpenAI(streaming=True)

	user_id = request.args.get('user_id')
	if not user_id:
		return jsonify({"error": "User ID is required"}), 400

	# Check if user already has an agent
	if user_id not in agents:
		user_queue = Queue()
		users[user_id] = user_queue  # Store the user's queue in the dictionary

		llm.callbacks = [StreamingHandler(user_queue)]  # Initialize the callback with the user's queue

		current_time = time.time()  # Get the current timestamp
		agent = initialize_bot(llm)
		agents[user_id] = agent  # Store the agent in the dictionary
	else:
		agent = agents[user_id]

	user_input = request.args.get('prompt', '')
	if not user_input:
		return jsonify({"error": "User input is required"}), 400

	def process_input():
		agent({"input": user_input})

	# Start the agent function in a separate thread
	threading.Thread(target=process_input).start()

	def sse_stream():
		while True:
			token = users[user_id].get()
			yield f"data: {token}\n\n"

	return Response(stream_with_context(sse_stream()), content_type='text/event-stream')


def cleanup_old_agents():
	while True:
		current_time = time.time()  # Get the current timestamp
		agents_to_remove = []

		# Check the age of each agent
		for user_id, agent_data in agents.items():
			agent_creation_time = agent_data['timestamp']
			if current_time - agent_creation_time > 86400:  # 86400 seconds = 24 hours
				agents_to_remove.append(user_id)

		# Remove old agents
		for user_id in agents_to_remove:
			del agents[user_id]

		time.sleep(60)  # Wait for 60 seconds (1 minute) before checking again

