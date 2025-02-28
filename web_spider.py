import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import pandas as pd
import hashlib

def detect_technology(url):
    try:
        response = requests.get(url, timeout=5)
        server_header = response.headers.get('Server', 'Unknown').lower()
        return server_header
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def get_default_file_path(server_header):
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
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Default file list not found: {file_path}")
        return []

def extract_directories(urls):
    directories = set()
    for url in urls:
        parsed = urlparse(url)
        path_parts = parsed.path.strip('/').split('/')
        if path_parts:
            directories.add(f"{parsed.scheme}://{parsed.netloc}/{'/'.join(path_parts[:-1])}")
    return directories

def hash_value(value):
    return hashlib.sha256(value.encode()).hexdigest()

def crawl_site(url, max_depth=2):
    visited = set()
    to_visit = [url]
    found_urls = set()
    
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
    default_urls = {urljoin(base_url, df) for df in default_files}
    default_found = found_urls & default_urls
    non_default = found_urls - default_urls
    
    default_dirs = extract_directories(default_found)
    non_default_dirs = extract_directories(non_default)
    
    return default_found, non_default, default_dirs, non_default_dirs

def create_cross_matrix(default_set, non_default_set, label1, label2):
    all_items = sorted(default_set | non_default_set)
    matrix = []
    for item in all_items:
        matrix.append([hash_value(item), item in default_set, item in non_default_set])
    
    df = pd.DataFrame(matrix, columns=['Hashed Item', label1, label2])
    return df

def main():
    target_url = input("Enter target URL (e.g., http://example.com): ")
    technology = detect_technology(target_url)
    
    if not technology:
        print("Failed to detect server technology.")
        return
    
    print(f"Detected Technology: {technology}")
    
    default_file_path = get_default_file_path(technology)
    default_files = load_default_files(default_file_path)
    print(f"Loaded {len(default_files)} default entries from {default_file_path}")
    
    found_urls = crawl_site(target_url)
    default_found, non_default, default_dirs, non_default_dirs = compare_urls(found_urls, default_files, target_url)
    
    print("\n=== Default URLs Found ===")
    for url in default_found:
        print(url)
    
    print("\n=== Non-Default URLs Found ===")
    for url in non_default:
        print(url)
    
    print("\n=== Default Directories Found ===")
    for directory in default_dirs:
        print(directory)
    
    print("\n=== Non-Default Directories Found ===")
    for directory in non_default_dirs:
        print(directory)
    
    print("\n=== Cross Matrix Comparison ===")
    url_matrix = create_cross_matrix(default_found, non_default, "Default URL", "Non-Default URL")
    dir_matrix = create_cross_matrix(default_dirs, non_default_dirs, "Default Dir", "Non-Default Dir")
    
    print("\nURL Comparison Matrix:")
    print(url_matrix.to_string(index=False))
    
    print("\nDirectory Comparison Matrix:")
    print(dir_matrix.to_string(index=False))

if __name__ == "__main__":
    main()

