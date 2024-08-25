from langchain import OpenAI, SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
import environ
import os

os.environ["OPENAI_API_KEY"] = ""

OPENAI_API_KEY = ""

env = environ.Env()
environ.Env.read_env()

# Setup database
db = SQLDatabase.from_uri(
    f"postgresql+psycopg2://postgres:{env('DBPASS')}@localhost:5432/{env('DATABASE')}",
)

# setup llm
llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)



# Create db chain
QUERY = """
Given an input question, first create a syntactically correct postgresql query to run, then look at the results of the query and return the answer.
Use the following format:

Question: Question here
SQLQuery: SQL Query to run
SQLResult: Result of the SQLQuery
Answer: Final answer here

{question}
"""

# Setup the database chain
db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)


## setup to run
prompt = 'how many order management tasks have been completed or open'

### format Db chain with the prompt from the user 
question = QUERY.format(question=prompt)

### ask LLM for the response based on the formatted question
db_chain.run(question)


