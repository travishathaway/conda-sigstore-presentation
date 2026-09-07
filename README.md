# Signing Conda Packages with Sigstore

A [reveal.js](https://revealjs.com) presentation about Sigstore's use in conda —
covering Sigstore basics, Fulcio, Rekor, and in-toto attestations, a cosign signing/
verification demo, PyPI's adoption of package attestations, and conda's own CEP 
proposals for signing and verifying packages.

Built with the [`reveal.js-conda-theme`](https://www.npmjs.com/package/reveal.js-conda-theme)
package. See its README (bundled at `node_modules/reveal.js-conda-theme/README.md`)
for the markup conventions used in `index.html` (title, single column, two columns,
dark, and light slide templates).

## Getting started

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
