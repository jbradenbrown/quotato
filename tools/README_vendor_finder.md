# Vendor Finder Tool

This tool allows you to generate vendor data for different service types and locations using AI with web search capabilities. The current implementation focuses on plumbers but can be extended to other service types.

## Features

- Generate plumber vendor data for a specified city
- Uses web search to verify information (phone numbers, websites, contact forms)
- Cache vendor data to avoid repeated API calls
- Customizable number of vendors to generate

## Setup

1. Make sure you have the required dependencies installed:
   ```
   pip install langchain-community langchain-core openai python-dotenv
   ```

2. Create a `.env` file in the project root with your API keys:
   ```
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here  # Required for web search functionality
   ```
   
   You can copy the `.env.example` file and fill in your actual API keys.

## Usage

### Using in Your Code

```python
from tools.vendor_finder import get_mock_vendors

# Get plumber vendors for Seattle (uses cached data if available)
vendors = get_mock_vendors("plumbing", "Seattle")

# Force regeneration of vendor data
vendors = get_mock_vendors("plumbing", "Seattle", regenerate=True)

# Access vendor information
for vendor in vendors:
    print(f"Name: {vendor['name']}")
    print(f"Phone: {vendor['phone']}")
    print(f"Services: {vendor['services']}")
```

### Command Line Usage

The vendor_finder.py script can be run directly from the command line:

```bash
# Generate plumber vendors for Seattle (default)
python tools/vendor_finder.py

# Generate plumber vendors for a different city
python tools/vendor_finder.py --city "San Francisco"

# Force regeneration of vendor data
python tools/vendor_finder.py --regenerate

# Specify minimum number of vendors to generate
python tools/vendor_finder.py --count 6
```

### Testing

A test script is provided to help you test the vendor finder functionality:

```bash
# Run the test with default settings
python tools/test_vendor_finder.py

# Test with a different city
python tools/test_vendor_finder.py --city "Portland"

# Force regeneration of vendor data
python tools/test_vendor_finder.py --regenerate

# Specify minimum number of vendors to generate
python tools/test_vendor_finder.py --count 6
```

## How It Works

1. The tool uses OpenAI with web search capabilities to generate vendor data based on a prompt.
2. When generating data, the tool:
   - Searches the web for plumbing companies in the specified city
   - Verifies phone numbers, websites, and contact form URLs
   - Confirms service areas and collects other relevant information
   - Formats the data into a structured JSON format
3. The generated data is saved to a JSON file in the `data/` directory.
4. Subsequent requests use the cached data unless regeneration is forced.

## Files

- `vendor_finder.py`: Main module for generating vendor data
- `test_vendor_finder.py`: Test script to demonstrate usage
- `data/plumber_vendors.json`: Generated plumber vendor data

## Extending

To extend this tool to other service types:

1. Update the `get_mock_vendors` function to handle different service types
2. Create appropriate prompts for different service types
3. Add logic to save/load different JSON files based on service type
