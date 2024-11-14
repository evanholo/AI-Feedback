import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Step 1: Scrape all component links from the main page
def get_component_links(main_url):
    response = requests.get(main_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract all component links from the main page
    component_links = [a.get('href') for a in soup.find_all('a', href=True)]
    filtered_links = [urljoin(main_url, link) for link in component_links if "package-summary" in link]
    return filtered_links

# Step 2: Scrape each package summary page for class links
def get_class_links(package_summary_url):
    response = requests.get(package_summary_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract class links from the package-summary page
    class_links = [a.get('href') for a in soup.find_all('a', href=True)]
    filtered_links = [urljoin(package_summary_url, link) for link in class_links]
    return filtered_links

# Step 3: Scrape method bodies from each class page
def get_methods_from_class(class_url):
    response = requests.get(class_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract method bodies from the class page (adjust based on the tag structure)
    methods = []
    method_bodies = soup.find_all('pre')  # Assuming method bodies are inside <pre> tags
    for method_body in method_bodies:
        methods.append(method_body.get_text())
    
    return methods

# Step 4: Putting it all together to scrape methods for all components
def main():
    main_url = "https://cse22x1.engineering.osu.edu/common/doc/index.html"
    
    # Get all component links from the main page
    component_links = get_component_links(main_url)
    
    all_methods = {}
    
    # Open a text file to write the output
    with open("output.txt", "w", encoding="utf-8") as file:
        # For each component package, get the class links and then the methods
        for component_link in component_links:
            class_links = get_class_links(component_link)
            
            # Scrape methods for each class
            for class_link in class_links:
                methods = get_methods_from_class(class_link)
                all_methods[class_link] = methods
                
                # Write results to the file
                file.write(f"Methods for {class_link}:\n")
                for method in methods:
                    file.write(method + "\n")
                file.write("\n")
    
    return all_methods

# Run the scraper
if __name__ == "__main__":
    all_methods = main()

