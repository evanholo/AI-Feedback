from langchain_anthropic import ChatAnthropic

model = ChatAnthropic(model='claude-3-5-sonnet-20240620')

import requests
from bs4 import BeautifulSoup

def scrape_documentation(url):
    # Send request to the URL
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract all text from the page (this may need to be adjusted based on HTML structure)
    paragraphs = soup.find_all('p')  # Adjust tag if the text is not in <p>
    text = "\n".join([para.get_text() for para in paragraphs])

    return text

# Example: Scrape the OSU documentation page
doc_url = "https://cse22x1.engineering.osu.edu/common/doc/"
documentation_text = scrape_documentation(doc_url)

print(documentation_text[:500])  # Print first 500 chars to verify
