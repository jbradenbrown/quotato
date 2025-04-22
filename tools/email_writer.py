from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI()

def generate_quote_email(service_type: str, city: str, details: str, provider: dict) -> str:
    template = "Write a polite email asking for a quote for {service_type} in {city}. {details}. The email will be sent to {provider}"
    prompt = PromptTemplate.from_template(template)
    response = llm.invoke(prompt.format(service_type=service_type, city=city, details=details, provider=provider))
    return response.content
