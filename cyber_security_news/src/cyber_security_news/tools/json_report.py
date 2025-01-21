from crewai_tools import BaseTool
import json
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

class JSONReportTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="JSONReportTool",
            description="Analyzes CVE JSON data and generates summary reports, plots, and CSV exports.",
            func=self._run
        )

    def _run(self, file_path: str) -> str:
        """Main execution method that processes the JSON file and generates reports"""
        data = self.load_json(file_path)
        df = self.parse_vulnerabilities(data)
        
        # Generate all reports
        summary = self.create_summary(df)
        plot_path = self.plot_severity_distribution(df)
        csv_path = self.export_to_csv(df)
        
        return f"Analysis complete:\n{summary}\nPlot saved to: {plot_path}\nCSV exported to: {csv_path}"

    def load_json(self, file_path):
        try:
            if not file_path.endswith('.json'):
                file_path = file_path + '.json'
            
            with open(file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return f"Error: Could not find file '{file_path}'"
        except json.JSONDecodeError:
            return f"Error: '{file_path}' is not a valid JSON file"

    def parse_vulnerabilities(self, data):
        vulnerabilities = []
        for vuln in data['vulnerabilities']:
            cve = vuln['cve']
            severity = (
                cve.get('metrics', {}).get('cvssMetricV31', [{}])[0]
                .get('cvssData', {}).get('baseSeverity', 'N/A')
            )
            
            # Only include HIGH or CRITICAL vulnerabilities
            if severity in ['HIGH', 'CRITICAL']:
                vulnerabilities.append({
                    'CVE ID': cve.get('id', 'N/A'),
                    'Published Date': cve.get('published', 'N/A'),
                    'Severity': severity,
                    'Description': (
                        cve.get('descriptions', [{}])[0].get('value', 'No description available')
                    )
                })
        return pd.DataFrame(vulnerabilities)

    def create_summary(self, df):
        """Create and return summary statistics as a string"""
        summary = df['Severity'].value_counts().to_string()
        return f"\nSummary of CVEs:\n{summary}"

    def plot_severity_distribution(self, df):
        """Create severity distribution plot and return the file path"""
        severity_counts = df['Severity'].value_counts()
        severity_counts.plot(kind='bar')
        plt.title('Severity Distribution of CVEs')
        plt.xlabel('Severity')
        plt.ylabel('Count')
        
        timestamp = pd.Timestamp.now().strftime("%Y%m%d")
        plot_path = f'severity_distribution_{timestamp}.png'
        plt.savefig(plot_path)
        plt.close()
        return plot_path

    def export_to_csv(self, df):
        """Export to CSV and return the file path"""
        timestamp = pd.Timestamp.now().strftime("%Y%m%d")
        csv_path = f'cve_summary_{timestamp}.csv'
        df.to_csv(csv_path, index=False)
        return csv_path