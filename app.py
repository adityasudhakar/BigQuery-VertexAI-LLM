from google.auth import default
import google.auth.transport.requests
from sqlalchemy import *
from sqlalchemy.engine import create_engine
from sqlalchemy.schema import *
import pandas as pd
from vertex_wrapper import VertexLLM, VertexChat, VertexEmbeddings, VertexMultiTurnChat


credentials, project = default()
auth_req = google.auth.transport.requests.Request()
credentials.refresh(auth_req)

PROJECT_ID = "spartan-acrobat-536"  # @param {type:"string"} ## Update this with your project id
LOCATION = "us-central1" # @param {type:"string"} ## Continue with us-central1

import langchain
print(f"LangChain version: {langchain.__version__}")

from google.cloud import aiplatform
print(f"Vertex AI SDK version: {aiplatform.__version__}")

# Initialize Vertex AI SDK
import vertexai
vertexai.init(project=PROJECT_ID, location=LOCATION)


REQUESTS_PER_MINUTE = 100

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


from google.cloud import bigquery
from google.cloud.bigquery import Client
client = Client(project=PROJECT_ID)
dataset_id = "spartan-acrobat-536"

# @title Specify Project details and location of the BQ table

project_id = PROJECT_ID  # @param {type:"string"}
location = LOCATION  # @param {type:"string"}
dataset_id = 'javascript' # @param {type:"string"}
table_name = 'pages' # @param {type:"string"}

table_uri = f"bigquery://{project_id}/{dataset_id}"
engine = create_engine(f"bigquery://{project_id}/{dataset_id}")

from langchain import SQLDatabase, SQLDatabaseChain
from langchain.prompts.prompt import PromptTemplate

def bq_qna(question):
  #create SQLDatabase instance from BQ engine
  db = SQLDatabase(engine=engine,metadata=MetaData(bind=engine),include_tables=[table_name])
  # db = SQLDatabase(engine=engine,metadata=MetaData(bind=engine),include_tables=['bigquery-public-data.iowa_liquor_sales.sales'])

  #create SQL DB Chain with the initialized LLM and above SQLDB instance
  db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True, return_intermediate_steps=True)

  #Define prompt for BigQuery SQL
  _googlesql_prompt = """You are a BigQuery SQL expert. Given an input question, first create a syntactically correct BigQuery query to run, then look at the results of the query and return the answer to the input question.
  Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per BigQuery SQL. You can order the results to return the most informative data in the database.
  Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in backticks (`) to denote them as delimited identifiers.
  Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
  Use the following format:
  Question: "Question here"
  SQLQuery: "SQL Query to run"
  SQLResult: "Result of the SQLQuery"
  Answer: "Final answer here"
  Only use the following tables:
  {table_info}

  If someone asks for specific month, use ActivityDate between current month's start date and current month's end date

  Question: {input}"""

  BigQuerySQL_PROMPT = PromptTemplate(
      input_variables=["input", "table_info", "top_k"],
      template=_googlesql_prompt,
  )

  #passing question to the prompt template
  final_prompt = BigQuerySQL_PROMPT.format(input=question, table_info=table_name, top_k=10000)

  #pass final prompt to SQL Chain
  output = db_chain(final_prompt)

  print("Output Keys", output.keys())
  return output['result'] , output['intermediate_steps'][0]

#Testing 1
# bq_qna('Count total number of context_actions')
# name any three context_timezone?

import streamlit as st
from streamlit_chat import message as st_message

def main():
    st.title("BigQuery QnA Chatbot")

    # Initialize session state variables for storing conversation history
    if 'conversation' not in st.session_state:
        st.session_state.conversation = []

    # Input box for the question
    question = st.text_input("Enter your question:")

    if st.button("Send"):
        if question:
            try:
                # Call the bq_qna function with the user's question
                answer, intermediate_steps = bq_qna(question)

                # Append question, answer, and intermediate steps to the conversation history
                st.session_state.conversation.append((question, answer, intermediate_steps))

            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.error("Please enter a question")

    # Display the conversation history using streamlit_chat
    for i, (q, a, steps) in enumerate(st.session_state.conversation):
        st_message(q, is_user=True, key=str(i) + '_user')
        st_message(a, is_user=False, key=str(i) + '_bot')
        with st.expander(f"Intermediate Steps for Q {i+1}"):
            st.write(steps)

    # Button to clear the conversation history
    if st.button("Clear Conversation"):
        st.session_state.conversation = []

if __name__ == "__main__":
    main()


