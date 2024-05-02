import re
import aiohttp
from bs4 import BeautifulSoup
from langchain.docstore.document import Document
from typing import List, Any
import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from config import SCRAPE_TIMEOUT

async def fetch(url, session):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Ejecutar en segundo plano
    options.add_argument("--disable-gpu") 
    
    # Inicializa el webdriver de Chrome
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) 
    try:
        print(f"Realizando solicitud HTTP a {url}")
        driver.get(url)

        # Espera a que el contenido se cargue
        tool_list_div = driver.find_element(By.ID, "tool-list")
        cards = tool_list_div.find_elements(By.CLASS_NAME, "card")

        html = driver.page_source
        print(f"Solicitud HTTP a {url} completada")
        return Document(page_content=html, metadata={"source": url})
    except Exception as e:
        print(f"Error al realizar la solicitud HTTP a {url}: {e}")
        return None
    finally:
        driver.quit()

async def scrape_links_to_documents(links: List[str]) -> List[Any]:
    if not links:
        raise Exception("No hay enlaces para raspar.")
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(url, session) for url in links]
        html_docs = await asyncio.gather(*tasks)

    return [process_document(doc) for doc in html_docs if doc and doc.page_content]

def process_document(doc):
    print(f"Analizando el contenido HTML de {doc.metadata['source']}")
    soup = BeautifulSoup(doc.page_content, "html.parser")
        
    # Extraer nombres de IA
    tool_names = []
    tool_elements = soup.find_all("div", class_="tool-list-title")  # Ajustar el selector según el HTML
    for element in tool_elements:
        tool_name = element.find("h2").text.strip()  # Ajustar el selector según el HTML
        tool_names.append(tool_name)

    # Extraer información de precios
    subscription = []
    suscription_elements = soup.find_all("span", class_="pricing-tag")  # Ajustar el selector según el HTML
    for element in suscription_elements:
        suscription = element.text.strip()  # Ajustar el selector según el HTML
        subscription.append(suscription)

    # Actualizar metadatos con nombres y precios
    metadata = update_metadata(soup, doc.metadata)
    metadata["tool_names"] = tool_names
    metadata["subscription"] = subscription
    
    clean_text = clean_html_text(soup)
    print(f"Metadatos: {metadata}")
    print(f"Extracción de información de {doc.metadata['source']} completada")
    return Document(page_content=clean_text, metadata=metadata)

def clean_html_text(soup):
    text = soup.get_text(separator="\n", strip=True)
    return re.sub(r"\n{3,}|\s{2,}", "\n", text)

def update_metadata(soup, metadata):
    title = soup.find("title").get_text() if soup.find("title") else None
    description = soup.find("meta", attrs={"name": "description"}).get("content", "No description found.") if soup.find("meta", attrs={"name": "description"}) else None
    language = soup.find("html").get("lang", "No language found.") if soup.find("html") else None
    metadata.update({"title": title, "description": description, "language": language})
    return metadata

