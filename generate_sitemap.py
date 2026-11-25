from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote
from xml.sax.saxutils import escape

BASE_URL = "https://seakatutoring.netlify.app"

PAGES = [
    {"path": "/", "changefreq": "weekly", "priority": "1.0"},
    {"path": "/counselling.html", "changefreq": "monthly", "priority": "0.8"},
    {"path": "/resources.html", "changefreq": "weekly", "priority": "0.8"},
    {"path": "/tutoring companies.html", "changefreq": "monthly", "priority": "0.8"},
]

OUTPUT_FILE = Path("sitemap.xml")


def build_sitemap(base_url: str, pages: list[dict[str, str]]) -> str:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    url_entries: list[str] = []

    for page in pages:
        raw_path = page["path"] if page["path"].startswith("/") else f"/{page['path']}"
        encoded_path = quote(raw_path, safe="/")
        full_url = escape(f"{base_url.rstrip('/')}{encoded_path}")
        changefreq = escape(page["changefreq"])
        priority = escape(page["priority"])

        entry = (
            "  <url>\n"
            f"    <loc>{full_url}</loc>\n"
            f"    <lastmod>{today}</lastmod>\n"
            f"    <changefreq>{changefreq}</changefreq>\n"
            f"    <priority>{priority}</priority>\n"
            "  </url>"
        )
        url_entries.append(entry)

    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(url_entries)
        + "\n</urlset>\n"
    )


def main() -> None:
    xml_content = build_sitemap(BASE_URL, PAGES)
    OUTPUT_FILE.write_text(xml_content, encoding="utf-8")
    print(f"Generated {OUTPUT_FILE} with {len(PAGES)} URLs.")


if __name__ == "__main__":
    main()
