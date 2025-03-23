import requests
import time

BASE_URL = "http://35.200.185.69:8000/v1/autocomplete?query="
RATE_LIMIT_DELAY = 1.2  
found_names = set()  
request_count = 0 

def fetch_names(query, page=1):
    global request_count
    try:
        request_count += 1  
        url = f"{BASE_URL}{query}&page={page}"
        response = requests.get(url)
        response_data = response.json()

        print(f"Full API response for '{query}', Page {page}:", response_data)

        if "names" in response_data and isinstance(response_data["names"], list):
            found_names.update(response_data["names"])
        
        elif "error" in response_data:
            print(f"API error for '{query}', Page {page}: {response_data['error']}")
            return
        
        else:
            print(f"Unexpected response format for '{query}', Page {page}: {response_data}")
            return

        if "nextPage" in response_data and response_data["nextPage"]:
            time.sleep(RATE_LIMIT_DELAY) 
            fetch_names(query, response_data["nextPage"])
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching '{query}', Page {page}: {e}")

def discover_names(prefix="", depth=3):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    
    for letter in alphabet:
        new_query = prefix + letter
        fetch_names(new_query)  

        if depth > 1:
            time.sleep(RATE_LIMIT_DELAY)  
            discover_names(new_query, depth - 1) 

def main():
    print("Starting API exploration...")
    discover_names("", 2)  
    print(f"Total API requests made: {request_count}")
    print(f"Extracted {len(found_names)} unique names:", list(found_names))

if __name__ == "__main__":
    main()
