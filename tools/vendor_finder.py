from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure LangChain with web search capability
llm = ChatOpenAI(model="gpt-4o-mini")
tool = {"type": "web_search_preview"}
llm_with_tools = llm.bind_tools([tool])

def generate_plumber_vendors(city: str, count: int = 5) -> list:
    """Generate plumber vendor data using LangChain and OpenRouter"""
    template = """
    I'm in {city}.
    
    Find professional plumbers (minimum {count}, maximum 8) that serve this city.
    
    For each company return a single JSON object with exactly these keys (all strings except services, which is an array of short strings):
    
    {{
      "name": "",
      "phone": "",
      "address": "",
      "email": "",
      "website": "",
      "contact_form_url": "",
      "services": [],
      "support_notes": ""
    }}
    
    Combine them into a JSON array—no extra text before or after.
    
    USE THE WEB_SEARCH TOOL to find and verify information about plumbers in {city}. Specifically:
    1. Search for plumbing companies in {city}
    2. Verify each company's phone number, website, and contact form URL
    3. Confirm their service area includes {city}
    4. Find their physical address and services offered
    
    Prefer companies within 30 miles of downtown {city}; if you must include one farther away, note the distance in support_notes.
    
    Be concise—limit support_notes to one sentence.
    
    If you can't find at least {count} valid entries, say "FEWER THAN {count} RESULTS" instead of the JSON.
    """
    
    prompt = PromptTemplate.from_template(template)
    response = llm_with_tools.invoke(prompt.format(city=city, count=count))
    
    # Extract the response content
    # When using tools like web_search, the response structure might be different
    if hasattr(response, 'content'):
        response_text = response.content
    else:
        # Handle different response structures that might come from tool use
        print("Response format differs from expected. Attempting to extract content...")
        if hasattr(response, 'message') and hasattr(response.message, 'content'):
            response_text = response.message.content
        elif isinstance(response, dict) and 'content' in response:
            response_text = response['content']
        elif isinstance(response, str):
            response_text = response
        else:
            print(f"Unexpected response format: {type(response)}")
            print(f"Response: {response}")
            return []
    
    try:
        # If response_text is already a list or dict, return it directly
        if isinstance(response_text, (list, dict)):
            return response_text
        # Try to parse the response as JSON string
        vendors = json.loads(response_text)
        return vendors
    except json.JSONDecodeError:
        # Try to extract JSON array from the response text
        import re
        print(f"Error parsing JSON response, attempting to extract JSON array: {response_text}")
        try:
            # Find the first '[' and last ']' to extract the JSON array
            start = response_text.find('[')
            end = response_text.rfind(']')
            if start != -1 and end != -1 and end > start:
                json_str = response_text[start:end+1]
                vendors = json.loads(json_str)
                return vendors
            else:
                # Try to extract with regex as a fallback
                match = re.search(r'\[.*\]', response_text, re.DOTALL)
                if match:
                    vendors = json.loads(match.group(0))
                    return vendors
        except Exception as e:
            print(f"Failed to extract JSON array: {e}")
        # If all parsing fails, return an empty list
        print(f"Final failure parsing JSON response: {response_text}")
        return []

def save_vendors_to_json(vendors: list, filename: str = "data/plumber_vendors.json") -> None:
    """Save vendor data to a JSON file"""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        json.dump(vendors, f, indent=2)
    print(f"Saved {len(vendors)} vendors to {filename}")

def get_mock_vendors(service_type: str, city: str, regenerate: bool = False) -> list:
    """
    Get vendor data, either from file or by generating it.
    
    Args:
        service_type: Type of service (e.g., "plumbing")
        city: City to find vendors in
        regenerate: Whether to force regeneration of vendor data
        
    Returns:
        List of vendor data
    """
    # Determine filename based on service type
    if "plumb" in service_type.lower():
        filename = "data/plumber_vendors.json"
    else:
        # Default to existing vendors.json for other service types
        filename = "data/vendors.json"
        if os.path.exists(filename):
            with open(filename) as f:
                return json.load(f)
    
    # Generate new data if regenerate is True, file doesn't exist, or it's empty
    if regenerate or not os.path.exists(filename):
        print(f"Generating new vendor data for {service_type} in {city}...")
        vendors = generate_plumber_vendors(city)
        if vendors:
            save_vendors_to_json(vendors, filename)
        else:
            print("Failed to generate vendor data. Using empty list.")
            return []
    
    # Load data from file
    try:
        with open(filename) as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        print(f"Error reading {filename}. Using empty list.")
        return []

if __name__ == "__main__":
    # This allows the script to be run directly for testing
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate vendor data for a specific service type and city")
    parser.add_argument("--service", default="plumbing", help="Service type (e.g., plumbing)")
    parser.add_argument("--city", default="Seattle", help="City to find vendors in")
    parser.add_argument("--regenerate", action="store_true", help="Force regeneration of vendor data")
    parser.add_argument("--count", type=int, default=5, help="Minimum number of vendors to generate")
    
    args = parser.parse_args()
    
    vendors = get_mock_vendors(args.service, args.city, args.regenerate)
    print(f"Found {len(vendors)} vendors for {args.service} in {args.city}")
    
    # Print the first vendor as an example
    if vendors:
        print("\nExample vendor:")
        print(json.dumps(vendors[0], indent=2))
