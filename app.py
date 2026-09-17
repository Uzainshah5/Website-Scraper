import os

import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI

from scraper import fetch_website_contents

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

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

EXAMPLE_URLS = [
    ["https://www.wikipedia.org"],
    ["https://news.ycombinator.com"],
    ["https://www.github.com"],
    ["https://openai.com"],
]

CSS = """
/* ── Global ── */
body, .gradio-container {
    background: #0d0f1a !important;
    font-family: 'Inter', sans-serif !important;
}

/* ── Header card ── */
#header-box {
    background: linear-gradient(135deg, #1a1d2e 0%, #141726 100%);
    border: 1px solid #2a2d45;
    border-radius: 18px;
    padding: 36px 40px 28px;
    margin-bottom: 4px;
    text-align: center;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
}
#header-box h1 {
    font-size: 2.4rem;
    font-weight: 800;
    background: linear-gradient(90deg, #818cf8, #a78bfa, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 10px;
    letter-spacing: -0.5px;
}
#header-box p {
    color: #94a3b8;
    font-size: 1.05rem;
    margin: 0;
}

/* ── Main panel ── */
#main-panel {
    background: linear-gradient(160deg, #131525 0%, #0f1120 100%);
    border: 1px solid #1e2235;
    border-radius: 18px;
    padding: 32px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.35);
}

/* ── URL input ── */
#url-input textarea, #url-input input {
    background: #1a1d2e !important;
    border: 1.5px solid #2a2d45 !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
    font-size: 1rem !important;
    padding: 14px 18px !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
#url-input textarea:focus, #url-input input:focus {
    border-color: #818cf8 !important;
    box-shadow: 0 0 0 3px rgba(129,140,248,0.15) !important;
    outline: none !important;
}
#url-input label {
    color: #94a3b8 !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
}

/* ── Summarize button ── */
#summarize-btn {
    background: linear-gradient(135deg, #818cf8 0%, #a78bfa 50%, #f472b6 100%) !important;
    border: none !important;
    border-radius: 12px !important;
    color: #fff !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    padding: 14px 0 !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: opacity 0.2s ease, transform 0.15s ease, box-shadow 0.2s ease !important;
    box-shadow: 0 4px 20px rgba(129,140,248,0.35) !important;
    letter-spacing: 0.02em !important;
}
#summarize-btn:hover {
    opacity: 0.9 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(129,140,248,0.45) !important;
}
#summarize-btn:active {
    transform: translateY(0) !important;
}

/* ── Secondary buttons ── */
#clear-btn, #copy-btn {
    background: transparent !important;
    border: 1.5px solid #2a2d45 !important;
    border-radius: 12px !important;
    color: #94a3b8 !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    padding: 12px 0 !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: border-color 0.2s ease, color 0.2s ease, background 0.2s ease !important;
}
#clear-btn:hover, #copy-btn:hover {
    border-color: #818cf8 !important;
    color: #818cf8 !important;
    background: rgba(129,140,248,0.06) !important;
}

/* ── Output markdown ── */
#output-box {
    background: #1a1d2e !important;
    border: 1.5px solid #2a2d45 !important;
    border-radius: 14px !important;
    color: #e2e8f0 !important;
    min-height: 260px !important;
    padding: 20px 24px !important;
    line-height: 1.75 !important;
    font-size: 0.97rem !important;
}
#output-box label {
    color: #94a3b8 !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
}

/* ── Examples ── */
.examples-holder table {
    background: #1a1d2e !important;
    border-radius: 12px !important;
    border: 1px solid #2a2d45 !important;
    overflow: hidden !important;
}
.examples-holder td, .examples-holder th {
    color: #94a3b8 !important;
    border-color: #2a2d45 !important;
}
.examples-holder tr:hover td {
    background: rgba(129,140,248,0.06) !important;
    color: #c7d2fe !important;
    cursor: pointer !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0d0f1a; }
::-webkit-scrollbar-thumb { background: #2a2d45; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #818cf8; }
"""


