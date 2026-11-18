# Downloads the archive photos used by "Then & now" into img/ba/ so the site serves them itself.
import json, os, time, urllib.request, io
from PIL import Image
os.makedirs("img/ba", exist_ok=True)
src = json.load(open("ba_sources.json"))
UA = {"User-Agent": "Mozilla/5.0 (compatible; landmarks-photo-fetch/1.0)"}
ok = fail = 0
for e in src:
    out = f"img/ba/{e['id']}.jpg"
    if os.path.exists(out):
        ok += 1; continue
    for attempt in range(4):
        try:
            data = urllib.request.urlopen(urllib.request.Request(e["u"], headers=UA), timeout=60).read()
            im = Image.open(io.BytesIO(data)).convert("RGB")
            if im.width > 1200:
                im = im.resize((1200, round(im.height * 1200 / im.width)), Image.LANCZOS)
            im.save(out, "JPEG", quality=82, optimize=True, progressive=True)
            ok += 1; print("ok", e["id"], im.size); break
        except Exception as ex:
            print("retry", e["id"], ex); time.sleep(5 * (attempt + 1))
    else:
        fail += 1; print("FAILED", e["u"])
    time.sleep(1)
print("done", ok, "ok,", fail, "failed")
