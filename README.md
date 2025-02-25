# Company Brochure Generator

An AI-powered tool that automatically generates a professional brochure for any company by analyzing its website. Simply provide the landing page URL, and the script does the rest.<br>
Requirements

To use this tool, you will need:

    An OpenAI API key

    A .env file in the project directory containing:

    OPENAI_API_KEY=your_openai_api_key_here

# How It Works

This script utilizes BeautifulSoup for web scraping and OpenAI’s GPT-4o-mini for intelligent content analysis.

    Scraping the Website:
        Extracts the textual content of the landing page.
        Collects all available links on the page.

    Filtering Relevant Links:
        The first API request to OpenAI processes the extracted links.
        It removes irrelevant links (e.g., Terms of Service, Privacy Policy) and retains those useful for a company brochure (e.g., About, Careers, Services).

    Generating the Brochure:
        The second API request compiles information from the landing page and relevant subpages.
        The AI crafts a well-structured, engaging company brochure suitable for potential customers, investors, and recruits.

This tool automates the process of gathering and structuring company information, making it an efficient solution for businesses and marketers.
