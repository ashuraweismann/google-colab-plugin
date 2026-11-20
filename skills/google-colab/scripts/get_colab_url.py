import sys
import os
import glob
import re
import socket
import sqlite3
import shutil
from urllib.parse import urlparse, parse_qs

def is_port_listening(port: int) -> bool:
    """Verifies whether the target local port is currently active and accepting connections."""
    try:
        with socket.create_connection(('127.0.0.1', int(port)), timeout=0.5):
            return True
    except (ConnectionRefusedError, socket.timeout, OSError):
        return False

def get_latest_bridge_token_and_port():
    """Finds the most recent mcpProxyToken and mcpProxyPort from browser history."""
    search_patterns = [
        # Windows
        os.path.expanduser('~') + '/AppData/Local/Google/Chrome/User Data/*/History',
        os.path.expanduser('~') + '/AppData/Local/Microsoft/Edge/User Data/*/History',
        # macOS
        os.path.expanduser('~') + '/Library/Application Support/Google/Chrome/*/History',
        os.path.expanduser('~') + '/Library/Application Support/Microsoft Edge/*/History',
        # Linux
        os.path.expanduser('~') + '/.config/google-chrome/*/History',
        os.path.expanduser('~') + '/.config/chromium/*/History',
    ]

    history_files = []
    for pattern in search_patterns:
        history_files.extend(glob.glob(pattern))

    for hf in history_files:
        tmp = hf + f".tmp_{os.getpid()}"
        try:
            shutil.copy2(hf, tmp)
            conn = sqlite3.connect(tmp)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT url FROM urls WHERE url LIKE '%mcpProxyToken%' ORDER BY last_visit_time DESC LIMIT 1"
            )
            row = cursor.fetchone()
            conn.close()
            if row:
                url = row[0]
                token_match = re.search(r'mcpProxyToken=([A-Za-z0-9_-]+)', url)
                port_match = re.search(r'mcpProxyPort=(\d+)', url)
                if token_match and port_match:
                    return token_match.group(1), port_match.group(1)
        except Exception:
            pass
        finally:
            if os.path.exists(tmp):
                try:
                    os.remove(tmp)
                except Exception:
                    pass

    return None, None

def make_colab_bridge_url(notebook_url: str) -> str:
    token, port = get_latest_bridge_token_and_port()
    if not token or not port:
        return notebook_url

    # Strip existing hash if present
    base_url = notebook_url.split('#')[0]
    return f"{base_url}#mcpProxyToken={token}&mcpProxyPort={port}"

def check_status():
    token, port = get_latest_bridge_token_and_port()
    if not port or not token:
        print("[STATUS] No recent Colab MCP session token found in browser history.")
        return False

    listening = is_port_listening(int(port))
    if listening:
        print(f"[STATUS] 🟢 Colab MCP Server is LIVE and listening on port {port} (token: {token[:6]}...).")
        return True
    else:
        print(f"[STATUS] 🔴 Colab MCP port {port} is NOT responding (server may have restarted or stopped).")
        return False

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--check':
        check_status()
    else:
        target = sys.argv[1] if len(sys.argv) > 1 else "https://colab.research.google.com/notebooks/empty.ipynb"
        print(make_colab_bridge_url(target))
