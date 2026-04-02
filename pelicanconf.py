from __future__ import annotations

AUTHOR = "Jay"
SITENAME = "DataEngineX"
SITEURL = "http://localhost:8080"
SITETITLE = "DataEngineX — Data + ML + AI Framework"
SITEDESCRIPTION = "Unified Data + ML + AI framework. Config-driven, self-hosted, production-ready."

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

# Navigation
MENUITEMS = [
    ("Why DEX", "/why/"),
    ("Docs", "https://docs.thedataenginex.org"),
    ("Changelog", "/changelog/"),
    ("GitHub", "https://github.com/TheDataEngineX/DEX"),
]

# Plugins
PLUGINS = ["pelican.plugins.sitemap"]
SITEMAP = {"format": "xml"}

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
GITHUB_URL = "https://github.com/TheDataEngineX/DEX"
PYPI_URL = "https://pypi.org/project/dataenginex/"
DOCS_URL = "https://docs.thedataenginex.org"
