#!/usr/bin/env python3
"""
Enhanced Markdown Server with Beautiful Styling
Serves markdown files with GitHub-like styling and syntax highlighting
"""

import http.server
import socketserver
import markdown
import os
import sys
from urllib.parse import unquote
from pathlib import Path

class MarkdownHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Parse the path
        path = unquote(self.path)
        
        # Remove query parameters
        if '?' in path:
            path = path.split('?')[0]
        
        # Default to IMPLEMENTATION.md if accessing root
        if path == '/':
            path = '/IMPLEMENTATION_GUIDE.md'
        
        # Remove leading slash
        if path.startswith('/'):
            path = path[1:]
        
        # Check if it's a markdown file
        if path.endswith('.md'):
            try:
                # Read markdown file
                with open(path, 'r', encoding='utf-8') as f:
                    markdown_content = f.read()
                
                # Process Mermaid code blocks before markdown conversion
                markdown_content = self.process_mermaid_blocks(markdown_content)
                
                # Configure markdown with extensions
                md = markdown.Markdown(extensions=[
                    'markdown.extensions.codehilite',
                    'markdown.extensions.fenced_code',
                    'markdown.extensions.tables',
                    'markdown.extensions.toc',
                    'markdown.extensions.nl2br',
                ])
                
                # Convert to HTML
                html_content = md.convert(markdown_content)
                
                # Create full HTML page with styling
                full_html = self.create_html_page(html_content, path)
                
                # Send response
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', str(len(full_html.encode('utf-8'))))
                self.end_headers()
                self.wfile.write(full_html.encode('utf-8'))
                
            except FileNotFoundError:
                self.send_error(404, f"File not found: {path}")
            except Exception as e:
                self.send_error(500, f"Error processing markdown: {str(e)}")
        else:
            # Serve other files normally
            super().do_GET()
    
    def process_mermaid_blocks(self, content):
        """Convert mermaid code blocks to HTML divs with mermaid class"""
        import re
        
        # Pattern to match mermaid code blocks
        pattern = r'```mermaid\n(.*?)\n```'
        
        def replace_mermaid(match):
            mermaid_code = match.group(1)
            return f'<div class="mermaid">\n{mermaid_code}\n</div>'
        
        # Replace all mermaid code blocks
        return re.sub(pattern, replace_mermaid, content, flags=re.DOTALL)
    
    def create_html_page(self, content, title):
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js"></script>
    <style>
        /* GitHub-like styling */
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif;
            font-size: 16px;
            line-height: 1.5;
            color: #24292f;
            background-color: #ffffff;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            margin-top: 24px;
            margin-bottom: 16px;
            font-weight: 600;
            line-height: 1.25;
        }}
        
        h1 {{
            font-size: 2em;
            padding-bottom: 0.3em;
            border-bottom: 1px solid #d0d7deff;
        }}
        
        h2 {{
            font-size: 1.5em;
            padding-bottom: 0.3em;
            border-bottom: 1px solid #d0d7deff;
        }}
        
        h3 {{
            font-size: 1.25em;
        }}
        
        code {{
            padding: 0.2em 0.4em;
            margin: 0;
            font-size: 85%;
            background-color: rgba(175, 184, 193, 0.2);
            border-radius: 6px;
            font-family: ui-monospace, SFMono-Regular, 'SF Mono', Consolas, 'Liberation Mono', Menlo, monospace;
        }}
        
        pre {{
            padding: 16px;
            overflow: auto;
            font-size: 85%;
            line-height: 1.45;
            background-color: #f6f8fa;
            border-radius: 6px;
            border: 1px solid #d0d7de;
        }}
        
        pre code {{
            background-color: transparent;
            border: 0;
            display: inline;
            line-height: inherit;
            margin: 0;
            overflow: visible;
            padding: 0;
            word-wrap: normal;
        }}
        
        table {{
            border-spacing: 0;
            border-collapse: collapse;
            width: 100%;
            margin-bottom: 16px;
        }}
        
        table th, table td {{
            padding: 6px 13px;
            border: 1px solid #d0d7de;
        }}
        
        table th {{
            background-color: #f6f8fa;
            font-weight: 600;
        }}
        
        table tr:nth-child(2n) {{
            background-color: #f6f8fa;
        }}
        
        blockquote {{
            padding: 0 1em;
            color: #656d76;
            border-left: 0.25em solid #d0d7de;
            margin: 0 0 16px 0;
        }}
        
        ul, ol {{
            padding-left: 2em;
            margin-bottom: 16px;
        }}
        
        li {{
            margin: 0.25em 0;
        }}
        
        hr {{
            height: 0.25em;
            padding: 0;
            margin: 24px 0;
            background-color: #d0d7de;
            border: 0;
        }}
        
        .highlight {{
            background: #f8f8f8;
            border: 1px solid #ccc;
            border-radius: 4px;
            padding: 10px;
            overflow-x: auto;
        }}
        
        /* Success indicators */
        body {{
            counter-reset: checkmark;
        }}
        
        p:has(✅)::before {{
            content: "✅ ";
            color: #28a745;
        }}
        
        /* Navigation */
        .nav {{
            background: #f6f8fa;
            padding: 10px 20px;
            margin: -20px -20px 20px -20px;
            border-bottom: 1px solid #d0d7de;
            position: sticky;
            top: 0;
            z-index: 100;
        }}
        
        .nav h1 {{
            margin: 0;
            font-size: 1.2em;
            border: none;
            padding: 0;
        }}
        
        /* Responsive */
        @media (max-width: 768px) {{
            body {{
                padding: 10px;
            }}
            .nav {{
                margin: -10px -10px 10px -10px;
            }}
        }}
    </style>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
    <script>hljs.highlightAll();</script>
