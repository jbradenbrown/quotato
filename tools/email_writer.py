from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

llm = ChatOpenAI()

def generate_quote_email(service_type: str, city: str, details: str) -> str:
    template = "Write a polite email asking for a quote for {service_type} in {city}. {details}"
    prompt = PromptTemplate.from_template(template)
    return llm.invoke(prompt.format(service_type=service_type, city=city, details=details))
