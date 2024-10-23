# SubBruter
SubBrute - Fast and Accurate Domain Enumeration Using DNS Queries
SubBrute is a Python script designed for high-speed and precise domain enumeration. By utilizing direct DNS queries without relying on HTTP requests, SubBrute can efficiently determine the existence of domains. This method significantly accelerates the brute-force process and eliminates false positives, providing reliable results in less time.

# Features
High Speed: Direct DNS queries make the enumeration process faster than traditional methods.
Accuracy: Eliminates false positives by avoiding unreliable HTTP responses.
Lightweight: No need for heavy dependencies; runs smoothly with minimal resources.
Easy to Use: Simple command-line interface for quick setup and execution.
How It Works
SubBrute sends DNS queries to check the existence of subdomains. Since DNS servers handle these queries directly, the response times are quicker compared to HTTP requests. This approach not only speeds up the process but also reduces network overhead.

# Usage:
python subbrute.py -d example.com -w wordlist.txt
-d or --domain: The target domain to enumerate.
-w or --wordlist: Path to the wordlist file containing potential subdomains.

# Requirements:
Python 3.x
DNS Python library (install via pip install dnspython)
Installation

# Clone the repository:
git clone https://github.com/yourusername/SubBrute.git

# Navigate to the directory:
cd SubBrute

# Install dependencies:
pip install -r requirements.txt
Contributing
Contributions are welcome! Please submit a pull request or open an issue to discuss improvements or features.

# License
This project is licensed under the MIT License.

