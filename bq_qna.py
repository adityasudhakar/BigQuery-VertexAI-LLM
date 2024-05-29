# bq_qna.py
from sqlalchemy import create_engine, MetaData
from langchain import SQLDatabase, SQLDatabaseChain
from langchain.prompts.prompt import PromptTemplate
from config import table_name, table_uri
from initialize import llm

def create_db_chain():
    engine = create_engine(table_uri)
    db = SQLDatabase(engine=engine, metadata=MetaData(bind=engine), include_tables=[table_name])
    db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True, return_intermediate_steps=True)
    return db_chain

# Initialize DB Chain once and reuse
db_chain = create_db_chain()

def bq_qna(question):
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

    final_prompt = BigQuerySQL_PROMPT.format(input=question, table_info=table_name, top_k=10000)
    output = db_chain(final_prompt)

    return output['result'], output['intermediate_steps'][0]
