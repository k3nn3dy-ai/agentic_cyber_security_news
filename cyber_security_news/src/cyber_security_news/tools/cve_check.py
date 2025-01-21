from colorama import init, Fore, Style
import requests
from datetime import datetime, timedelta
import json

"""
This script fetches recent CVE (Common Vulnerabilities and Exposures) data from the 
National Vulnerability Database (NVD) API. It retrieves vulnerabilities published 
in the last 7 days and outputs the results in JSON format.

The script:
1. Calculates a date range (last 7 days)
2. Makes an API request to the NVD database to get the vulnerabilities with known exploits over the last 7 days.
3. Prints either the vulnerability data or an error message
"""

high_base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0?cvssV3Severity=HIGH"
critical_base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0?cvssV3Severity=CRITICAL"
known_exploits_base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0?hasKev"

# Initialize colorama
init()

# Calculate dates
end_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000")
start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%S.000")

params = {
    "pubStartDate": start_date,
    "pubEndDate": end_date,
}

# Headers for the request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept": "application/json"
}

# Make the request
high_response = requests.get(high_base_url, params=params, headers=headers)
critical_response = requests.get(critical_base_url, params=params, headers=headers)
known_exploits_response = requests.get(known_exploits_base_url, params=params, headers=headers)

# Process the high response
if high_response.status_code == 200:
    data = high_response.json()
    print(f"{Fore.YELLOW}Found {Fore.RED}{len(data['vulnerabilities'])}{Fore.YELLOW} HIGH vulnerabilities{Style.RESET_ALL}")

    # Filter excluding "Awaiting Analysis"
    high_filtered_vulnerabilities = {
        "vulnerabilities": [
            vuln for vuln in data["vulnerabilities"]
            if (vuln.get("cve", {}).get("metrics", {}).get("cvssMetricV31", [{}])[0].get("cvssData", {}).get("baseScore", 0) >= 7.0
                and vuln.get("cve", {}).get("vulnStatus") != "Awaiting Analysis")
        ]
    }
    
    # Generate filename with current timestamp
    timestamp = datetime.now().strftime("%Y%m%d")
    filename = f"high_cve_results_{timestamp}.json"
    
    # Save filtered results to JSON file
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(high_filtered_vulnerabilities, indent=4, fp=f)
    
    print(f"{Fore.GREEN}Results saved to: {Fore.CYAN}{filename}{Style.RESET_ALL}")

if critical_response.status_code == 200:
    data = critical_response.json()
    print(f"{Fore.YELLOW}Found {Fore.RED}{len(data['vulnerabilities'])}{Fore.YELLOW} CRITICAL vulnerabilities{Style.RESET_ALL}")

    critical_filtered_vulnerabilities = {
        "vulnerabilities": [
            vuln for vuln in data["vulnerabilities"]
            if vuln.get("cve", {}).get("vulnStatus") != "Awaiting Analysis"
        ]
    }

    timestamp = datetime.now().strftime("%Y%m%d")
    filename = f"critical_cve_results_{timestamp}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(critical_filtered_vulnerabilities, indent=4, fp=f)

    print(f"{Fore.GREEN}Results saved to: {Fore.CYAN}{filename}{Style.RESET_ALL}")

if known_exploits_response.status_code == 200:
    data = known_exploits_response.json()
    print(f"{Fore.YELLOW}Found {Fore.RED}{len(data['vulnerabilities'])}{Fore.YELLOW} known exploits{Style.RESET_ALL}")
 

    timestamp = datetime.now().strftime("%Y%m%d")
    filename = f"known_exploits_cve_results_{timestamp}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, indent=4, fp=f)

    print(f"{Fore.GREEN}Results saved to: {Fore.CYAN}{filename}{Style.RESET_ALL}")  

else:
    print(f"{Fore.RED}API Request Failed: HTTP {high_response.status_code}{Style.RESET_ALL}")
    print(f"{Fore.RED}{high_response.text}{Style.RESET_ALL}")
