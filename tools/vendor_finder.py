from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure LangChain to use OpenRouter
llm = ChatOpenAI()

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
      "website": "",
      "contact_form_url": "",
      "services": [],
      "support_notes": ""
    }}
    
    Combine them into a JSON array—no extra text before or after.
    
    Use web browsing to verify phone numbers and contact‑/quote‑form URLs.
    
    Prefer companies within 30 miles of downtown {city}; if you must include one farther away, note the distance in support_notes.
    
    Be concise—limit support_notes to one sentence.
    
    If you can't find at least {count} valid entries, say "FEWER THAN {count} RESULTS" instead of the JSON.
    """
    
    prompt = PromptTemplate.from_template(template)
    response = llm.invoke(prompt.format(city=city, count=count))
    
    # Extract the response content
    response_text = response.content
    
    try:
        # Try to parse the response as JSON
        vendors = json.loads(response_text)
        return vendors
    except json.JSONDecodeError:
        # If parsing fails, log the error and return an empty list
        print(f"Error parsing JSON response: {response_text}")
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
