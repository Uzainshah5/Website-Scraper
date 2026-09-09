# AI Website Summarizer

A simple Python application that scrapes a website and uses Google's Gemini AI to generate a concise summary of its content.

## How It Works

The application follows a simple pipeline:

Website URL
     ↓
Web Scraper
     ↓
Extract readable content
     ↓
Gemini AI
     ↓
Generate summary

## Features

- Scrapes website content using Python
- Removes common unnecessary HTML elements
- Uses Gemini 2.5 Flash for summarization
- Generates summaries in Markdown
- Handles invalid URLs and request errors
- Keeps API credentials in environment variables

## Tech Stack

- Python
- Requests
- BeautifulSoup
- Google Gemini
- OpenAI-compatible API
- python-dotenv

## Project Structure

```text
Website-Scraper/
│
├── scraper.py
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
└── .env.example

Installation

Clone the repository:

git clone https://github.com/Uzainshah5/Website-Scraper.git

Move into the project:

cd Website-Scraper

Create a virtual environment:

python -m venv .venv

Activate it.

Windows
.venv\Scripts\activate
macOS / Linux
source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt
API Key Setup

Create a .env file in the project root:

GEMINI_API_KEY=your_api_key_here

Never commit your .env file to GitHub.

Usage

Run:

python main.py

Enter a website URL when prompted:

AI Website Summarizer
------------------------------
Enter a website URL: https://example.com

The application will scrape the website and generate an AI-powered summary.

Limitations

This project uses a simple HTTP-based scraper.

Websites that rely heavily on JavaScript to render their content may not work correctly because the scraper does not currently run a browser.

Websites protected by anti-bot systems may also reject the request.

A future version could use Selenium or Playwright to support JavaScript-rendered websites.

Future Improvements
Add a web interface
Support JavaScript-rendered websites
Add Selenium or Playwright support
Improve content extraction
Add URL validation
Add summary length options
Add support for multiple AI providers