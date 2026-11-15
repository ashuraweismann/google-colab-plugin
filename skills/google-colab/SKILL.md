---
name: google-colab
description: Interact with Google Colab via the official Colab MCP server. Offload heavy computation, machine learning, and data science tasks to Google Colab cloud runtimes (CPUs, GPUs, TPUs), programmatically create and structure notebook cells, execute Python code, and stream outputs in real time.
---

# Google Colab Integration

This skill guides the use of Google Colab via the official [Colab MCP Server (`colab-mcp`)](https://github.com/googlecolab/colab-mcp), announced in the [Google Developers Blog](https://developers.googleblog.com/announcing-the-colab-mcp-server-connect-any-ai-agent-to-google-colab/).

## Architecture & How It Works

The Colab MCP server acts as a local-to-cloud bridge using a **WebSocket session proxy**:

1. **Local Proxy Launch**: When the MCP server starts, it initializes a local WebSocket server on localhost with an ephemeral handshake token.
2. **Browser Tab Connection**: The agent calls `open_colab_browser_connection` (or the equivalent initialization tool). This launches a Google Colab notebook session in the user's default browser (Google Chrome).
3. **Local WebSocket Handshake**: The Colab browser frontend detects the token parameters and establishes a bidirectional WebSocket back to the local MCP server.
4. **Dynamic Tool Exposure**: Once the handshake completes, the Colab MCP server dynamically publishes notebook manipulation tools (`add_code_cell`, `run_code_cell`, `update_cell`, `get_cells`, etc.) to the agent via MCP's `notifications/tools/list_changed` protocol.
5. **Interactive Execution**: The agent sends commands through MCP, the server pushes them via WebSocket to the browser tab, and Colab's cloud kernel executes the code, streaming results, plots, and logs back to the agent while rendering live in the browser for the user.

> [!IMPORTANT]
> The browser tab running Google Colab must remain open and connected for the duration of the session. If the user closes the tab, the WebSocket bridge disconnects.

---

## Prerequisites

- **Google Chrome**: Recommended for standard localhost WebSocket support (Private Network Access policies in some other browsers like Safari may block localhost bridges).
- **Google Account**: The user must be signed into Google in their browser to access Google Colab (`colab.research.google.com`).
- **Python & `uv`**: Required to run the MCP server via `uvx`.

---

## Tool Workflow

### 1. Initiating the Session
Call `open_colab_browser_connection` to begin.
- Inform the user that a Google Colab tab will open in their browser.
- Prompt the user to keep the tab open while the agent works.
- Wait for the dynamic tool list to register.

### 2. Inspecting the Notebook
- Use `get_cells` to inspect existing code cells, markdown cells, and outputs in the current notebook.
- Always check the current structure before appending or editing to avoid overwriting user work or duplicating setup.

### 3. Structuring the Notebook
When generating a notebook, organize it logically:
- **Markdown Cells**: Add section headers (`# Data Ingestion`, `## Model Training`, `### Evaluation`) and concise explanations so the resulting notebook is a polished, reproducible document.
- **Setup & Dependencies**: Add a cell at the top for `!pip install ...` or `import ...` statements.
- **Code Execution Cells**: Split operations into manageable chunks (data loading -> exploration -> model definition -> training -> visualization).

### 4. Executing Code
- Call `run_code_cell` (or `proxy_execute_cell`) to execute code on Colab's cloud kernel.
- Inspect the output:
  - Text stdout/stderr
  - Rich output (dataframes, tables)
  - Generated plots (Matplotlib, Seaborn, Plotly)
  - Exceptions and tracebacks
- If an execution fails, inspect the error message and traceback, make adjustments with `update_cell`, and re-execute.

### 5. Managing Cloud Accelerators (GPU / TPU)
- Colab provides free and paid access to hardware accelerators (NVIDIA T4, V100, A100 GPUs, and Google TPUs).
- If the user needs GPU acceleration, remind them they can select **Runtime > Change runtime type > GPU (e.g. T4)** in the Colab browser UI.
- Verify GPU availability in code:
  ```python
  import torch
  print(f"CUDA Available: {torch.cuda.is_available()}")
  if torch.cuda.is_available():
      print(f"Device: {torch.cuda.get_device_name(0)}")
  ```

---

## Best Practices

1. **Keep Cells Modular**: Never dump hundreds of lines into a single cell. Break work into distinct, logically isolated cells.
2. **Handle Dependencies Early**: Run all required `!pip install` statements in an early setup cell.
3. **Iterative Execution & Feedback**: Execute cells sequentially and verify the output of each before proceeding to the next.
4. **Preserve User Context**: If interacting with an existing notebook, read current cells first before making changes.
5. **Informative Markdown**: Include explanations, assumptions, and next steps in markdown cells to ensure the notebook serves as an enduring, readable artifact.
