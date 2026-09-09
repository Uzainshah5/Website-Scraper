import os

from dotenv import load_dotenv
from openai import OpenAI

from scraper import fetch_website_contents


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY is not set. "
        "Create a .env file and add your Gemini API key."
    )


client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)


SYSTEM_PROMPT = """
You are an AI assistant that analyzes the contents of a website.

Provide a short, clear summary of the website.

Ignore navigation menus, cookie notices, advertisements,
and other irrelevant website elements.

If the website contains important news, announcements,
products, services, or key information, include those in
the summary.

Respond in Markdown.
"""


def summarize_website(url: str) -> str:
    """
    Scrape a website and generate an AI-powered summary.
    """

    website_content = fetch_website_contents(url)

    if not website_content:
        return "No readable content was found on this website."

    user_prompt = f"""
Here is the content of a website:

{website_content}

Please provide a concise summary of this website.
"""

    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
    )

    return response.choices[0].message.content


def main():
    print("AI Website Summarizer")
    print("-" * 30)

    url = input("Enter a website URL: ").strip()

    if not url:
        print("Please enter a valid URL.")
        return

    try:
        print("\nScraping website...")
        summary = summarize_website(url)

        print("\nSummary")
        print("=" * 30)
        print(summary)

    except Exception as error:
        print(f"\nError: {error}")


if __name__ == "__main__":
    main()