def summarize_website(url: str):
    """Scrape a website and return an AI-powered summary."""
    url = url.strip()

    if not url:
        return "Please enter a URL before clicking **Summarize**.", gr.update(visible=False)

    # Auto-prepend https:// if missing
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    if not api_key:
        return (
            " **GEMINI_API_KEY** is not set. "
            "Create a `.env` file and add your key.",
            gr.update(visible=False),
        )

    try:
        website_content = fetch_website_contents(url)
    except Exception as e:
        return f" **Failed to fetch the website.**\n\n```\n{e}\n```", gr.update(visible=False)

    if not website_content:
        return "No readable content was found on this website.", gr.update(visible=False)

    user_prompt = f"""Here is the content of a website:

{website_content}

Please provide a concise summary of this website."""

    try:
        response = client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
        )
        summary = response.choices[0].message.content
    except Exception as e:
        return f" **AI summarization failed.**\n\n```\n{e}\n```", gr.update(visible=False)

    return summary, gr.update(visible=True)


def clear_all():
    return "", "Your website summary will appear here…", gr.update(visible=False)


# ── Build UI ──────────────────────────────────────────────────────────────────
with gr.Blocks(title="AI Website Summarizer") as demo:

    # ── Header ────────────────────────────────────────────────────────────────
    gr.HTML("""
    <div id="header-box">
        <h1>🌐 AI Website Summarizer</h1>
        <p>Paste any URL and get an instant AI-powered summary powered by
           <strong>Gemini 2.5 Flash</strong></p>
    </div>
    """)

    # ── Main panel ────────────────────────────────────────────────────────────
    with gr.Column(elem_id="main-panel"):

        url_input = gr.Textbox(
            label="Website URL",
            placeholder="https://example.com  (press Enter or click Summarize)",
            lines=1,
            elem_id="url-input",
        )

        with gr.Row():
            summarize_btn = gr.Button(
                "✨  Summarize", elem_id="summarize-btn", variant="primary", scale=3
            )
            clear_btn = gr.Button(
                "🗑  Clear", elem_id="clear-btn", variant="secondary", scale=1
            )

        output = gr.Markdown(
            label="Summary",
            value="Your website summary will appear here…",
            elem_id="output-box",
        )

        copy_btn = gr.Button(
            "📋  Copy Summary", elem_id="copy-btn", visible=False
        )

        gr.Examples(
            examples=EXAMPLE_URLS,
            inputs=url_input,
            label="✦ Quick Examples",
        )

    # ── Footer ────────────────────────────────────────────────────────────────
    gr.HTML("""
    <div style="text-align:center; margin-top:20px; color:#334155; font-size:0.82rem;">
        <strong style="color:#818cf8">Gradio</strong> &amp;
        <strong style="color:#a78bfa">Gemini 2.5 Flash</strong>
    </div>
    """)

    # ── Event wiring ──────────────────────────────────────────────────────────
    summarize_btn.click(
        fn=summarize_website,
        inputs=[url_input],
        outputs=[output, copy_btn],
        show_progress="full",
    )

    url_input.submit(
        fn=summarize_website,
        inputs=[url_input],
        outputs=[output, copy_btn],
        show_progress="full",
    )

    clear_btn.click(
        fn=clear_all,
        inputs=[],
        outputs=[url_input, output, copy_btn],
    )

    copy_btn.click(
        fn=None,
        js="() => { navigator.clipboard.writeText(document.querySelector('#output-box .prose').innerText || ''); }",
    )


if __name__ == "__main__":
    demo.launch(
        inbrowser=True,
        css=CSS,
        theme=gr.themes.Base(
            primary_hue="violet",
            neutral_hue="slate",
            font=[gr.themes.GoogleFont("Inter"), "sans-serif"],
        ),
    )
