# AI Website Summarizer

A lightweight Python tool that extracts readable content from a website and uses Google's Gemini 2.5 Flash model to generate a concise AI-powered summary.

## Overview

The project combines traditional web scraping with generative AI.

Given a website URL, the application:

1. Fetches the webpage using HTTP requests.
2. Parses the HTML with BeautifulSoup.
3. Removes unnecessary elements such as navigation, headers, footers, scripts, and styles.
4. Extracts the readable page content.
5. Sends the content to Gemini 2.5 Flash.
6. Returns a concise Markdown summary.

## Architecture

```text
Website URL
     │
     ▼
┌──────────────┐
│  Web Scraper │
│ Requests +   │
│ BeautifulSoup│
└──────┬───────┘
       │
       ▼
Extracted Content
       │
       ▼
┌──────────────┐
│  Gemini AI   │
│ 2.5 Flash    │
└──────┬───────┘
       │
       ▼
AI-Generated Summary
```

## Features

* Scrapes website content with Python
* Extracts readable text from HTML
* Removes common unnecessary HTML elements
* Uses Gemini 2.5 Flash for summarization
* Returns summaries in Markdown
* Uses environment variables for API credentials
* Includes basic request timeout and error handling

## Tech Stack

* **Python**
* **Requests** — HTTP requests
* **BeautifulSoup4** — HTML parsing and content extraction
* **Google Gemini 2.5 Flash** — AI summarization
* **OpenAI Python SDK** — Gemini's OpenAI-compatible API
* **python-dotenv** — environment variable management

## Project Structure

```text
Website-Scraper/
│
├── main.py              # Application entry point and AI summarization
├── scraper.py           # Website scraping and content extraction
├── requirements.txt     # Python dependencies
├── .env.example         # Example environment configuration
├── .gitignore           # Files excluded from Git
└── README.md            # Project documentation
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Uzainshah5/Website-Scraper.git
cd Website-Scraper
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your API key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

Never commit your `.env` file or expose your API key publicly.

### 5. Run the application

```bash
python main.py
```

Enter a website URL when prompted:

```text
AI Website Summarizer
------------------------------
Enter a website URL: https://example.com
```

The application will scrape the website and generate an AI-powered summary.

## Example

```text
Enter a website URL: https://example.com

Scraping website...

Summary
==============================
Example.com is a simple demonstration
website used for documentation and examples.
```

## Limitations

This project currently uses a simple HTTP-based scraping approach.

Some websites may not work correctly, particularly:

* JavaScript-heavy applications
* Websites that require browser rendering
* Websites protected by anti-bot systems
* Websites that block automated requests

For example, a website that builds its content dynamically with JavaScript may return little or no useful content because the scraper does not currently run a browser.

## Future Improvements

Potential improvements include:

* Add URL validation
* Improve content extraction
* Add a graphical/web interface
* Support JavaScript-rendered websites with Playwright or Selenium
* Add configurable summary lengths
* Add support for multiple AI providers
* Add automated tests
* Add deployment support

## What I Learned

This project helped me practice:

* Web scraping and HTML parsing
* Working with HTTP requests
* Environment variable management
* Integrating an AI API
* Prompt design for summarization
* Separating application logic into modules
* Handling errors from external services

## License

This project is licensed under the MIT License.
