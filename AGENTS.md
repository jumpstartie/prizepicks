# AGENTS.md

## Cursor Cloud specific instructions

This repo is a single static web app: the **PrizePicks MLB Props Finder**
(`index.html`, `styles.css`, `app.js`, `data.js`). There is no backend, no
build step, and no third-party dependencies.

- Run the app: `npm start` (serves the static files via
  `python3 -m http.server 4173`), then open <http://localhost:4173>. There is
  no hot reload — edit a file and refresh the browser.
- Lint/validate JS: `npm test` runs `node --check` on `app.js` and `data.js`.
  Run it from the repo root; `node --check` resolves paths relative to the
  current directory.
- There is no separate build/lint tool beyond the above; do not look for
  webpack/eslint/tsc configs.
- The slate in `data.js` (`MLB_PROPS`) is representative **sample** data.
  `api.prizepicks.com` is behind a DataDome bot challenge and returns HTTP 403
  to plain server/browser requests, so live projections cannot be fetched here.
  To use real data, replace `MLB_PROPS` (see README "Connecting real PrizePicks
  data").
