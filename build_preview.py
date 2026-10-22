"""Build standalone customer and merchant pages with styles and product art embedded."""
from base64 import b64encode
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
styles = (ROOT / "styles.css").read_text(encoding="utf-8")
app = (ROOT / "app.js").read_text(encoding="utf-8")
dataset = (ROOT / "data" / "store_complete.js").read_text(encoding="utf-8")
asset_files = list((ROOT / "assets" / "products").glob("*.svg")) + list((ROOT / "assets").glob("*.webp"))
def asset_key(path):
    return {"zid-beauty-hero": "beauty-hero", "skincare-contact-sheet": "skincare-sheet"}.get(path.stem, path.stem)

assets = {asset_key(path): f"data:{'image/svg+xml' if path.suffix == '.svg' else 'image/webp'};base64," + b64encode(path.read_bytes()).decode("ascii")
          for path in sorted(asset_files)}
for template_name, output_name in (("index.template.html", "index.html"), ("merchant.template.html", "merchant.html")):
    html = (ROOT / template_name).read_text(encoding="utf-8")
    html = html.replace('<link rel="stylesheet" href="styles.css">', f"<style>\n{styles}\n</style>")
    html = html.replace('<script src="data/store_complete.js"></script><script src="app.js"></script>', "<script>window.ZID_SOURCE_DATA=" + dataset.split("=",1)[1].strip().rstrip(";") + ";</script>\n<script>window.ZID_INLINE_ASSETS = " + json.dumps(assets, ensure_ascii=False) + ";</script>\n<script>\n" + app + "\n</script>")
    (ROOT / output_name).write_text(html, encoding="utf-8")
    print(f"Built standalone page: {ROOT / output_name} ({len(html):,} characters)")
