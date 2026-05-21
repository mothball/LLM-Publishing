"""Run the build."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build import monograph_html, index_html, MONO_DIR, ROOT
from content import MONOGRAPHS

# Per-monograph pages
for m in MONOGRAPHS:
    out = MONO_DIR / f"{m['slug']}.html"
    out.write_text(monograph_html(m))
    print(f"wrote {out.relative_to(ROOT)}")

# Index
(ROOT / "index.html").write_text(index_html(MONOGRAPHS))
print(f"wrote index.html ({len(MONOGRAPHS)} monographs)")
