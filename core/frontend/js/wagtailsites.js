
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
        const tagsButton = document.querySelector('[data-toggle]');
        const tags = document.querySelectorAll('[data-tag]');
        const tagsContainer = document.querySelector('[data-tags-container]');

        if (tagsButton) {
            tagsButton.addEventListener('click', () => {
                tags.forEach((tag) => {
                    tag.classList.toggle('u-hide');
                });
                tagsContainer.classList.toggle('tags__additional--show')
                tagsButton.innerHTML = tagsButton.innerHTML === 'Show more tags' ? 'Show fewer tags' : 'Show more tags';
            });
        }
    }
}

window.site = new Site({ });
