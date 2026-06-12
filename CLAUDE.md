# CLAUDE.md — DEX Website

## Project Overview
Marketing site + versioned documentation for thedataenginex.org.
Static site generated with Pelican (marketing) + custom build script (docs).
Deployed to Cloudflare Pages.

**Stack:** Pelican 4.12 · Python 3.13+ · uv · Custom `dex` theme · Jinja2 · Markdown
**Live site:** https://thedataenginex.org

## Commands
uv run poe dev        # Dev server at http://localhost:8080 (Pelican only, live reload)
uv run poe build      # Production build: Pelican + docs -> output/
uv run poe build-pelican  # Pelican only
uv run poe build-docs     # Docs only (after Pelican build)
uv run poe serve      # Serve output/ locally
uv run poe clean      # Remove output/

## Key Files
| Path | Purpose |
|------|---------|
| pelicanconf.py | Pelican dev config |
| publishconf.py | Pelican production config |
| content/pages/ | Marketing pages (why.md, changelog.md) |
| themes/dex/ | Custom Pelican theme + docs CSS/JS |
| scripts/build_site.py | Docs build script (runs after Pelican) |
| templates/docs/ | Docs Jinja2 templates |
| config/site.yml | Docs site configuration |
| docs-store/ | Versioned documentation (synced from source repos) |
| .github/workflows/deploy.yml | CI deploy via Cloudflare Pages Action |
| .github/workflows/sync.yml | Docs sync triggered by source repo releases |

## Docs Build

`scripts/build_site.py` walks `docs-store/` and renders .md -> .html.
- Output goes to Pelican's `output/docs/` directory
- Generates `output/sitemap.xml`, `output/robots.txt` (overwriting Pelican's)
- Generates `output/search-index.json` for client-side search
- Minifies HTML output

### Adding docs from a new version
```bash
# Manually add to docs-store/
mkdir -p docs-store/dataenginex/v0.2.0/
cp -r /path/to/docs/* docs-store/dataenginex/v0.2.0/
uv run poe build-docs
```

### Sync from source repo release
Source repos fire `repository_dispatch` -> `.github/workflows/sync.yml`.
