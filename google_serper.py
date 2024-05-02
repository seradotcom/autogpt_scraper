from langchain_community.utilities import GoogleSerperAPIWrapper
from config import NUM_GEN_LINKS
from dotenv import load_dotenv
import os
import pprint

# Cargar variables de entorno
load_dotenv(override=True)
serper_api_key = os.getenv("SERPER_API_KEY")


def get_ai_info(tool_name: str, num_snippets=None) -> tuple[str, list, str, str]:
    """Gets the most relevant URL, snippets, description, and image URL for the AI tool."""
    try:
        search = GoogleSerperAPIWrapper(k=NUM_GEN_LINKS, serper_api_key=serper_api_key)
        results = search.results(f"{tool_name} AI")

        # Extract information
        most_relevant_link = results['organic'][0]['link']
        snippets = [result['snippet'] for result in results['organic'][:num_snippets]]
        description = results.get('knowledgeGraph', {}).get('description', "")

        # Verificar si knowledgeGraph contiene la URL de la imagen
        url_img = results.get('knowledgeGraph', {}).get('imageUrl', "")
        if not url_img:
            # Buscar logo si no se encuentra en knowledgeGraph
            searchImg = GoogleSerperAPIWrapper(type="images")
            results = searchImg.results(f"{tool_name} AI logo png")
            url_img = results['images'][0]['imageUrl']

        return most_relevant_link, snippets, description, url_img
    except Exception as e:
        return "", [], "", ""


"""# Example usage (get 5 snippets)
most_relevant_url, snippets, ai_description, url_image = get_ai_info("Gemini", num_snippets=None)
print(f"Most Relevant URL: {most_relevant_url}")
print(f"Snippets:")
for snippet in snippets:
    print(f"- {snippet}")
print(f"AI Description: {ai_description}")
print(f"URL img: {url_image}")
"""
