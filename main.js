import Reveal from 'reveal.js';
import RevealMarkdown from 'reveal.js/plugin/markdown';
import RevealHighlight from 'reveal.js/plugin/highlight';
import RevealNotes from 'reveal.js/plugin/notes';

import 'reveal.js/reset.css';
import 'reveal.js/reveal.css';
// The theme maps highlight.js tokens itself - no separate highlight.js stylesheet needed.
import 'reveal.js-conda-theme/conda.css';

import condaIconUrl from 'reveal.js-conda-theme/assets/conda_c.svg';
import condaLogoUrl from 'reveal.js-conda-theme/assets/conda_logo.svg';

document.querySelector('link[rel="icon"]')?.setAttribute('href', condaIconUrl);
for (const logo of document.querySelectorAll('img.conda-logo')) {
	logo.setAttribute('src', condaLogoUrl);
}

// More info about initialization & config:
// - https://revealjs.com/initialization/
// - https://revealjs.com/config/
Reveal.initialize({
	// The conda theme positions slide content with padding and is tuned for
	// a 1280x720 canvas. `center: false` and `margin: 0` are required.
	width: 1280,
	height: 720,
	margin: 0,
	center: false,
	minScale: 0.2,
	maxScale: 2.0,

	hash: true,
	slideNumber: 'c/t',
	transition: 'fade',
	transitionSpeed: 'fast',
	backgroundTransition: 'fade',

	// Learn about plugins: https://revealjs.com/plugins/
	plugins: [RevealMarkdown, RevealHighlight, RevealNotes],
});
