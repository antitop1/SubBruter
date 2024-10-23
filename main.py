import dns.resolver
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import argparse
import logging
from typing import List, Tuple

def setup_logging():
    """Sets up logging."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('subbrute.log'),
            logging.StreamHandler()
        ]
    )

def check_subdomain(domain: str, subdomain: str, retries: int = 3, delay: float = 1.0) -> Tuple[str, bool]:
    """
    Checks if a subdomain exists by performing an A record DNS query.

    :param domain: The main domain.
    :param subdomain: The subdomain to check.
    :param retries: Number of retries on timeout.
    :param delay: Delay between retries.
    :return: Tuple (full subdomain, result of the check).
    """
    full_domain = f"{subdomain}.{domain}"
    for attempt in range(retries):
        try:
            # Perform an A record query (IP address)
            dns.resolver.resolve(full_domain, 'A', lifetime=5.0)
            return full_domain, True
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers):
            return full_domain, False
        except dns.exception.Timeout:
            if attempt < retries - 1:
                time.sleep(delay)
                continue
            else:
                return full_domain, False
        except Exception as e:
            logging.error(f"Error checking {full_domain}: {e}")
            return full_domain, False
    return full_domain, False

def process_subdomains(domain: str, subdomains: List[str], max_workers: int = 100) -> None:
    """
    Processes a list of subdomains for the specified domain.

    :param domain: The main domain.
    :param subdomains: List of subdomains to check.
    :param max_workers: Maximum number of threads.
    """
    existing_subdomains = []

    # Use ThreadPoolExecutor for multithreading
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(check_subdomain, domain, subdomain): subdomain for subdomain in subdomains}
        
        # Initialize progress bar
        for future in tqdm(as_completed(futures), total=len(futures), desc=f"Checking subdomains for {domain}", unit="subdomain"):
            try:
                subdomain, found = future.result()
                if found:
                    existing_subdomains.append(subdomain)
                    tqdm.write(f"Found: {subdomain}")
            except Exception as e:
                logging.error(f"Error processing subdomain: {e}")

    # Write found subdomains to file
    output_file = f"existing_subdomains_{domain}.txt"
    with open(output_file, "w") as file:
        for subdomain in existing_subdomains:
            file.write(subdomain + "\n")
    logging.info(f"Results saved to {output_file}")

def main():
    """Main function of the program."""
    setup_logging()

    parser = argparse.ArgumentParser(description="SubBrute - Fast and Accurate Subdomain Bruteforce Using DNS Queries")
    parser.add_argument("-d", "--domains", required=True, help="File containing main domains")
    parser.add_argument("-s", "--subdomains", required=True, help="File containing list of subdomains")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Maximum number of threads (default: 100)")
    args = parser.parse_args()

    # Read main domains from file
    try:
        with open(args.domains, "r") as file:
            domains = file.read().splitlines()
    except Exception as e:
        logging.error(f"Failed to read domains file {args.domains}: {e}")
        return
    
    # Read subdomains from file
    try:
        with open(args.subdomains, "r") as file:
            subdomains = file.read().splitlines()
    except Exception as e:
        logging.error(f"Failed to read subdomains file {args.subdomains}: {e}")
        return
    
    for domain in domains:
        logging.info(f"Processing domain: {domain}")
        process_subdomains(domain, subdomains, max_workers=args.threads)

if __name__ == "__main__":
    main()
