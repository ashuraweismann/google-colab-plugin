# Google Colab Plugin

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

Connect AI coding agents to **Google Colab** via the official [Colab MCP Server (`colab-mcp`)](https://github.com/googlecolab/colab-mcp), based on the Google Developers announcement: [*Announcing the Colab MCP Server: Connect any AI Agent to Google Colab*](https://developers.googleblog.com/announcing-the-colab-mcp-server-connect-any-ai-agent-to-google-colab/).

---

## Features

- **Cloud Compute Offloading**: Run resource-heavy Python code, data pipelines, and machine learning models on Google's cloud infrastructure (CPUs, NVIDIA GPUs, and Google TPUs).
- **Interactive Notebook Control**: Programmatically insert code and markdown cells, edit existing cells, and structure reproducible Jupyter/Colab notebooks.
- **Real-Time Output Streaming**: Stream logs, standard output/error, formatted tables, and Matplotlib/Seaborn visualization plots back to the agent while rendering live in your open browser tab.
- **Dynamic Tool Registration**: Connects over a local-to-cloud WebSocket bridge, dynamically exposing cell creation, editing, and execution tools.

---

## Architecture

```
+-------------------+       MCP        +---------------------+
|   AI Assistant    | <=============> |  colab-mcp (local)  |
|                   |                 +----------+----------+
+-------------------+                            |
                                      Local      | WebSocket
                                      Bridge     | (localhost)
                                                 v
                                      +---------------------+
                                      | Colab Browser Tab   |
                                      | (Google Chrome)     |
                                      +----------+----------+
                                                 |
                                      Google     | Cloud RPC
                                      Cloud      v
                                      +---------------------+
                                      | Colab Cloud Runtime |
                                      | (CPU / GPU / TPU)   |
                                      +---------------------+
```

---

## Prerequisites

1. **Python 3.10+ & `uv`**:
   The MCP server is packaged via `uvx`. Ensure `uv` is installed:
   ```bash
   pip install uv
   ```
2. **Google Chrome**:
   Colab's web interface initiates a local WebSocket connection to `localhost`. Google Chrome is recommended for seamless Private Network Access compatibility.
3. **Google Account**:
   Ensure you are logged into [Google Colab](https://colab.research.google.com) in your browser.

---

## Configuration

The MCP server configuration in `mcp_config.json`:

```json
{
  "mcpServers": {
    "colab-mcp": {
      "command": "uvx",
      "args": [
        "--system-certs",
        "git+https://github.com/googlecolab/colab-mcp"
      ],
      "env": {
        "UV_SYSTEM_CERTS": "true"
      },
      "timeout": 30000
    }
  }
}
```

---

## Usage

### Suggested Prompts
- *"Connect to Google Colab and run a GPU benchmark"*
- *"Create a Colab notebook to analyze this dataset and plot graphs"*
- *"Train a deep learning model using Colab's cloud compute"*

### Workflow
1. Prompt your agent with a computational or notebook task.
2. The agent calls the session initialization tool (`open_colab_browser_connection`).
3. A Google Colab notebook tab will open automatically in your browser.
4. **Keep the Colab browser tab open** to maintain the WebSocket bridge.
5. The agent will iteratively create cells, execute code, verify outputs, and display results.

---

## Troubleshooting & FAQ

#### The browser tab opened, but the agent says connection timed out
The handshake token is valid for a short window (typically 60 seconds). Ensure you are logged into your Google account and keep the newly opened Colab tab in the foreground until the connection establishes.

#### Safari or other browsers block the connection
Certain browsers enforce strict Private Network Access policies that block public websites (`colab.research.google.com`) from connecting to `localhost` WebSockets. Use Google Chrome as your default browser.

#### SSL/TLS certificate errors when downloading `colab-mcp`
The configuration includes `--system-certs` and `UV_SYSTEM_CERTS=true` to read certificates from your OS trust store. If you are behind a corporate proxy, ensure your corporate root CA is trusted in your system certificate store.

#### How do I enable GPU or TPU?
In the open Colab browser tab, navigate to **Runtime > Change runtime type**, select your preferred hardware accelerator (e.g., T4 GPU, A100 GPU, or TPU), and click **Save**.

---

## Author

Developed by [ashuraweismann](https://github.com/ashuraweismann).

## License

[Apache-2.0](LICENSE)
