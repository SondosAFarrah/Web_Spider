import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import hashlib

def detect_technology(url):
    """
    Detects the web server technology by analyzing the 'Server' header in the HTTP response.
    :param url: Target URL to analyze.
    :return: Server technology string or None if detection fails.
    """
    try:
        response = requests.get(url, timeout=5)
        return response.headers.get('Server', 'Unknown').lower()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def get_default_file_path(server_header):
    """
    Determines the default file list based on the detected server technology.
    :param server_header: Detected web server technology.
    :return: Filename of the corresponding default file list.
    """
    if "nginx/1.19.0" in server_header:
        return "default_nginx_1_19_0.txt"
    elif "apache/2.4.62" in server_header:
        return "default_apache_2_4_62.txt"
    elif "apache" in server_header:
        return "default_apache.txt"
    elif "nginx" in server_header:
        return "default_nginx.txt"
    elif "iis" in server_header:
        return "default_iis.txt"
    else:
        return "default_other.txt"

def load_default_files(file_path):
    """
    Loads the default file list from the given file.
    :param file_path: Path to the default file list.
    :return: A list of default filenames.
    """
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Default file list not found: {file_path}")
        return []

def hash_value(value):
    """
    Computes the SHA-256 hash of a given value.
    :param value: String to hash.
    :return: Hashed value.
    """
    return hashlib.sha256(value.encode()).hexdigest()

def crawl_site(url, max_depth=3):
    """
    Crawls a website to extract internal URLs up to a specified depth.
    :param url: Base URL to start crawling.
    :param max_depth: Maximum depth for recursive crawling.
    :return: A set of discovered URLs.
    """
    visited, found_urls = set(), set()
    to_visit = [url]
    for _ in range(max_depth):
        new_links = []
        for link in to_visit:
            if link in visited:
                continue
            try:
                response = requests.get(link, timeout=5)
                visited.add(link)
                soup = BeautifulSoup(response.text, 'html.parser')
                for a_tag in soup.find_all('a', href=True):
                    absolute_url = urljoin(url, a_tag['href'])
                    if absolute_url.startswith(url):
                        found_urls.add(absolute_url)
                        new_links.append(absolute_url)
            except requests.exceptions.RequestException:
                continue
        to_visit = new_links
    return found_urls

def compare_urls(found_urls, default_files, base_url):
    """
    Compares discovered URLs with the default file list.
    :param found_urls: Set of URLs found during crawling.
    :param default_files: List of default files that should exist.
    :param base_url: The base website URL.
    :return: Sets of default files found and non-default files.
    """
    default_urls = {urljoin(base_url, df) for df in default_files}
    return found_urls & default_urls, found_urls - default_urls

def create_cross_matrix(default_set, non_default_set, label1, label2):
    """
    Generates a comparison matrix between default and non-default URLs.
    :param default_set: Set of URLs that match default files.
    :param non_default_set: Set of URLs that do not match default files.
    :param label1: Label for default URLs.
    :param label2: Label for non-default URLs.
    :return: Pandas DataFrame containing the comparison matrix.
    """
    all_items = sorted(default_set | non_default_set)
    matrix = [[hash_value(item), item in default_set, item in non_default_set] for item in all_items]
    return pd.DataFrame(matrix, columns=['Hashed Item', label1, label2])

def save_results(default_found, non_default, url_matrix):
    """
    Saves the results of the web scanning process to a file.
    :param default_found: Set of default URLs found.
    :param non_default: Set of non-default URLs found.
    :param url_matrix: Pandas DataFrame containing the comparison matrix.
    """
    with open("spidering_results.txt", "w") as file:
        file.write("=== Default URLs Found ===\n")
        file.writelines(f"{url}\n" for url in default_found)
        file.write("\n=== Non-Default URLs Found ===\n")
        file.writelines(f"{url}\n" for url in non_default)
        file.write("\n=== Cross Matrix Comparison ===\n")
        file.write(url_matrix.to_string(index=False))

def main():
    """
    Main execution function to run the web scanning process.
    """
    target_url = input("Enter target URL (e.g., http://example.com): ")
    technology = detect_technology(target_url)
    if not technology:
        print("Failed to detect server technology.")
        return
    default_files = load_default_files(get_default_file_path(technology))
    found_urls = crawl_site(target_url)
    default_found, non_default = compare_urls(found_urls, default_files, target_url)
    url_matrix = create_cross_matrix(default_found, non_default, "Default URL", "Non-Default URL")
    save_results(default_found, non_default, url_matrix)
    print("Results saved to spidering_results.txt")

if __name__ == "__main__":
    main()
