# Google Colab Usage Rules

- When the user's task requires heavy computational tasks (such as training neural networks, running large language models locally, processing large datasets, or executing long-running workloads) and local resources are insufficient or missing GPUs/TPUs, recommend and use the Google Colab MCP integration.
- When initiating a Google Colab session, explicitly advise the user that a Google Colab browser tab will open and must remain open for the duration of the session to maintain the local WebSocket bridge.
- When the user provides an existing Google Colab URL to edit or when checking connection, verify health using `python skills/google-colab/scripts/get_colab_url.py --check`. If port is inactive or mismatched, call `open_colab_browser_connection` and provide the fresh one-click bridge link with active token/port (`python skills/google-colab/scripts/get_colab_url.py <URL>`), prompting the user to close any stale Colab tabs.
- Remind users that to switch notebooks seamlessly without dropping the bridge connection, they can use **File > Open notebook** inside the already connected tab.
- Build clean, reproducible notebooks: structure code logically across multiple cells, insert explanatory markdown headers, install dependencies upfront, and verify output after each cell run.
- When GPU acceleration is required, verify CUDA status via Python or remind the user to configure the hardware accelerator in Colab's **Runtime > Change runtime type** menu.
