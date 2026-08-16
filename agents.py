from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
from dotenv import load_dotenv


load_dotenv()

llm = ChatOpenAI(
    model="gpt-5.6",
    reasoning_effort="none"
)

# Search Agent
def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search],
        system_prompt="""
        You are a research search agent.

        Your job is to collect reliable information about the user's topic.

        Rules:
        1. Use the web_search tool when needed.
        2. Perform at most 3 searches.
        3. Do not repeat the same search.
        4. After collecting sufficient information, stop using tools.
        5. Return a concise summary containing the important findings,
           titles, URLs and snippets.
        """
    )

# Reader Agent

def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url],
        system_prompt="""
        You are a research reader agent.

        Your job is to select the most relevant URL from the
        provided search results and scrape it.

        Rules:
        1. Select only the most relevant URL.
        2. Call scrape_url at most once.
        3. After getting the scraped content, stop using tools.
        4. Return the useful extracted information.
        """
    )

# Writer Chain

writer_prompt=ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Wrirte a detailed research report on the topic below
    Topic: {topic}
    
    Research Gathered:
    {research}
    
    Structure the report as:
    - Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional
    
    
    
    
    """)

])

writer_chain=writer_prompt|llm|StrOutputParser()

# Critic_Chain

critic_prompt=ChatPromptTemplate.from_messages([
    ("system", "You are sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..""")
])

critic_chain=critic_prompt|llm|StrOutputParser()


