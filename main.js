import Reveal from 'reveal.js';
import RevealMarkdown from 'reveal.js/plugin/markdown';
import RevealHighlight from 'reveal.js/plugin/highlight';
import RevealNotes from 'reveal.js/plugin/notes';

import 'reveal.js/reset.css';
import 'reveal.js/reveal.css';
import 'reveal.js/plugin/highlight/monokai.css';
import 'reveal.js-conda-theme/conda.css';

import condaIconUrl from 'reveal.js-conda-theme/assets/conda_c.svg';
import condaWordmarkUrl from 'reveal.js-conda-theme/assets/conda_logo.svg';

document.querySelector('link[rel="icon"]')?.setAttribute('href', condaIconUrl);
document.querySelector('img.wordmark')?.setAttribute('src', condaWordmarkUrl);

// More info about initialization & config:
// - https://revealjs.com/initialization/
// - https://revealjs.com/config/
Reveal.initialize({
	hash: true,

	// Learn about plugins: https://revealjs.com/plugins/
	plugins: [RevealMarkdown, RevealHighlight, RevealNotes],
});
