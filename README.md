# 🌌 MCP Star Gazing Server

This project implements a **Model Context Protocol (MCP)** server that provides information about upcoming **lunar eclipses** using the [`skyfield`](https://rhodesmill.org/skyfield/) astronomy library.

Built with [FastMCP](https://github.com/ContextualAI/mcp), this server offers a tool endpoint to compute lunar eclipses between two ISO 8601 timestamps.

---

## 🛠 Features

- Computes upcoming **lunar eclipse** events using JPL ephemeris data (`de421.bsp`)
- Uses `skyfield.eclipselib.lunar_eclipses` for precise astronomy calculations
- Returns eclipse metadata in a structured format (time, type, and additional data)

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Prakul95/mcp-python-star-gazing.git
cd mcp-python-star-gazing
```

### 2. Set up the virtual environment

```bash
uv venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
uv pip sync pyproject.toml
```

This installs:
- `mcp[cli]`
- `requests`
- `skyfield`

### 4. Run the MCP server

```bash
mcp run mcp_star_gazing.py
```

You should see:
```
[mcp] Running server...
[mcp] Available tools: get_lunar_eclipse
```

---

## 🧪 Usage

You can call the tool from a connected MCP client:

```json
{
  "method": "get_lunar_eclipse",
  "params": {
    "starting_time_iso_datetime": "2026-01-01T00:00",
    "ending_time_iso_datetime": "2026-12-31T23:59"
  }
}
```

### Sample response:

```json
{
  "2026-03-03 11:36": [
    "y=1",
    "Total eclipse of the Moon",
    {
      "duration": 102.5
    }
  ]
}
```

---

## 📦 Project Structure

```
mcp-python-star-gazing/
├── mcp_star_gazing.py       # Main MCP server with lunar eclipse logic
├── pyproject.toml           # Project + dependency definitions
├── uv.lock                  # Pinned versions of all dependencies
└── .gitignore               # Ignore venv and cache
```

---

## 🧠 How It Works

- Uses `skyfield.api.Loader` to fetch planetary ephemeris data
- Converts ISO 8601 strings to Skyfield time objects
- Calls `eclipselib.lunar_eclipses()` with start and end times
- Formats and returns eclipse info

---

## 📅 Ephemeris Data Note

By default, `skyfield` downloads `de421.bsp` into a temporary path:
```python
load = Loader('/tmp/skyfield')
```

You may update this path in `mcp_star_gazing.py` for caching or persistent storage.

---

## 🧑‍💻 Author

👤 [Prakul](https://github.com/Prakul95)

---

## 🪐 License

MIT License — use freely, modify responsibly, observe wisely.
