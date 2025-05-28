<div align="center">

<h1>Ollama-Chutes.ai Proxy Server ↔️☁️</h1>

<p>
  An Ollama-compatible API proxy server that interfaces with Chutes.ai's LLM services.
</p>
<p>:earth_americas: <a href="https://github.com/2jang/ollama-chutesai-proxy/blob/main/README-ko.md">한국어</a> | <a href="https://github.com/2jang/ollama-chutesai-proxy">English</a></p>

</div>

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)]([https://www.python.org/](https://www.python.org/))

<br />

This project is an asynchronous API server built with Python and `aiohttp`. It acts as a proxy, providing an Ollama-compatible interface that forwards requests to Chutes.ai's LLM services.
This allows users to interact with Chutes.ai models using clients designed for Ollama (like WebUIs). 🚀

The server handles request transformation, parameter mapping, system prompt injection, message history management, and streams responses back to the client in the Ollama format.

## ✨ Key Features

- ⚙️ **Easy Configuration**: Setup via `config.py` for API tokens, model names, server port, and default LLM parameters.
- 💨 **Streaming Support**: Handles streaming responses from Chutes.ai and delivers them to the client.

## ❓ What is Chutes.ai?

Chutes.ai is a service that allows you to use various LLMs by making API requests. Many of their models are available for free. Feel free to explore their models!

## 🚀 Getting Started

### 📋 Prerequisites

-   **Python**: Make sure you have Python 3.8+ installed.
-   **pip**: Python's package installer, usually comes with Python.
-   **Chutes.ai API Key**: Obtain an API Key from [Chutes.ai](https://chutes.ai/app/api). This is **required**.

### 🛠️ Installation Steps

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/2jang/ollama-chutesai-proxy.git
    cd ollama-chutesai-proxy
    ```

2.  **Install required Python packages**:
    ```bash
    pip install aiohttp
    ```

### 🔑 Configuration (`config.py`)

Before running the server, you **must** configure it.  
Edit the `config.py` file and fill in the required and optional parameters.

**Required:**
* `API_TOKEN`: Your Chutes.ai API token.

Once configured and dependencies are installed, you can start the server:

```bash
python main.py
```

## 🖥️ Connecting from a WebUI

If you are using a WebUI that supports connecting to an Ollama API endpoint (like Ollama WebUI, Open WebUI, etc.), you can configure it to use this proxy server.

1.  In your WebUI, navigate to **Settings**- > **Admin Settings** -> **Connection**.
2.  Add or modify the Ollama API URL:
    * If this proxy server is running on your **local machine** (same machine as the WebUI or accessible on the local network), use:
      `http://localhost:11435`
      (Ensure `11435` matches the `SERVER_PORT` in your `config.py`.)
    * If the WebUI is running inside a **Docker container** and this proxy server is running on the host machine, use:
      `http://host.docker.internal:11435`
      (This address allows the Docker container to reach services running on the host. Again, ensure the port is correct.)

After saving the settings, you should be able to select with your model.

## 🧩 Tech Stack

-   **Core**:
    -   [Python](https://www.python.org/) (3.8+)
-   **Asynchronous HTTP**:
    -   [aiohttp](https://docs.aiohttp.org/en/stable/) (for asynchronous HTTP client/server)
-   **Concurrency**:
    -   [asyncio](https://docs.python.org/3/library/asyncio.html) (for asynchronous programming, built into Python)

## 🤝 Contributing

Contributions are always welcome! Whether it's bug reports, feature suggestions, or Pull Requests. If you'd like to contribute, please follow these steps:

1.  Fork this repository.
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

## 📝 License

This project is distributed under the MIT License. See the `LICENSE` file for more information.

## 🙏 Acknowledgements

* [Chutes.ai](https://chutes.ai/) - For providing the LLM services.
* [Ollama](https://ollama.com/) - For the API specification this proxy aims to be compatible with.

---

⭐ If you find this project useful, please consider giving it a Star! ⭐
