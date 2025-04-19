from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

llm = ChatOpenAI()

def generate_form_submission(service_type: str, city: str, details: str, user_name: str, user_email: str) -> str:
    template = """
You're filling out an online quote request form for a {service_type} service in {city}.
Here's the customer info:

- Name: {user_name}
- Email: {user_email}

Service details:
{details}

Write a clear, professional version of what this person would submit to the form.
Avoid filler. Write in plain English. Keep it short.
"""
    prompt = PromptTemplate.from_template(template)
    return llm.invoke(prompt.format(
        service_type=service_type,
        city=city,
        details=details,
        user_name=user_name,
        user_email=user_email
    ))
