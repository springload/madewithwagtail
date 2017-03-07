
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
        let tagsButton = document.querySelector('[data-toggle]');
        let tags = document.querySelectorAll('[data-tag]');
        let tagsContainer = document.querySelector('[data-tags-container]');

        if (tagsButton) {
            tagsButton.addEventListener('click', () => {
                tags.forEach(tag => {
                    tag.classList.toggle('u-hide');
                });
                tagsContainer.classList.toggle('tags__additional--show')
                tagsButton.innerHTML === 'Show More' ? tagsButton.innerHTML = 'Show Less' : tagsButton.innerHTML = 'Show More';
            });
        }
    }
}

window.site = new Site({ });
