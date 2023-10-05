from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.agents.agent_toolkits import create_retriever_tool
from langchain.agents.openai_functions_agent.agent_token_buffer_memory import AgentTokenBufferMemory
from langchain.agents.openai_functions_agent.base import OpenAIFunctionsAgent
from langchain.schema.messages import SystemMessage
from langchain.prompts import MessagesPlaceholder
from langchain.agents import AgentExecutor
from flask import current_app as app  
import os

load_dotenv()

os.getenv("LANGCHAIN_TRACING_V2")
os.getenv("LANGCHAIN_ENDPOINT")
os.getenv("LANGCHAIN_API_KEY") 
os.getenv("LANGCHAIN_PROJECT")  

DEPLOYMENT_ENV = os.environ.get('DEPLOYMENT_ENV', 'DEVELOPMENT')

if DEPLOYMENT_ENV == 'PRODUCTION':
	base_directory = "./embeddings/"
	# base_directory = "/var/data/embeddings/"
else:
	base_directory = ".\\embeddings\\"

print(os.getcwd())

openai_api_key = os.environ["OPENAI_API_KEY"]

def initialize_tools():
	print(os.path.join(base_directory, "gitbook_chroma_db"))
	print(os.path.join(base_directory, "csv_chroma_db"))
	print(os.path.join(base_directory, "pdf_chroma_db"))
	pdf_vectorstore = Chroma(persist_directory=os.path.join(base_directory, "pdf_chroma_db"), embedding_function=OpenAIEmbeddings())
	pdf_retriever = pdf_vectorstore.as_retriever()

	csv_vectorstore = Chroma(persist_directory=os.path.join(base_directory, "csv_chroma_db"), embedding_function=OpenAIEmbeddings())
	csv_retriever = csv_vectorstore.as_retriever()

	gitbook_vectorstore = Chroma(persist_directory=os.path.join(base_directory, "gitbook_chroma_db"), embedding_function=OpenAIEmbeddings())
	gitbook_retriever = gitbook_vectorstore.as_retriever()

	pdf_documents = pdf_vectorstore.get()['documents']
	csv_documents = csv_vectorstore.get()['documents']
	gitbook_documents = gitbook_vectorstore.get()['documents']

	# print all first documents
	print(pdf_documents[0])
	print(csv_documents[0])
	print(gitbook_documents[0])

	main_tool = create_retriever_tool(
		pdf_retriever, 
		"parallel_tcg",
		"Documents detail 'Parallel', a post-apocalyptic trading card game with five human factions, and its 'Echo Replication' feature allowing creation of Echo cards using in-game resources."
	)
	csv_tool = create_retriever_tool(
		csv_retriever,
		"cards_database",
		"Useful for answering questions about cards"
	)
	gitbook_tool = create_retriever_tool(
		gitbook_retriever,
		"echelon_docs",
		"Useful for answering questions about PRIME, Echelon, and the anything related to the economics of the Parallel ecosystem"
	)
	
	tools = [main_tool, csv_tool, gitbook_tool]

	return tools

# pdf_vectorstore = Chroma(persist_directory=os.path.join(base_directory, "pdf_chroma_db"), embedding_function=OpenAIEmbeddings())
# pdf_retriever = pdf_vectorstore.as_retriever()

# csv_vectorstore = Chroma(persist_directory=os.path.join(base_directory, "csv_chroma_db"), embedding_function=OpenAIEmbeddings())
# csv_retriever = csv_vectorstore.as_retriever()

# gitbook_vectorstore = Chroma(persist_directory=os.path.join(base_directory, "gitbook_chroma_db"), embedding_function=OpenAIEmbeddings())
# gitbook_retriever = gitbook_vectorstore.as_retriever()

# print(os.path.join(base_directory, "gitbook_chroma_db"))
# print(os.path.join(base_directory, "csv_chroma_db"))
# print(os.path.join(base_directory, "pdf_chroma_db"))

# main_tool = create_retriever_tool(
# 	pdf_retriever, 
# 	"parallel_tcg",
# 	"Documents detail 'Parallel', a post-apocalyptic trading card game with five human factions, and its 'Echo Replication' feature allowing creation of Echo cards using in-game resources."
# )
# csv_tool = create_retriever_tool(
# 	csv_retriever,
# 	"cards_database",
# 	"Useful for answering questions about cards"
# )
# gitbook_tool = create_retriever_tool(
# 	gitbook_retriever,
# 	"echelon_docs",
# 	"Useful for answering questions about PRIME, Echelon, and the anything related to the economics of the Parallel ecosystem"
# )
# tools = [main_tool, csv_tool, gitbook_tool]



def initialize_bot(llm):
	# Memory Component
	memory_key = "history"
	memory = AgentTokenBufferMemory(memory_key=memory_key, llm=llm, max_history=2, max_token_limit= 3000)
	tools = app.tools
	print(tools)

	# Prompt Template
	system_message = SystemMessage(
		content=(
			"Do your best to answer the questions about Parallel TCG. "
			"Feel free to use any tools available to look up relevant information."
		)
	)
	prompt = OpenAIFunctionsAgent.create_prompt(
		system_message=system_message,
		extra_prompt_messages=[MessagesPlaceholder(variable_name=memory_key)]
	)

	# Agent
	agent = OpenAIFunctionsAgent(llm=llm, tools=tools, prompt=prompt)

	# Agent Executor
	return AgentExecutor(agent=agent, tools=tools, memory=memory, verbose=True, return_intermediate_steps=True)    
