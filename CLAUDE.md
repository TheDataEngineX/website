# CLAUDE.md — DEX Website

> Workspace-wide rules in `../CLAUDE.md`.

## Project Overview

Marketing site for thedataenginex.org. Static site generated with Pelican, deployed to Cloudflare Pages.

**Stack:** Pelican · Python 3.13+ · uv · Custom `dex` theme

**Live site:** https://thedataenginex.org

## Commands

```bash
uv run poe dev     # Dev server at http://localhost:8080 (live reload)
uv run poe build   # Production build → output/
uv run poe serve   # Serve output/ locally
uv run poe clean   # Remove output/
```

## Key Files

| Path | Purpose |
|------|---------|
| `pelicanconf.py` | Dev config (localhost) |
| `publishconf.py` | Production config (thedataenginex.org) |
| `content/pages/` | Static pages (why.md, changelog.md) |
| `themes/dex/` | Custom Pelican theme |
| `content/extra/CNAME` | Cloudflare/GitHub Pages CNAME |
| `.github/workflows/deploy.yml` | CI deploy via Cloudflare Pages Action |
