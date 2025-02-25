from openai import OpenAI
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
import os
import json
from IPython.display import Markdown, display

load_dotenv(override=True)
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI()

class Website:
    """A website with scraped data, contains title, content and relevant links."""
    def __init__(self, url):
        self.url = url
        response = requests.get(url)
        self.content = ""
        self.links = []
        soup = BeautifulSoup(response.content, "html.parser")

        self.title = soup.title.get_text() if soup.title else "No title Found"

        for element in soup.find_all(["script", "style", "img", "input"]):
            element.decompose()

        self.content = soup.get_text(separator=" ", strip=True)
        if soup.body:
            links = soup.body.find_all(True, attrs={"href": True})
            for link in links:
                self.links.append(link.get('href'))

    def get_content(self):
        return f"\nThe content of the webpage: {self.content}"

def relevant_link(web_links):
    link_system_prompt = "You are provided with a list of links found on a webpage. \
    You are able to decide which of the links would be most relevant to include in a brochure about the company, \
    such as links to an About page, or a Company page, or Careers/Jobs pages.\n"
    link_system_prompt += "You should respond in JSON as in this example:"
    link_system_prompt += """
    {
    "links": [
        {"type": "about page", "url": "https://full.url/goes/here/about"},
        {"type": "careers page", "url": "https://another.full.url/careers"}
        ]
    }
    """

    link_user_prompt = f"Here is the list of links on the website: {w1.url} - please decide which of these are relevant \
    web links for a brochure about the company, respond with the full https URL in JSON format. \
    Do not include Terms of Service, Privacy, email links.\nLinks (some might be relative links):\n"
    for link in web_links:
        link_user_prompt += f"{link}\n"

    message = [
        {"role": "system", "content": link_system_prompt},
        {"role": "user", "content": link_user_prompt}
    ]

    response = client.chat.completions.create(model="gpt-4o-mini", messages=message, response_format={"type": "json_object"})
    return response.choices[0].message.content

def get_brochure(lists):
    link_data = json.loads(lists)["links"]
    link_urls = [link["url"] for link in link_data]

    brochure_system_prompt = "You are an assistant that analyzes the contents of several relevant pages from a company website \
and creates a short brochure about the company for prospective customers, investors and recruits. Respond in markdown.\
Include details of company culture, customers and careers/jobs if you have the information."

    brochure_user_prompt = f"Here is the name of the company: {w1.title} each page and its content:\n\
The content of the landing page: {w1.content}\nThe content of other webpages:\n\n"


    for link in link_urls:
        try:
            page = requests.get(link, timeout=5)
            soup = BeautifulSoup(page.content, "html.parser")
            content = soup.get_text(separator=" ", strip=True)
            brochure_user_prompt += f"Page: {link}\nContent: {content}\n\n"
        except requests.RequestException as e:
            print(f"Failed to fetch {link}: {e}")

    brochure_message = [
        {"role": "system", "content": brochure_system_prompt},
        {"role": "user", "content": brochure_user_prompt}
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=brochure_message
    )

    return response.choices[0].message.content

w1 = Website(input("Enter the company's landing page link: "))
useful_links = relevant_link(w1.links)
brochure = get_brochure(useful_links)
display(Markdown(brochure))
