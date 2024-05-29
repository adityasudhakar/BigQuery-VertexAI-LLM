# initialize.py
from google.auth.transport.requests import Request
import google.auth
import langchain
from google.cloud import aiplatform
import vertexai
from vertex_wrapper import VertexLLM, VertexChat, VertexEmbeddings, VertexMultiTurnChat

from config import PROJECT_ID, LOCATION, REQUESTS_PER_MINUTE

def initialize_vertex_ai():
    credentials, _ = google.auth.default()
    auth_req = Request()
    credentials.refresh(auth_req)

    # Initialize Vertex AI SDK
    vertexai.init(project=PROJECT_ID, location=LOCATION)

    llm = VertexLLM(
        model_name='text-bison@001',
        max_output_tokens=1024,
        temperature=0.1,
        top_p=0.8,
        top_k=40,
        verbose=True,
    )

    chat = VertexChat()
    mchat = VertexMultiTurnChat(max_output_tokens=1024)
    embedding = VertexEmbeddings(requests_per_minute=REQUESTS_PER_MINUTE)

    return llm, chat, mchat, embedding

# Initialize once and reuse
llm, chat, mchat, embedding = initialize_vertex_ai()
