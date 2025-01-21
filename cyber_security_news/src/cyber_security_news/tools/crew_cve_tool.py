from colorama import init, Fore, Style
from pydantic import BaseModel
from datetime import datetime, timedelta
import requests
import json
from langchain.tools import BaseTool, tool
from typing import Optional

"""
This script fetches recent CVE (Common Vulnerabilities and Exposures) data from the 
National Vulnerability Database (NVD) API, adapted for use with CrewAI.
"""

# Initialize colorama
init()

# Define input model
class CVERequest(BaseModel):
    severity: str  # Options: CRITICAL, HIGH, KNOWN_EXPLOITS
    days: int = 7  # Default is the last 7 days

# Define output model
class CVEResponse(BaseModel):
    severity: str 
    count: int
    vulnerabilities: list
    filename: str

# API Base URLs
BASE_URLS = {
    "CRITICAL": "https://services.nvd.nist.gov/rest/json/cves/2.0?cvssV3Severity=CRITICAL",
    "HIGH": "https://services.nvd.nist.gov/rest/json/cves/2.0?cvssV3Severity=HIGH",
    "KNOWN_EXPLOITS": "https://services.nvd.nist.gov/rest/json/cves/2.0?hasKev"
}

# Headers for the request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept": "application/json"
}

def fetch_cve_data(request: CVERequest) -> CVEResponse:
    """
    Fetch CVE data based on the provided request.
    """
    # Validate severity level
    if request.severity not in BASE_URLS:
        raise ValueError(f"Invalid severity level: {request.severity}")

    # Prepare dates
    end_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000")
    start_date = (datetime.now() - timedelta(days=request.days)).strftime("%Y-%m-%dT%H:%M:%S.000")

    params = {
        "pubStartDate": start_date,
        "pubEndDate": end_date
    }

    # Make API request
    response = requests.get(BASE_URLS[request.severity], params=params, headers=HEADERS)

    if response.status_code != 200:
        raise Exception(f"API Request Failed: HTTP {response.status_code}\n{response.text}")

    # Process response
    data = response.json()
    vulnerabilities = data.get("vulnerabilities", [])
    filtered_vulnerabilities = [
        vuln for vuln in vulnerabilities
        if vuln.get("cve", {}).get("vulnStatus") != "Awaiting Analysis"
    ] if vulnerabilities else []  # Handle empty vulnerabilities list

    # Save results to a file even if empty
    timestamp = datetime.now().strftime("%Y-%m-%d")
    filename = f"{request.severity.lower()}_cve_results_{timestamp}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump({"vulnerabilities": filtered_vulnerabilities}, f, indent=4)

    return CVEResponse(
        severity=request.severity,
        count=len(filtered_vulnerabilities),
        vulnerabilities=filtered_vulnerabilities,
        filename=filename
    )

@tool
def fetch_cve_data_tool(severity: str = "CRITICAL", days: int = 7) -> str:
    """Fetches recent CVE (Common Vulnerabilities and Exposures) data based on severity level and time range.
    
    Args:
        severity: The severity level to filter CVEs (CRITICAL, HIGH, or KNOWN_EXPLOITS)
        days: Number of days to look back for CVEs
        
    Returns:
        A string containing the CVE data results
    """
    print(f"Fetching CVEs with severity: {severity}, days: {days}")  # Debug logging
    
    # Validate input before creating request
    if severity not in BASE_URLS:
        return f"Error: Invalid severity level. Must be one of: {', '.join(BASE_URLS.keys())}"
    
    try:
        request = CVERequest(severity=severity, days=days)
        response = fetch_cve_data(request)
        result = (
            f"No {response.severity} vulnerabilities found in the last {days} days."
            if response.count == 0
            else f"Found {response.count} {response.severity} vulnerabilities in the last {days} days."
        )
        result += f" Results saved to: {response.filename}"
        print(f"Tool execution completed: {result}")  # Debug logging
        return result
    except Exception as e:
        error_msg = f"Error fetching CVE data: {str(e)}"
        print(error_msg)  # Debug logging
        return error_msg

# Example usage in CrewAI flow
if __name__ == "__main__":
    # Create a sample request
    request = CVERequest(severity="CRITICAL", days=7)
    try:
        result = fetch_cve_data(request)
        print(f"{Fore.YELLOW}Found {Fore.RED}{result.count}{Fore.YELLOW} {result.severity} vulnerabilities{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Results saved to: {Fore.CYAN}{result.filename}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")