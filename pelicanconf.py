from __future__ import annotations

AUTHOR = "TheDataEngineX"
SITENAME = "TheDataEngineX"
SITEURL = "https://thedataenginex.org"
SITETITLE = "DataEngineX — Complete Data + ML + AI Engineering Platform"
SITEDESCRIPTION = "DataEngineX is the complete platform for Data + ML + AI engineering. Production-ready pipelines, ML lifecycle, and AI agents unified under one dex.yaml. Native integrations with Airflow, MLflow, LangChain, and more."
SITE_KEYWORDS = "DataEngineX, complete data platform, end-to-end ML platform, AI engineering platform, self-hosted data platform, data ML AI framework, dex framework, config-driven data pipeline, Python data framework, DuckDB pipeline, MLflow integration, LangChain integration"

PATH = "content"
TIMEZONE = "UTC"
DEFAULT_LANG = "en"

# Disable blog
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
DEFAULT_PAGINATION = False

# Theme
THEME = "themes/dex"

# Navigation — Docs now points to local
MENUITEMS = [
    ("Why DataEngineX", "/why/"),
    ("Philosophy", "/philosophy/"),
    ("Docs", "/docs/dataenginex/latest/"),
    ("Changelog", "/changelog/"),
    ("GitHub", "https://github.com/TheDataEngineX/dataenginex"),
]

# Plugins — disabled sitemap; build_site.py generates complete sitemap
PLUGINS = []

# Static paths
STATIC_PATHS = ["extra"]
EXTRA_PATH_METADATA = {
    "extra/robots.txt": {"path": "robots.txt"},
    "extra/CNAME": {"path": "CNAME"},
}

# Pages
PAGE_URL = "{slug}/"
PAGE_SAVE_AS = "{slug}/index.html"
DISPLAY_PAGES_ON_MENU = False
DISPLAY_CATEGORIES_ON_MENU = False

# Social
GITHUB_URL = "https://github.com/TheDataEngineX/dataenginex"
PYPI_URL = "https://pypi.org/project/dataenginex/"
DOCS_URL = "https://thedataenginex.org/docs/dataenginex/latest/"
