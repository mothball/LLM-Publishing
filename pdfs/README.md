# PDFs

Drop original monograph PDFs in this directory. Filename convention matches the
corresponding HTML page slug, e.g. `01-performant-vectorized-python.pdf`.

After adding a PDF:

1. Open `content.py`
2. Find the monograph entry by `num`
3. Set `"pdf_available": True`
4. Run `python3 run_build.py` to regenerate the HTML
5. Commit and push

The HTML's "Download PDF" link will then resolve to the file.
