import asyncio
from scraper import scrape_links_to_documents
from google_serper import get_ai_info
from openai_utils import generate_responses
from db_connection import insertar_datos
import os

async def main():
    # List of URLs
    page_urls = [f"https://findmyaitool.com/browse-tools?page={i}" for i in range(1, 2)]
    
    path = "ai_imgs"
    os.makedirs(path, exist_ok=True)

    # Extract info of each page.
    for url in page_urls:
        documents = await scrape_links_to_documents([url])

        for document in documents:
            # Get names and subscription of all AIs
            tool_names = document.metadata.get("tool_names")
            subscription = document.metadata.get("subscription")

            for tool_name, suscription in zip(tool_names, subscription):
                # Get snippets and description with Google Serper
                most_relevant_url, snippets, ai_description, url_img = get_ai_info(tool_name)

                # Combine snippets and description for context
                context = "\n".join(snippets) + "\n" + ai_description

                # Generate responses using the asynchronous function
                responses = await generate_responses(tool_name, context)

                # Check for explicit content
                is_explicit = responses[-1].strip() == "Explicit"  # Check the last response 

                if is_explicit:
                    print(f"Skipping '{tool_name}' due to explicit content.")
                    continue  # Skip to the next tool
                
                # Extract info of tuple's responses
                enterprise_category = responses[0].strip()
                content_type = responses[1].strip()
                ecosystem_layer = responses[2].strip()
                descripcion = responses[3].strip()
                licencia = responses[4].strip()

                # Insert into database
                insertar_datos(tool_name, descripcion, licencia, suscription, most_relevant_url, url_img, enterprise_category, ecosystem_layer, content_type, path)
                
                # Imprimir resultados
                """print(f"Descripción: {responses[3]}")
                print(f"Suscripción: {suscription}")
                print(f"Categoría principal: {responses[0]}")
                print(f"Tipo de contenido: {responses[1]}") 
                print(f"Capa del ecosistema de IA generativa: {responses[2]}") 
                print(f"Tipo de licencia: {responses[4]}") """
                
                """ # Crear un diccionario con la información
                data = {
                    "name": tool_name,
                    "description": responses[3],
                    "licence": responses[4],
                    "subscription": suscription,
                    "link": most_relevant_url,
                    "ecosystem_layer": responses[2]
                }

                # Guardar la información en un archivo JSON
                with open("ai_data.json", "a") as f:
                    json.dump(data, f)
                    f.write("\n")"""
            

if __name__ == "__main__":
    asyncio.run(main())