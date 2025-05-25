<div align="center">

  <h1>Ollama-Chutes.ai Proxy Server</h1>

  <p>
    An Ollama-compatible API proxy server that interfaces with Chutes.ai's LLM services.
  </p>

<p>:earth_americas: <a href="https://github.com/2jang/ollama-chutesai-proxy">English</a> | <a href="https://github.com/2jang/ollama-chutesai-proxy/blob/main/README-ko.md">한국어</a></p>

</div>

<br />

# :notebook_with_decorative_cover: Table of Contents

- [About the Project](#star2-about-the-project)
    * [Tech Stack](#space_invader-tech-stack)
    * [Features](#dart-features)
- [Getting Started](#toolbox-getting-started)
    * [Prerequisites](#bangbang-prerequisites)
    * [Installation](#gear-installation)
    * [Configuration](#key-configuration-configpy)
    * [Run](#running-run-locally)
- [Connecting from a WebUI](#desktop_computer-connecting-from-a-webui)



## :star2: About the Project

This project is an asynchronous API server built with Python and `aiohttp`. It acts as a proxy, providing an Ollama-compatible interface that forwards requests to Chutes.ai's Large Language Model (LLM) services. This allows users to interact with Chutes.ai models using clients for Ollama(WebUI).

The server handles request transformation, parameter mapping, system prompt injection, message history management, and streams responses back to the client in the Ollama format.

### :space_invader: Tech Stack

<ul>
  <li><a href="https://www.python.org/">Python</a></li>
  <li><a href="https://docs.aiohttp.org/en/stable/">aiohttp</a> (for asynchronous HTTP client/server)</li>
  <li><a href="https://docs.python.org/3/library/asyncio.html">asyncio</a> (for asynchronous programming)</li>
</ul>

### :dart: Features

- **Ollama Compatibility:** Implements key Ollama API endpoints
- **Chutes.ai API:** Seamlessly routes requests to the configured Chutes.ai API.
- **Configuration via `config.py`:** Easy setup for API tokens, model names, server ports, and default LLM parameters.
- **Streaming Support:** Handles streaming responses from Chutes.ai to the client.

## :toolbox: Getting Started

Follow these steps to get the proxy server up and running on your local machine.

### :bangbang: Prerequisites

- Make sure you have Python 3.8+ installed. You'll also need `pip` for installing packages.
- Get a API Keys for Chutes.ai https://chutes.ai/app/api

### :gear: Installation

1.  Clone the repository (if you haven't already):
    ```bash
    git clone https://github.com/2jang/ollama-chutesai-proxy.git
    cd ollama-chutesai-proxy 
    ```

2.  Install the required Python packages:
    ```bash
    pip install aiohttp
    ```

### :key: Configuration (`config.py`)

Before running the server, you need to configure it.  
Edit `config.py` and fill in the required and optional parameters. At a minimum, you **must** provide your `API_TOKEN`.

### :running: Run Locally

Once configured and dependencies are installed, you can start the server:

```bash
python main.py
```

### :desktop_computer: Connecting from a WebUI

If you are using a WebUI that supports connecting to an Ollama API endpoint, you can configure it to use this proxy server.

1.  In your WebUI, navigate to **Settings** -> **Admin Settings** -> **Connections**.
2. Add or modify the Ollama API URL:
    * If this proxy server is running on your **local machine** (same machine as the WebUI or accessible on the local network), use:
      `http://localhost:11435`
      (Ensure `11435` matches the `SERVER_PORT` in your `config.py`.)
    * If the WebUI is running inside a **Docker container** and this proxy server is running on the host machine, use:
      `http://host.docker.internal:11435`
      (This address allows the Docker container to reach services running on the host. Again, ensure the port is correct.)

After saving the settings, you can see your model at the model list.

## :handshake: Acknowledgments

* [Chutes.ai](https://chutes.ai/)
* [Ollama](https://ollama.com/)
