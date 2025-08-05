# 🌌 MCP Star Gazing Server

This project implements a **Model Context Protocol (MCP)** server that provides information about upcoming **lunar eclipses** using the [`skyfield`](https://rhodesmill.org/skyfield/) astronomy library.

Built with [FastMCP](https://github.com/modelcontextprotocol/python-sdk?tab=readme-ov-file#fastmcp-properties), this server offers a tool endpoint to compute lunar eclipses between two ISO 8601 timestamps.

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

## API Key Setup

This project uses the OpenWeatherMap API to fetch real weather data. You'll need to:

1. Sign up for a free account at [OpenWeatherMap](https://openweathermap.org/api)
2. Get your API key from the dashboard
3. Set the environment variable:

```sh
export OPENWEATHER_API_KEY=your_api_key_here
```

### 4. Run the MCP server

```bash
mcp dev mcp_star_gazing.py
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

For adding the tool to Claude update the config as:

```json
{
  "mcpServers": {
    "star-gazing": {
      "command": "uv",
      "args": ["run", "[...]", "/[PATH_TO_PROJECT]/src/mcp_star_gazing.py"],
      "env": {
        "OPENWEATHER_API_KEY": "your_api_key_here"
      }
    }
  }
}
```
(This example is simplified — refer to https://modelcontextprotocol.io/quickstart/user for more details)

And this will live inside the `claude_desktop_config.json` file which you can access via the Developer settings. But you can also take a shortcut and install it right away by running this command (which will just create the entry in the config file for you):

```sh
mcp install mcp_star_gazing.py
```

You will need to restart Claude desktop to see the tool in your "search and tools" section.

For options on implementing MCP clients in code:

- https://modelcontextprotocol.io/quickstart/client
- https://github.com/mcp-use/mcp-use

## 🧑‍💻 Author

👤 [Prakul](https://github.com/Prakul95)

---

## 🪐 License

MIT License — use freely, modify responsibly, observe wisely.
