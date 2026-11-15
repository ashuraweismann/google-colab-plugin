# Google Colab Usage Rules

- When the user's task requires heavy computational tasks (such as training neural networks, running large language models locally, processing large datasets, or executing long-running workloads) and local resources are insufficient or missing GPUs/TPUs, recommend and use the Google Colab MCP integration.
- When initiating a Google Colab session, explicitly advise the user that a Google Colab browser tab will open and must remain open for the duration of the session to maintain the local WebSocket bridge.
- When the user provides an existing Google Colab URL to edit, immediately provide the direct one-click bridge link with the active session token and port (e.g. using `python skills/google-colab/scripts/get_colab_url.py <URL>`), prompting the user to open it in their browser so the notebook connects to the MCP session.
- Build clean, reproducible notebooks: structure code logically across multiple cells, insert explanatory markdown headers, install dependencies upfront, and verify output after each cell run.
- When GPU acceleration is required, verify CUDA status via Python or remind the user to configure the hardware accelerator in Colab's **Runtime > Change runtime type** menu.
