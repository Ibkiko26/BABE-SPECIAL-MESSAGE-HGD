import http.server
import os
import socketserver
import webbrowser
from pathlib import Path
import http.server
import os
import socketserver
import webbrowser
from pathlib import Path

PORT = 8000
ROOT = Path(__file__).resolve().parent


def discover_images():
    allowed = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tif', '.tiff'}
    files = [p.name for p in ROOT.iterdir() if p.is_file() and p.suffix.lower() in allowed]
    return sorted(files, key=lambda name: name.lower())


def build_html(images):
    # Build a gallery matching the screenshot layout
    cards = []
    for img in images:
        cards.append(f'<div class="photo-frame"><img src="{img}" alt="Maureen"></div>')
    gallery = '\n'.join(cards)

    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Happy Girlfriend's Day</title>
  <link href="https://fonts.googleapis.com/css2?family=Great+Vibes&family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <div class="page">
    <header class="hero">
      <h1>Happy Girlfriend's Day, My love!</h1>
      <div class="hero-heart">💖</div>
    </header>

    <section class="gallery">
      {gallery}
    </section>

    <section class="message-card">
      <p class="intro">To my amazing love,</p>
      <p>On this Girlfriend's Day, I just wanted to take a moment to celebrate you. I wish you nothing but endless happiness, radiant good health, and massive financial breakthroughs in everything you do.</p>
      <p>I am so incredibly proud of your hard work. It takes immense courage and dedication to step completely out of your comfort zone and move to a whole new continent. You did that to change your life and uplift your family, and watching you push forward is truly inspiring.</p>
      <p>Keep shining, keep grinding, and know that I am always cheering you on.</p>

      <p class="with-love">With all my love,</p>
      <p class="signature">Your Boyfriend, Ibrahim Koros</p>
    </section>
  </div>
</body>
</html>
'''


def write_index_html():
    (ROOT / 'index.html').write_text(build_html(discover_images()), encoding='utf-8')


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)


if __name__ == '__main__':
    write_index_html()
    os.chdir(ROOT)
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Server started at http://localhost:{PORT}")
        webbrowser.open(f'http://localhost:{PORT}')
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
            httpd.server_close()
    write_index_html()
    os.chdir(ROOT)
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Server started at http://localhost:{PORT}")
        print("Opening the celebration page for Maureen...")
        webbrowser.open(f'http://localhost:{PORT}')
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
            httpd.server_close()