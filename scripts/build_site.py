#!/usr/bin/env python3
"""Build documentation pages for thedataenginex.org.

Runs after Pelican. Walks docs-store/, renders .md -> .html via Jinja2,
generates sitemap.xml, robots.txt (overwriting Pelican's), and
search-index.json. Outputs to Pelican's output/ directory.
"""

import json
import os
import re
import shutil
from datetime import datetime
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader
from markdown import markdown

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = REPO_ROOT / "config" / "site.yml"
DOCS_STORE = REPO_ROOT / "docs-store"
TEMPLATES_DIR = REPO_ROOT / "templates"
OUTPUT_DIR = REPO_ROOT / "output"


def load_config():
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)


def discover_docs_versions(docs_store: Path) -> dict:
    """Return {repo_name: [version_str, ...]} sorted newest first."""
    result = {}
    if not docs_store.exists():
        return result
    for repo_dir in sorted(docs_store.iterdir()):
        if not repo_dir.is_dir() or repo_dir.name.startswith("."):
            continue
        versions = []
        for ver_dir in sorted(repo_dir.iterdir(), reverse=True):
            if ver_dir.is_dir() and not ver_dir.name.startswith("."):
                versions.append(ver_dir.name)
        if versions:
            result[repo_dir.name] = sorted(versions, key=parse_semver, reverse=True)
    return result


def parse_semver(version_str: str) -> tuple:
    match = re.match(r"^v?(\d+)\.(\d+)\.(\d+)$", version_str)
    if match:
        return tuple(int(g) for g in match.groups())
    return (0, 0, 0)


def get_doc_tree(repo_dir: Path) -> list[dict]:
    """Return [{slug, title, path}] sorted alphabetically."""
    docs = []
    for f in sorted(repo_dir.iterdir()):
        if f.suffix == ".md":
            slug = f.stem
            content = f.read_text(encoding="utf-8")
            title = extract_title(content) or slug.replace("-", " ").title()
            docs.append({"slug": slug, "title": title, "path": f})
    return docs


def extract_title(md_content: str) -> str | None:
    match = re.search(r"^#\s+(.+)$", md_content, re.MULTILINE)
    return match.group(1).strip() if match else None


def extract_description(md_content: str) -> str | None:
    lines = md_content.split("\n")
    in_para = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# "):
            in_para = True
            continue
        if in_para and stripped:
            return (stripped[:152] + "...") if len(stripped) > 155 else stripped
        if in_para and not stripped:
            continue
        if in_para and stripped.startswith("#"):
            break
    return None


def extract_toc(md_content: str) -> list[dict]:
    items = []
    for line in md_content.split("\n"):
        match = re.match(r"^(#{2,3})\s+(.+)$", line)
        if match:
            text = match.group(2).strip()
            anchor_id = text.lower().replace(" ", "-").replace(".", "").replace(",", "")
            items.append({"level": len(match.group(1)), "text": text, "id": anchor_id})
    return items


def render_markdown_to_html(md_content: str) -> str:
    extensions = ["fenced_code", "codehilite", "tables", "sane_lists", "attr_list"]
    return markdown(md_content, extensions=extensions)


def get_highest_semver(versions: list[str]) -> str:
    if not versions:
        return ""
    sorted_vers = sorted(versions, key=parse_semver, reverse=True)
    return sorted_vers[0]


def compute_is_stale(last_updated_str: str | None, months_threshold: int = 6) -> tuple[bool, int]:
    if not last_updated_str:
        return False, 0
    try:
        updated = datetime.strptime(last_updated_str, "%Y-%m-%d").date()
    except ValueError:
        return False, 0
    delta = datetime.now().date() - updated
    months = delta.days // 30
    return months > months_threshold, months


def generate_sitemap(pages: list[dict], site_url: str) -> str:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for p in pages:
        loc = f"{site_url}{p['url']}"
        lastmod = p.get("last_updated") or datetime.now().strftime("%Y-%m-%d")
        priority = p.get("priority", "0.7")
        changefreq = p.get("changefreq", "monthly")
        lines.append("  <url>")
        lines.append(f"    <loc>{loc}</loc>")
        lines.append(f"    <lastmod>{lastmod}</lastmod>")
        lines.append(f"    <priority>{priority}</priority>")
        lines.append(f"    <changefreq>{changefreq}</changefreq>")
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines)


def generate_robots_txt(site_url: str) -> str:
    return f"User-agent: *\nAllow: /\n\nSitemap: {site_url}/sitemap.xml\n"


def minify_html(html: str) -> str:
    html = re.sub(r"\s+", " ", html)
    html = re.sub(r">\s+<", "><", html)
    return html.strip()


def minify_css(css: str) -> str:
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{}:;,])\s*", r"\1", css)
    css = re.sub(r";}", "}", css)
    return css.strip()


def minify_js(js: str) -> str:
    js = re.sub(r"//.*", "", js)
    js = re.sub(r"/\*.*?\*/", "", js, flags=re.DOTALL)
    js = re.sub(r"\s+", " ", js)
    return js.strip()


def check_thin_content(md_content: str, slug: str) -> None:
    word_count = len(md_content.split())
    if word_count < 100:
        print(f"  WARNING: '{slug}' has only {word_count} words (below 100)")


