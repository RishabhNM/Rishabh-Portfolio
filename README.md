# Rishabh's portfolio site

```
portfolio/
├── index.html   ← the design (you don't need to touch this)
├── site.yaml    ← ALL your text, projects and links: edit this
├── files/       ← your Resume and CV PDFs (the download buttons)
└── images/      ← optional game screenshots / icons
```

## Editing
1. Open `site.yaml` in VS Code and change what you like. The top of the file explains the rules.
2. Save, then refresh the page.

- **Add a project:** copy a project block (from `- title:` down to its links), paste it, change the text.
- **Big card vs. list:** `featured: true` puts a project in the big "Selected work" cards.
- **Add an image to a card:** put `cozy-words.png` in `images/`, then in that project write `image: images/cozy-words.png`.
- **Update your Resume / CV:** replace the PDFs in `files/` (keep the same names).
- **Colours and fonts:** at the top of `index.html`, inside `:root { ... }`.

## Previewing on your computer
Double-clicking `index.html` won't load `site.yaml` (browsers block that for local files).
Instead, open cmd in this folder and run:
```
python -m http.server
```
Then open http://localhost:8000 in your browser. Press Ctrl + C to stop.

## Putting it online (free)
**Netlify (easiest):** go to https://app.netlify.com/drop and drag the whole `portfolio` folder onto the page.
You get a link straight away. To update, drag the folder again (or connect it to GitHub).

**GitHub Pages:** create a repository, upload everything in this folder, then go to
Settings > Pages > Deploy from branch > `main` / root. Your site appears at `https://<username>.github.io/<repo>`.

Both let you connect your own domain later.
