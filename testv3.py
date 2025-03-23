import requests
import time
import json
from collections import deque

class AutocompleteExtractor:
    def __init__(self, base_url='http://35.200.185.69:8000'):
        self.base_url = base_url
        self.endpoint = '/v3/autocomplete'
        self.param_name = 'query'
        self.discovered_names = set()
        self.request_count = 0
        self.start_time = time.time()
        self.rate_limit_delay = 0.75  # Initial delay between requests (seconds)
        self.retry_delay = 1.0  # Initial retry delay for rate limiting (seconds)
        self.max_retries = 5  # Maximum number of retries for a request
    
    def delay(self, seconds):
        time.sleep(seconds)
    
    def make_request(self, prefix):
        url = f"{self.base_url}{self.endpoint}"
        params = {self.param_name: prefix}
        self.request_count += 1
        
        for attempt in range(self.max_retries):
            try:
                self.delay(self.rate_limit_delay)
                response = requests.get(url, params=params)
                
                if response.status_code == 429:
                    print(f"Rate limited. Retrying in {self.retry_delay} seconds...")
                    self.delay(self.retry_delay)
                    self.retry_delay *= 2
                    self.rate_limit_delay *= 1.5
                    continue
                
                self.retry_delay = 1.0
                return response.json()
            except requests.RequestException as e:
                print(f"Request error: {e}. Retrying in {self.retry_delay} seconds...")
                self.delay(self.retry_delay)
                self.retry_delay *= 2
        
        raise Exception(f"Failed to get response after {self.max_retries} attempts")
    
    def test_endpoint(self):
        try:
            print(f"Testing endpoint: {self.base_url}{self.endpoint}?{self.param_name}=a")
            response = self.make_request('a')
            print("Endpoint test successful.")
            self.analyze_response_structure(response)
            return True
        except Exception as e:
            print(f"Endpoint test failed: {e}")
            return False
    
    def analyze_response_structure(self, data):
        print("\nAnalyzing response structure:")
        if isinstance(data, list):
            print(f"- Response is a list with {len(data)} items")
        elif isinstance(data, dict):
            print(f"- Response is a dictionary with keys: {', '.join(data.keys())}")
    
    def extract_results(self, response_data):
        if isinstance(response_data, list):
            return [item if isinstance(item, str) else item.get('name') for item in response_data]
        elif isinstance(response_data, dict):
            for key in ['results', 'suggestions', 'completions', 'data', 'items']:
                if key in response_data and isinstance(response_data[key], list):
                    return [item if isinstance(item, str) else item.get('name') for item in response_data[key]]
            return list(response_data.values())
        return []
    
    def extract_all_names(self):
        print("\n===== EXTRACTING NAMES =====")
        queue = deque(chr(i) for i in range(97, 123))  # a-z
        visited = set(queue)
        
        while queue:
            prefix = queue.popleft()
            try:
                response_data = self.make_request(prefix)
                results = self.extract_results(response_data)
                for name in results:
                    if name not in self.discovered_names:
                        self.discovered_names.add(name)
                        if name.startswith(prefix) and len(name) > len(prefix):
                            for i in range(97, 123):
                                new_prefix = name[:len(prefix) + 1]
                                if new_prefix not in visited:
                                    visited.add(new_prefix)
                                    queue.append(new_prefix)
            except Exception as e:
                print(f"Error processing prefix '{prefix}': {e}")
    
    def extract_with_combination_strategy(self):
        print("\n===== EXTRACTING NAMES WITH OPTIMIZED STRATEGY =====")
        common_prefixes = [chr(i) for i in range(97, 123)] + ['th', 'he', 'an', 're', 'er', 'in', 'on', 'at', 'nd']
        for prefix in common_prefixes:
            try:
                response_data = self.make_request(prefix)
                results = self.extract_results(response_data)
                self.discovered_names.update(results)
            except Exception as e:
                print(f"Error processing prefix '{prefix}': {e}")
    
    def save_results(self, filename="extracted_names_v3.json"):
        with open(filename, "w") as f:
            json.dump(list(self.discovered_names), f, indent=2)
        print(f"Saved {len(self.discovered_names)} names to {filename}")
    
    def print_summary(self):
        elapsed = time.time() - self.start_time
        print("\n===== EXTRACTION SUMMARY =====")
        print(f"Total names found: {len(self.discovered_names)}")
        print(f"Total requests made: {self.request_count}")
        print(f"Time elapsed: {elapsed:.2f} seconds")
        print(f"Request rate: {self.request_count / elapsed:.2f} requests/second")
    
# Main function to run the extraction
def main():
    extractor = AutocompleteExtractor()
    if extractor.test_endpoint():
        extractor.extract_all_names()
        extractor.save_results()
        extractor.print_summary()A
    else:
        print("Failed to access the autocomplete endpoint.")

if __name__ == "__main__":
    main()
