from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

ROOT = Path(__file__).resolve().parent


def discover_images():
    extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tif', '.tiff'}
    files = []
    for path in ROOT.iterdir():
        if path.is_file() and path.suffix.lower() in extensions:
            files.append(path.name)
    return sorted(files)


def build_html(images):
    cards = []
    for index, image in enumerate(images, start=1):
        cards.append(
            f'<div class="photo-card"><img src="{image}" alt="Maureen portrait {index}"></div>'
        )
    gallery_items = cards + cards
    gallery = "\n".join(gallery_items)
    return f'''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Happy Girlfriends Day, Maureen</title>
    <link rel="stylesheet" href="style.css" />
  </head>
  <body>
    <div class="hearts">
      <span>💖</span><span>💗</span><span>💘</span><span>💝</span>
    </div>

    <main class="container">
      <section class="hero-card">
        <p class="eyebrow">A sweet message for my lovely girl</p>
        <h1>Happy Girlfriends Day, Maureen Mbete Musau</h1>
        <p class="message">
          My beautiful Maureen, I just want to remind you how much I admire your grace,
          strength, and beautiful heart. May this day bring you endless joy, good health,
          and a beautiful flow of financial breakthrough. Your hard work and dedication have
          been inspiring, especially as you completed your Diploma in Health Records final exams.
          I am proud of your perseverance and the way you keep pushing forward.
        </p>
        <p class="message">
          As you step into the corporate world, I wish you the very best, all the luck in the world,
          and a future filled with success, peace, and happiness. Keep shining, my love.
        </p>
        <p class="signature">With love and admiration, Ibrahim Koros</p>
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
            {gallery}
          </div>
        </div>
      </section>
    </main>
  </body>
</html>
'''


def write_page():
    html = build_html(discover_images())
    (ROOT / 'index.html').write_text(html, encoding='utf-8')


class QuietHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)


if __name__ == '__main__':
    write_page()
    port = 8000
    httpd = ThreadingHTTPServer(('0.0.0.0', port), QuietHandler)
    print(f'Serving at http://localhost:{port}')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\nServer stopped.')
