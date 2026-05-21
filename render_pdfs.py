"""Render each monograph HTML to a PDF using headless Chromium.

The pages have to be served over HTTP for relative URLs (katex/, fonts, style.css)
to resolve cleanly, so we spin up a temp localhost server.
"""
import http.server
import socketserver
import threading
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))
from content import MONOGRAPHS

PDFS = ROOT / "pdfs"
PDFS.mkdir(exist_ok=True)

# ------- temp HTTP server -------
PORT = 8778
os_chdir = __import__("os").chdir
os_chdir(str(ROOT))
socketserver.TCPServer.allow_reuse_address = True
httpd = socketserver.TCPServer(("127.0.0.1", PORT), http.server.SimpleHTTPRequestHandler)
httpd.timeout = 0.1
t = threading.Thread(target=httpd.serve_forever, daemon=True)
t.start()

# ------- render -------
PRINT_CSS = """
@page { size: Letter; margin: 0.85in 0.7in; }
@media print {
  .masthead, .colophon { display: none !important; }
  .reconstruction-notice { page-break-after: avoid; }
  .mono-header { page-break-after: avoid; }
  h2, h3 { page-break-after: avoid; }
  pre, table, blockquote { page-break-inside: avoid; }
  .toc { page-break-inside: avoid; }
  body {
    background: white !important;
    background-image: none !important;
  }
  .page { padding: 0 !important; max-width: 100% !important; }
}
"""

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context()
    page = ctx.new_page()

    for m in MONOGRAPHS:
        url = f"http://127.0.0.1:{PORT}/monographs/{m['slug']}.html"
        out = PDFS / f"{m['slug']}.pdf"

        page.goto(url, wait_until="networkidle")
        # Wait for KaTeX render
        page.wait_for_function(
            "document.querySelectorAll('.katex').length > 0 || "
            "document.querySelectorAll('.prose').length > 0",
            timeout=10000
        )
        # Inject print CSS
        page.add_style_tag(content=PRINT_CSS)
        # Brief settle for fonts
        page.wait_for_timeout(800)

        page.pdf(
            path=str(out),
            format="Letter",
            print_background=True,
            margin={"top": "0.85in", "bottom": "0.85in", "left": "0.7in", "right": "0.7in"},
            prefer_css_page_size=True,
        )
        size_kb = out.stat().st_size // 1024
        print(f"  {out.name}  ({size_kb} KB)")

    browser.close()

httpd.shutdown()
print(f"\nDone. {len(MONOGRAPHS)} PDFs in {PDFS.relative_to(ROOT)}/")
