# Encar Live Catalog

Live car catalog demo that fetches real-time data from Encar API.

## Features
- 5 active car cards with live data
- 1 placeholder card for upcoming vehicles
- Auto-refresh every 30 seconds
- Korean to English translation

## Tech Stack
- Node.js + Express (Backend proxy)
- Vanilla HTML/CSS/JS (Frontend)
- Encar Internal API

## Installation

```bash
npm install
npm start
```

Open http://localhost:3001/catalog.html

## Files
- `catalog.html` - Main catalog page
- `server.js` - Express proxy server
- `encar_api_test.py` - Python API testing script
