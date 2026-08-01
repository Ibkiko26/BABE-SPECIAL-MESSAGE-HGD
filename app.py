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
  # Build a 4-row marquee gallery. Each row scrolls in alternating directions.
  def make_row(imgs, row_index):
    if not imgs:
      imgs = images
    cards = ''.join(f'<div class="photo-frame"><img src="{img}" alt="Maureen"></div>' for img in imgs)
    # duplicate for seamless scroll
    track = cards + cards
    direction = 'track-left' if row_index % 2 == 0 else 'track-right'
    duration = 60 + (row_index * 8)  # slight variation per row
    return f'<div class="row"><div class="track {direction}" style="--dur:{duration}s">{track}</div></div>'

  # distribute images across 4 rows round-robin
  rows = []
  for r in range(4):
    row_imgs = images[r::4]
    rows.append(make_row(row_imgs, r))

  marquee = '\n'.join(rows)

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
      <h1>Happy Girlfriend's Day, My love! <span class="title-emoji">💖</span></h1>
      <div class="sparkles">
        <span class="spark">✨</span>
        <span class="spark">✨</span>
        <span class="spark">✨</span>
        <span class="spark">✨</span>
      </div>
    </header>

    <section class="marquee">
      {marquee}
    </section>

    <section class="message-card">
      <div class="message-hearts" aria-hidden="true">
        <span>💗</span><span>💖</span><span>💘</span><span>💝</span>
      </div>
      <p class="intro">To my amazing love,</p>
      <p>On this Girlfriend's Day I celebrate you — your heart, your courage, and the beautiful future you are building. I wish you boundless happiness, unshakable good health, and a real financial breakthrough that opens new doors and brings peace of mind.</p>
      <p>I want to specially commend your hard work and determination in completing your Diploma in Health Records final exams. That milestone is the result of late nights, focus, and steady perseverance — I am so proud of how far you've come.</p>
      <p>As you step into the corporate world, I wish you every success and smooth transitions. May you find opportunities that match your talent, mentors who champion you, and the confidence to thrive. Good luck — I know you will shine.</p>

      <p class="with-love">With all my love and pride,</p>
      <p class="signature">Ibrahim Koros — Your Boyfriend</p>
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