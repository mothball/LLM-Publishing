"""Export vault_data.py -> assets/vault-data.js so vault.html can load it without a server."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from vault_data import NODES, EDGES

# Sanity check edge endpoints
ids = {n["id"] for n in NODES}
bad = [e for e in EDGES if e["source"] not in ids or e["target"] not in ids]
if bad:
    raise SystemExit(f"Broken edges: {bad}")

payload = {"nodes": NODES, "edges": EDGES}

out = Path(__file__).parent / "assets" / "vault-data.js"
out.write_text("// AUTO-GENERATED from vault_data.py. Do not edit by hand.\n"
               "const VAULT = " + json.dumps(payload, indent=2) + ";\n")
print(f"wrote {out.relative_to(Path(__file__).parent)} "
      f"({len(NODES)} nodes, {len(EDGES)} edges)")