</head>
<body>
    <div class="nav">
        <h1>📚 GitOps Implementation Documentation</h1>
        <p style="margin: 5px 0 0 0; color: #656d76; font-size: 14px;">
            🚀 Complete implementation guide with ArgoCD and Kustomize | 
            <a href="/">Implementation Doc</a> | 
            <a href="/README.md">Project README</a>
        </p>
    </div>
    {content}
    <footer style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #d0d7de; text-align: center; color: #656d76;">
        <p>📖 Served by Python Markdown Server | 🎯 GitOps Implementation Complete</p>
    </footer>
    <script>
        // Initialize Mermaid
        mermaid.initialize({{ 
            startOnLoad: true,
            theme: 'base',
            themeVariables: {{
                primaryColor: '#0969da',
                primaryTextColor: '#24292f',
                primaryBorderColor: '#1f2328',
                lineColor: '#656d76',
                secondaryColor: '#f6f8fa',
                tertiaryColor: '#ffffff',
                background: '#ffffff',
                mainBkg: '#f6f8fa',
                secondBkg: '#ffffff',
                tertiaryTextColor: '#24292f'
            }},
            flowchart: {{
                useMaxWidth: true,
                htmlLabels: true,
                curve: 'basis'
            }},
            sequence: {{
                diagramMarginX: 50,
                diagramMarginY: 10,
                actorMargin: 50,
                width: 150,
                height: 65,
                boxMargin: 10,
                boxTextMargin: 5,
                noteMargin: 10,
                messageMargin: 35
            }},
            pie: {{
                textPosition: 0.75
            }}
        }});
        
        // Process any existing mermaid diagrams
        mermaid.run();
        
        // Style mermaid containers
        document.addEventListener('DOMContentLoaded', function() {{
            const mermaidElements = document.querySelectorAll('.mermaid');
            mermaidElements.forEach(element => {{
                element.style.textAlign = 'center';
                element.style.background = '#ffffff';
                element.style.border = '1px solid #d0d7de';
                element.style.borderRadius = '6px';
                element.style.padding = '16px';
                element.style.margin = '16px 0';
                element.style.boxShadow = '0 1px 3px rgba(0,0,0,0.1)';
            }});
        }});
    </script>
</body>
</html>"""

def main():
    port = 8000
    
    # Check if IMPLEMENTATION.md exists
    if not os.path.exists('IMPLEMENTATION.md'):
        print("❌ Error: IMPLEMENTATION.md not found in current directory")
        print("📂 Current directory:", os.getcwd())
        print("📄 Available files:", os.listdir('.'))
        sys.exit(1)
    
    try:
        with socketserver.TCPServer(("", port), MarkdownHandler) as httpd:
            print("🚀 Starting Enhanced Markdown Server...")
            print(f"📖 Serving documentation at: http://localhost:{port}")
            print(f"📂 Current directory: {os.getcwd()}")
            print("📄 Available at:")
            print(f"   • Implementation Guide: http://localhost:{port}/")
            print(f"   • Project README: http://localhost:{port}/README.md")
            print("🛑 Press Ctrl+C to stop the server")
            print("-" * 60)
            
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except OSError as e:
        print(f"❌ Error starting server: {e}")
        if "Address already in use" in str(e):
            print(f"💡 Port {port} is already in use. Try a different port or stop the existing server.")

if __name__ == "__main__":
    main()