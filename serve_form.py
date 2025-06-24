#!/usr/bin/env python3
"""
Simple HTTP server to serve the business input form
"""

import http.server
import socketserver
import webbrowser
import os
from pathlib import Path

PORT = 8080


class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()


def main():
    # Change to the directory containing this script
    os.chdir(Path(__file__).parent)

    # Check if the HTML file exists
    if not os.path.exists("business_input_form.html"):
        print("❌ business_input_form.html not found!")
        print("Please make sure the file exists in the current directory.")
        return

    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"🌐 Starting HTTP server on port {PORT}")
        print(
            f"📄 Serving business input form at: http://localhost:{PORT}/business_input_form.html"
        )
        print("🔗 Opening browser automatically...")

        # Open the browser
        webbrowser.open(f"http://localhost:{PORT}/business_input_form.html")

        print("\n⏹️  Press Ctrl+C to stop the server")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped")


if __name__ == "__main__":
    main()
