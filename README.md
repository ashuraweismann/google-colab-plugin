# Google Colab Plugin

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](plugin.json)

Connect AI coding agents to **Google Colab** via the official [Colab MCP Server (`colab-mcp`)](https://github.com/googlecolab/colab-mcp), built to the [Google Antigravity Plugin Standards](https://antigravity.google/docs/build-plugins/).

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
|   (Antigravity)   |                 +----------+----------+
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

## Directory Structure

```text
google-colab/
├── plugin.json                 # Manifest complying with antigravity.google/schemas/v1/plugin.json
├── README.md                   # Plugin documentation and setup instructions
├── LICENSE                     # Apache 2.0 open-source license
├── mcp_config.json             # MCP server configuration for colab-mcp
├── assets/
│   └── logo.svg                # Colab branding logo
├── rules/
│   └── AGENTS.md               # Active rules for compute offloading
└── skills/
    └── google-colab/
        └── SKILL.md            # Agent skill for session bridging and notebook management
```

---

## Installation

### Via Antigravity CLI (`agy`)
```bash
# Clone the repository
git clone https://github.com/ashuraweismann/google-colab-plugin.git

# Validate manifest and components
agy plugin validate --strict ./google-colab-plugin

# Install locally
agy plugin install ./google-colab-plugin
```

### Manual Installation
Clone directly into your Antigravity user plugins directory:

**Windows (PowerShell):**
```powershell
git clone https://github.com/ashuraweismann/google-colab-plugin.git "$env:USERPROFILE\.gemini\config\plugins\google-colab"
```

**macOS / Linux:**
```bash
git clone https://github.com/ashuraweismann/google-colab-plugin.git ~/.gemini/config/plugins/google-colab
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

## Author & Credits

* **Plugin Author & Maintainer**: [ashuraweismann](https://github.com/ashuraweismann)
* **Upstream MCP Server**: Powered by the official open-source [Google Colab MCP Server (`googlecolab/colab-mcp`)](https://github.com/googlecolab/colab-mcp), developed by the Google Colab team (Apache-2.0).

## License

[Apache-2.0](LICENSE)
