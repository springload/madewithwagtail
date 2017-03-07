
import GA from 'springload-analytics.js';

if ('ontouchstart' in window) {
    document.documentElement.className = document.documentElement.className + ' touch';
} else {
    document.documentElement.className = document.documentElement.className + ' no-touch';
}

const message = `
[ SPRINGLOAD ]
Want to ship things that matter, at scale? Springloaders work on sites and apps with more than 54 million sessions/year.
You could join our cross-functional dev team and work on challenging projects in Python, Node and ReactJS.
Send your CV to apply@springload.co.nz, or better yet, send us a pull request: https://github.com/springload
`;

class Site {
    constructor() {
        GA.init();
        this.initTags();

        if ('info' in console) {
            console.info(message);
        }
    }

    initTags() {
        const tagsToggle = document.querySelector('[data-tags-toggle]');
        const tagsContainer = document.querySelector('[data-tags-additional]');

        const toggleTags = () => {
            const wasVisible = JSON.parse(tagsToggle.getAttribute('aria-expanded'));
            const isVisible = !wasVisible;
            tagsToggle.setAttribute('aria-expanded', isVisible);
            tagsContainer.setAttribute('aria-hidden', !isVisible);

            // First toggle hide/show in the inner element, then toggle the animation.
            tagsContainer.children[0].classList.toggle('u-hide', !isVisible);
            tagsContainer.classList.toggle('tags__additional--show', isVisible)
            tagsToggle.innerHTML = isVisible ? 'Show fewer tags' : 'Show more tags';
        };

        if (tagsToggle) {
            tagsToggle.addEventListener('click', toggleTags);
        }
    }
}

window.site = new Site({ });
