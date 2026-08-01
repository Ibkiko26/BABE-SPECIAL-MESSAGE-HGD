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
    cards = "".join(
        f'<div class="photo-card"><img src="{image}" alt="Maureen portrait"></div>'
        for image in images
    )
    gallery_markup = cards + cards
    return f'''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Happy Girlfriends Day, My love</title>
    <link rel="stylesheet" href="style.css" />
  </head>
  <body>
    <div class="hearts">
      <span>💖</span><span>💗</span><span>💘</span><span>💝</span>
    </div>

    <main class="container">
      <section class="hero-card">
        <p class="eyebrow">A sweet tribute for my lovely girl</p>
        <h1>Happy Girlfriends Day, My love 💖💗</h1>
        <p class="message">
          My beautiful love, I just want to remind you how much I admire your grace,
          strength, and beautiful heart. May this day bring you endless joy, good health,
          and a beautiful flow of financial breakthrough. Your hard work and dedication have
          been inspiring, especially as you completed your Diploma in Health Records final exams.
          I am so proud of your perseverance and the way you keep pushing forward. 💕
        </p>
        <p class="message">
          As you step into the corporate world, I wish you the very best, all the luck in the world,
          and a future filled with success, peace, and happiness. Keep shining, my love. 💘✨
        </p>
        <p class="signature">With love and admiration, Ibrahim Koros 💕</p>
      </section>

      <section class="gallery-card">
        <div class="gallery-heading">
          <h2>A little gallery of your beauty</h2>
          <p>Every picture carries a smile, and every smile reminds me of your lovely spirit.</p>
        </div>
        <div class="gallery-shell">
          <div class="heart-splash heart-splash-a">💗</div>
          <div class="heart-splash heart-splash-b">💖</div>
          <div class="heart-splash heart-splash-c">💘</div>
          <div class="gallery-track">
            {gallery_markup}
          </div>
        </div>
      </section>
    </main>
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
        print("Opening the celebration page for Maureen...")
        webbrowser.open(f'http://localhost:{PORT}')
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
            httpd.server_close()