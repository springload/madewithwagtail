
import GA from 'springload-analytics.js';

import tagsToggle from './components/tagsToggle';

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
        tagsToggle.init();

        if ('info' in console) {
            console.info(message);
        }
    }
}

window.site = new Site({ });