def main():
    config = load_config()
    site = config["site"]
    repos_config = config.get("repos", {})
    all_versions = discover_docs_versions(DOCS_STORE)

    if not OUTPUT_DIR.exists():
        print(f"ERROR: Pelican output directory '{OUTPUT_DIR}' does not exist. Run Pelican build first.")
        return

    # Setup Jinja2
    env = Environment(loader=FileSystemLoader(str(REPO_ROOT)))
    env.globals["now"] = datetime.now()

    # Collect all pages for sitemap
    sitemap_pages = []

    # Scan Pelican output for existing pages (/, /why/, /changelog/, /philosophy/) to include in sitemap
    pelican_html_dirs = ["", "why", "changelog", "philosophy"]
    for subdir in pelican_html_dirs:
        index_path = OUTPUT_DIR / subdir / "index.html"
        if index_path.exists():
            url = f"/{subdir}/" if subdir else "/"
            sitemap_pages.append({
                "url": url,
                "last_updated": None,
                "priority": "1.0" if not subdir else "0.8",
                "changefreq": "monthly",
            })

    # Render docs
    search_pages = []

    for repo_name, versions in all_versions.items():
        repo_display = repos_config.get(repo_name, {}).get("display_name", repo_name)
        latest_version = get_highest_semver(versions)

        for version in versions:
            repo_dir = DOCS_STORE / repo_name / version
            if not repo_dir.is_dir():
                continue

            docs = get_doc_tree(repo_dir)
            is_latest = version == latest_version

            for doc in docs:
                md_content = doc["path"].read_text(encoding="utf-8")
                check_thin_content(md_content, doc["slug"])

                html_content = render_markdown_to_html(md_content)
                title = doc["title"]
                description = extract_description(md_content)
                last_updated = None  # placeholder; could come from git date
                is_stale, months_since = compute_is_stale(last_updated)

                toc_items = extract_toc(md_content)
                slug = doc["slug"]
                page_url = f"/docs/{repo_name}/{version}/" if slug == "index" else f"/docs/{repo_name}/{version}/{slug}/"
                canonical_url = page_url

                # Sidebar
                sidebar_items = [
                    {
                        "title": d["title"],
                        "slug": d["slug"],
                        "active": d["slug"] == slug,
                        "url": f"/docs/{repo_name}/{version}/" if d["slug"] == "index" else f"/docs/{repo_name}/{version}/{d['slug']}/",
                    }
                    for d in docs
                ]

                page_ctx = {
                    "title": title,
                    "description": description or "",
                    "url": page_url,
                    "canonical_url": canonical_url,
                    "content": html_content,
                    "slug": slug,
                    "type": "doc",
                    "last_updated": last_updated,
                    "is_stale": is_stale,
                    "months_since_update": months_since if is_stale else 0,
                    "og_image": None,
                    "toc_items": toc_items,
                }

                repo_ctx = {
                    "name": repo_name,
                    "display_name": repo_display,
                    "version": version,
                    "latest_version": latest_version,
                    "available_versions": versions,
                }

                nav_ctx = {"sidebar": sidebar_items}

                template = env.get_template("templates/docs/doc.html")
                output = template.render(
                    site=site,
                    page=page_ctx,
                    repo=repo_ctx,
                    navigation=nav_ctx,
                )

                # Write versioned page
                out_path = OUTPUT_DIR / "docs" / repo_name / version / "index.html" if slug == "index" else OUTPUT_DIR / "docs" / repo_name / version / slug / "index.html"
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_text(minify_html(output), encoding="utf-8")

                # Write to latest/
                if is_latest:
                    latest_ctx = dict(page_ctx)
                    latest_ctx["canonical_url"] = canonical_url
                    latest_output = template.render(
                        site=site,
                        page=latest_ctx,
                        repo=dict(repo_ctx, version="latest"),
                        navigation=nav_ctx,
                    )
                    latest_path = OUTPUT_DIR / "docs" / repo_name / "latest" / "index.html" if slug == "index" else OUTPUT_DIR / "docs" / repo_name / "latest" / slug / "index.html"
                    latest_path.parent.mkdir(parents=True, exist_ok=True)
                    latest_path.write_text(minify_html(latest_output), encoding="utf-8")

                # Sitemap entry (only for real version, not latest alias)
                sitemap_pages.append({
                    "url": page_url,
                    "last_updated": last_updated or datetime.now().strftime("%Y-%m-%d"),
                    "priority": "0.8",
                    "changefreq": "monthly",
                })

                # Search index entry
                search_pages.append({
                    "title": title,
                    "url": page_url,
                    "description": description or "",
                    "repo": repo_name,
                    "version": version,
                })

    # Write sitemap (overwrites Pelican's)
    sitemap_xml = generate_sitemap(sitemap_pages, site["url"])
    (OUTPUT_DIR / "sitemap.xml").write_text(sitemap_xml, encoding="utf-8")

    # Write robots.txt (overwrites Pelican's static one)
    robots_txt = generate_robots_txt(site["url"])
    (OUTPUT_DIR / "robots.txt").write_text(robots_txt, encoding="utf-8")

    # Write search index
    search_json = json.dumps(search_pages, ensure_ascii=False, indent=2)
    (OUTPUT_DIR / "search-index.json").write_text(search_json, encoding="utf-8")

    # Minify Pelican's CSS and JS
    css_path = OUTPUT_DIR / "theme" / "css" / "main.css"
    if css_path.exists():
        css_path.write_text(minify_css(css_path.read_text(encoding="utf-8")), encoding="utf-8")

    docs_css_path = OUTPUT_DIR / "theme" / "css" / "docs.css"
    if docs_css_path.exists():
        docs_css_path.write_text(minify_css(docs_css_path.read_text(encoding="utf-8")), encoding="utf-8")

    for js_path in (OUTPUT_DIR / "theme" / "js").rglob("*.js") if (OUTPUT_DIR / "theme" / "js").exists() else []:
        js_path.write_text(minify_js(js_path.read_text(encoding="utf-8")), encoding="utf-8")

    print(f"Docs built at {OUTPUT_DIR}")
    print(f"  Docs pages: {len(search_pages)}")
    print(f"  Sitemap URLs: {len(sitemap_pages)}")


if __name__ == "__main__":
    main()
