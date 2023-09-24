from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.agents.agent_toolkits import create_retriever_tool
from langchain.agents.agent_toolkits import create_conversational_retrieval_agent
import os

load_dotenv()

os.getenv("LANGCHAIN_TRACING_V2")
os.getenv("LANGCHAIN_ENDPOINT")
os.getenv("LANGCHAIN_API_KEY") 
os.getenv("LANGCHAIN_PROJECT")  

openai_api_key = os.environ["OPENAI_API_KEY"]

pdf_vectorstore = Chroma(persist_directory="./pdf_chroma_db", embedding_function=OpenAIEmbeddings())
pdf_retriever = pdf_vectorstore.as_retriever()

csv_vectorstore = Chroma(persist_directory="./csv_chroma_db", embedding_function=OpenAIEmbeddings())
csv_retriever = csv_vectorstore.as_retriever()

gitbook_vectorstore = Chroma(persist_directory="./gitbook_chroma_db", embedding_function=OpenAIEmbeddings())
gitbook_retriever = gitbook_vectorstore.as_retriever()

main_tool = create_retriever_tool(
	pdf_retriever, 
	"parallel_tcg",
	"Useful for answering questions about Parallel TCG"
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

def initialize_bot(llm):
	agent_executor = create_conversational_retrieval_agent(llm, tools, verbose=True)
	return agent_executor

