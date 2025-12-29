
import requests
import sys

def test_bet_summary():
    url = "http://localhost:5000/bet-summary"
    params = {
        "odds_1": -110,
        "odds_2": -110,
        "total_bet": 100
    }
    
    try:
        print(f"Testing {url} with params {params}...")
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            print("Success! Response:")
            print(data)
            
            # Basic validation
            if abs(data['percent_probability'] - 0.5) > 0.01:
                print("Error: Expected probability around 0.5")
                sys.exit(1)
            if abs(data['bet_amount'] - 50.0) > 0.01:
                print("Error: Expected bet amount around 50.0")
                sys.exit(1)
                
            print("Verification passed.")
        else:
            print(f"Failed with status code {response.status_code}")
            print(response.text)
            sys.exit(1)
            
    except requests.exceptions.ConnectionError:
        print("Could not connect to server. Is it running?")
        sys.exit(1)

if __name__ == "__main__":
    test_bet_summary()
