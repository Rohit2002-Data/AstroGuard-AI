"""Download files exposed by NASA's public OSDR API for study OSD-575."""
from pathlib import Path
import json
import re
import requests

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "raw"
API = "https://osdr.nasa.gov/osdr/data/osd/files/575/?page=0&size=25"
STUDY_PAGE = "https://osdr.nasa.gov/bio/repo/data/studies/OSD-575"


def walk(obj):
    if isinstance(obj, dict):
        yield obj
        for value in obj.values():
            yield from walk(value)
    elif isinstance(obj, list):
        for value in obj:
            yield from walk(value)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    print("Querying NASA OSDR public file API for OSD-575...")
    try:
        response = requests.get(API, timeout=45)
        response.raise_for_status()
        payload = response.json()
    except Exception as exc:
        print(f"Could not query API: {exc}\nOpen the official study page: {STUDY_PAGE}")
        return

    (OUT / "osd575_api_response.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    candidates, seen = [], set()
    url_keys = ("file_url", "download_url", "url", "href", "s3_url", "fileUrl", "downloadUrl")
    name_keys = ("file_name", "filename", "name", "fileName", "label")
    for item in walk(payload):
        url = next((item.get(k) for k in url_keys if isinstance(item.get(k), str) and item[k].startswith("http")), None)
        if not url or url in seen:
            continue
        if "/osdr/data/osd/files/" in url and url.rstrip("/").endswith("575"):
            continue
        name = next((item.get(k).strip() for k in name_keys if isinstance(item.get(k), str) and item[k].strip()), None)
        if not name:
            name = url.split("/")[-1].split("?")[0] or "osd575_download"
        candidates.append((name, url))
        seen.add(url)

    if not candidates:
        print("No direct download links were exposed in the API response.")
        print("API response saved to data/raw/osd575_api_response.json for inspection.")
        print(f"Open {STUDY_PAGE}, expand Files, and download public tables/metadata manually.")
        print("Extract CSV/TSV/XLSX files into data/raw/ and launch the dashboard.")
        return

    downloaded = 0
    for name, url in candidates:
        safe_name = re.sub(r"[^A-Za-z0-9._-]+", "_", name)
        if not Path(safe_name).suffix:
            safe_name += Path(url.split("?")[0]).suffix or ".download"
        destination = OUT / safe_name
        if destination.exists():
            print(f"Already exists, skipping: {destination.name}")
            continue
        try:
            print(f"Downloading {safe_name}")
            with requests.get(url, stream=True, timeout=90) as r:
                r.raise_for_status()
                with destination.open("wb") as f:
                    for chunk in r.iter_content(chunk_size=262144):
                        if chunk:
                            f.write(chunk)
            downloaded += 1
        except Exception as exc:
            print(f"Could not download {url}: {exc}")
    print(f"Finished. Downloaded {downloaded} file(s) to {OUT}")
    print("Inspect the study metadata and units before interpreting any result.")


if __name__ == "__main__":
    main()
