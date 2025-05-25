<div align="center">

  <img src="assets/logo.png" alt="logo" width="200" height="auto" /> <h1>Ollama-Chutes.ai Proxy Server</h1>

  <p>
    An Ollama-compatible API proxy server that interfaces with Chutes.ai's LLM services.
  </p>

</div>

<br />

# :notebook_with_decorative_cover: Table of Contents

- [About the Project](#star2-about-the-project)
  * [Tech Stack](#space_invader-tech-stack)
  * [Features](#dart-features)
- [Getting Started](#toolbox-getting-started)
  * [Prerequisites](#bangbang-prerequisites)
  * [Configuration](#key-configuration-configpy)
  * [Installation](#gear-installation)
  * [Run Locally](#running-run-locally)
- [Usage](#eyes-usage)
  * [API Endpoints](#electric_plug-api-endpoints)
- [Roadmap](#compass-roadmap)
- [Contributing](#wave-contributing)
  * [Code of Conduct](#scroll-code-of-conduct)
- [License](#warning-license)
- [Contact](#handshake-contact)
- [Acknowledgements](#gem-acknowledgements)



## :star2: About the Project

This project is an asynchronous API server built with Python and `aiohttp`. It acts as a proxy, providing an Ollama-compatible interface that forwards requests to Chutes.ai's Large Language Model (LLM) services. This allows users to interact with Chutes.ai models using clients designed for Ollama.

The server handles request transformation, parameter mapping, system prompt injection, message history management, and streams responses back to the client in the Ollama format.

### :space_invader: Tech Stack

<ul>
  <li><a href="https://www.python.org/">Python</a></li>
  <li><a href="https://docs.aiohttp.org/en/stable/">aiohttp</a> (for asynchronous HTTP client/server)</li>
  <li><a href="https://docs.python.org/3/library/asyncio.html">asyncio</a> (for asynchronous programming)</li>
</ul>

### :dart: Features

- **Ollama Compatibility:** Implements key Ollama API endpoints:
  - `POST /api/chat`: For chat completions (streaming and non-streaming).
  - `GET /api/tags`: Lists available models (as configured).
  - `GET /api/version`: Returns the proxy server's version.
- **Chutes.ai Backend:** Seamlessly routes requests to the configured Chutes.ai API.
- **Configuration via `config.py`:** Easy setup for API tokens, model names, server ports, and default LLM parameters.
- **System Prompt Management:**
  - Allows a default system prompt to be set in `config.py`.
  - Uses client-provided system prompts if available.
- **Message History Control:** Configurable maximum number of messages to retain in the conversation history (`MAX_HISTORY_MESSAGES`).
- **Parameter Mapping:** Translates Ollama client parameters to their Chutes.ai equivalents. Supports overriding server defaults with client-sent options.
- **Streaming Support:** Handles streaming responses from Chutes.ai and forwards them as newline-delimited JSON (NDJSON) to the client.
- **Debug Mode:** Verbose logging for request/response details and internal operations.

## :toolbox: Getting Started

Follow these steps to get the proxy server up and running on your local machine.

### :bangbang: Prerequisites

Make sure you have Python 3.8+ installed. You'll also need `pip` for installing packages.

```bash
python --version
pip --version
```
:key: Configuration (config.py)
Before running the server, you need to configure it.

Create config.py:
If a config.example.py is provided, rename it to config.py. Otherwise, create a new file named config.py in the root of the project directory.

Edit config.py:
Open config.py and fill in the required and optional parameters. At a minimum, you must provide your API_TOKEN.