import os 
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

_client = Groq(api_key=os.environ["GROQ_API_KEY"])

def ask(prompt: str,model: str= "openai/gpt-oss-20b", max_tokens: int= 1024)-> str:
    """
    Send a single-turn prompt to the LLM and return its text reply.
    """
    response = _client.chat.completions.create(
        model=model,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content
def ask_with_tools(prompt: str, tools: list, model: str= "openai/gpt-oss-20b"):
    response = _client.chat.completions.create(
        model= model,
        max_tokens=1024,
        messages=[{"role":"user", "content":prompt}],
        tools = tools,
        tool_choice="auto",
        
    )
    return response.choices[0].message