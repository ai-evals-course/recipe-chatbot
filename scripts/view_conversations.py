from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from rich.console import Console

RESULTS_DIR: Path = Path("results")


def create_conversations_viewer(results_path: Path) -> None:
    """Creates a paginated HTML viewer for conversations."""
    if not results_path.exists():
        raise FileNotFoundError(f"Results file not found at: {results_path}")

    with results_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        conversations = list(reader)

    if not conversations:
        Console().print("[yellow]No conversations found in the results file.[/yellow]")
        return

    html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Conversation Viewer</title>
    <style>
        body {{ font-family: sans-serif; margin: 2em; background-color: #f4f4f9; color: #333; }}
        .container {{ max-width: 800px; margin: auto; background: white; padding: 1em; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
        .conversation {{ border: 1px solid #ddd; padding: 1em; margin-bottom: 1em; border-radius: 8px; }}
        .message {{ margin-bottom: 0.5em; padding: 0.5em; border-radius: 5px; }}
        .user {{ background-color: #e1f5fe; border-left: 3px solid #0288d1; }}
        .assistant {{ background-color: #e8f5e9; border-left: 3px solid #4caf50; }}
        .system {{ background-color: #fbe9e7; border-left: 3px solid #d84315; }}
        .pagination {{ text-align: center; margin: 1em 0; }}
        .pagination a {{ margin: 0 5px; text-decoration: none; color: #0288d1; padding: 8px 12px; border: 1px solid #ddd; border-radius: 4px; }}
        .pagination a.active {{ background-color: #0288d1; color: white; }}
        pre, code {{ white-space: pre-wrap; word-wrap: break-word; }}
        h1, h2, h3 {{ color: #333; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Conversation Viewer</h1>
        <div id="conversation-container"></div>
        <div class="pagination" id="pagination-links"></div>
    </div>

    <script>
        const conversations = {conversations_json};
        const itemsPerPage = 1;
        let currentPage = 1;

        function displayConversation() {{
            const container = document.getElementById('conversation-container');
            container.innerHTML = '';
            const conversationData = conversations[currentPage - 1];
            
            const conversationDiv = document.createElement('div');
            conversationDiv.className = 'conversation';
            
            const idHeader = document.createElement('h2');
            idHeader.textContent = `Conversation ID: ${{conversationData.id}}`;
            conversationDiv.appendChild(idHeader);

            const history = JSON.parse(conversationData.conversation_history);
            history.forEach(msg => {{
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${{msg.role}}`;
                
                const roleStrong = document.createElement('strong');
                roleStrong.textContent = `${{msg.role.charAt(0).toUpperCase() + msg.role.slice(1)}}:`;
                
                messageDiv.appendChild(roleStrong);
                messageDiv.appendChild(document.createElement('br'));
                
                // Naive check for markdown-like content to render
                const contentDiv = document.createElement('div');
                contentDiv.innerHTML = msg.content.replace(/\\n/g, '<br>'); // A simple replacement for newlines
                messageDiv.appendChild(contentDiv);

                conversationDiv.appendChild(messageDiv);
            }});

            container.appendChild(conversationDiv);
            updatePagination();
        }}

        function updatePagination() {{
            const paginationContainer = document.getElementById('pagination-links');
            paginationContainer.innerHTML = '';
            const totalPages = conversations.length;

            for (let i = 1; i <= totalPages; i++) {{
                const link = document.createElement('a');
                link.href = '#';
                link.textContent = i;
                if (i === currentPage) {{
                    link.className = 'active';
                }}
                link.onclick = (e) => {{
                    e.preventDefault();
                    currentPage = i;
                    displayConversation();
                }};
                paginationContainer.appendChild(link);
            }}
        }}

        displayConversation();
    </script>
</body>
</html>
    """

    # Prepare data for embedding into the template
    conversations_json = json.dumps(
        [
            {
                "id": c.get("id", "N/A"),
                "conversation_history": c.get("conversation_history", "[]"),
            }
            for c in conversations
        ]
    )
    html_content = html_template.format(conversations_json=conversations_json)

    viewer_path = results_path.parent / f"viewer_{results_path.stem}.html"
    with viewer_path.open("w", encoding="utf-8") as f:
        f.write(html_content)

    Console().print(
        f"[bold green]Created conversation viewer at: {viewer_path}[/bold green]"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="View conversation results.")
    parser.add_argument(
        "results_csv",
        type=Path,
        help="Path to the results CSV file from a bulk test run.",
    )
    args = parser.parse_args()
    create_conversations_viewer(args.results_csv) 