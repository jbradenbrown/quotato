#!/usr/bin/env python3
"""
Test script for vendor_finder.py

This script demonstrates how to use the vendor_finder.py module to generate
plumber vendor data for a specified city using web search functionality.

Usage:
    python test_vendor_finder.py [--city CITY] [--regenerate] [--count COUNT]

Examples:
    # Generate plumber vendors for Seattle (uses cached data if available)
    python test_vendor_finder.py
    
    # Generate plumber vendors for Portland, force regeneration
    python test_vendor_finder.py --city Portland --regenerate
    
    # Generate at least 6 plumber vendors for San Francisco
    python test_vendor_finder.py --city "San Francisco" --count 6 --regenerate
"""

import os
import json
# Import from the local module
from vendor_finder import get_mock_vendors, generate_plumber_vendors, save_vendors_to_json

def test_vendor_generation(city="Seattle", regenerate=False, count=5):
    """Test the vendor generation functionality"""
    print(f"\n{'='*50}")
    print(f"Testing vendor generation for {city}")
    print(f"{'='*50}")
    
    # Test direct generation
    if regenerate:
        print(f"\n1. Directly generating {count} plumber vendors for {city}...")
        vendors = generate_plumber_vendors(city, count)
        print(f"Generated {len(vendors)} vendors")
        
        if vendors:
            # Save to a test file
            test_file = f"data/test_plumbers_{city.lower().replace(' ', '_')}.json"
            save_vendors_to_json(vendors, test_file)
            print(f"Saved test data to {test_file}")
    
    # Test get_mock_vendors function
    print(f"\n2. Using get_mock_vendors for 'plumbing' in {city} (regenerate={regenerate})...")
    vendors = get_mock_vendors("plumbing", city, regenerate)
    print(f"Retrieved {len(vendors)} vendors")
    
    # Display the results
    if vendors:
        print("\nVendor data preview:")
        for i, vendor in enumerate(vendors[:3], 1):  # Show first 3 vendors
            print(f"\nVendor {i}: {vendor['name']}")
            print(f"  Phone: {vendor['phone']}")
            print(f"  Address: {vendor['address']}")
            print(f"  Website: {vendor['website']}")
            print(f"  Services: {', '.join(vendor['services'][:2])}...")
        
        if len(vendors) > 3:
            print(f"\n... and {len(vendors) - 3} more vendors")
    else:
        print("No vendors found or generation failed")
    
    return vendors

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test the vendor_finder module")
    parser.add_argument("--city", default="Seattle", help="City to find vendors in")
    parser.add_argument("--regenerate", action="store_true", help="Force regeneration of vendor data")
    parser.add_argument("--count", type=int, default=5, help="Minimum number of vendors to generate")
    
    args = parser.parse_args()
    
    # Make sure the .env file is loaded with required API keys
    missing_keys = []
    if not os.getenv("OPENROUTER_API_KEY"):
        missing_keys.append("OPENROUTER_API_KEY")
    if not os.getenv("OPENAI_API_KEY"):
        missing_keys.append("OPENAI_API_KEY")
    
    if missing_keys:
        print(f"\nWARNING: The following API keys were not found in environment variables: {', '.join(missing_keys)}")
        print("Make sure you have a .env file with the required API keys.")
        print("Example .env file content:")
        print("OPENROUTER_API_KEY=your_openrouter_api_key_here")
        print("OPENAI_API_KEY=your_openai_api_key_here  # Required for web search functionality")
    
    # Run the test
    test_vendor_generation(args.city, args.regenerate, args.count)
