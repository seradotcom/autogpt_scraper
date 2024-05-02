from langchain_openai import OpenAI
from prompt_repo import get_prompts
from dotenv import load_dotenv
import asyncio
import os

# Cargar variables de entorno
load_dotenv(override=True)
openai_api_key = os.getenv("OPENAI_API_KEY")

async def generate_responses(tool_name, context):
  """Generates responses from OpenAI for the given tool and context."""
  llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
  prompts = get_prompts(tool_name, context)
  
  # Create a list of coroutines (calls to llm)
  coroutines = [llm.ainvoke(prompt_template.format(context=context)) 
                for _, prompt_template in prompts]  # Access the second element (template)

  # Use asyncio.gather to await the coroutines concurrently
  responses = await asyncio.gather(*coroutines)
  
  return responses