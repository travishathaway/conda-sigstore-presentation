# conda reveal.js starter kit

A starter kit for creating conda themed [reveal.js](https://revealjs.com) presentations
using the [`reveal.js-conda-theme`](../reveal.js-conda-theme) package.

`index.html` contains one example of each slide template: title, single column, two
columns, dark, and light. See [reveal.js-conda-theme's README](../reveal.js-conda-theme/README.md#markup-conventions)
for the markup conventions each template relies on.

## Getting started

Copy this folder out as the seed for your own presentation repo, then:

```bash
npm install
npm start          # serves index.html with live reload
```

To build a static, deployable version of the presentation:

```bash
npm run build      # outputs to dist/
```

## How it's wired up

- `package.json` depends on `reveal.js` and `reveal.js-conda-theme` — both installed
  from npm, no vendored/forked source.
- `main.js` imports reveal.js core, the notes/highlight/markdown plugins, and the
  conda theme's CSS, then calls `Reveal.initialize(...)`.
- `index.html` is plain reveal.js markup; Vite bundles `main.js` and its CSS/asset
  imports for you.

## Credits

Built on [reveal.js](https://github.com/hakimel/reveal.js) by Hakim El Hattab and
contributors, MIT licensed.
