
import GA from 'springload-analytics.js';

if ('ontouchstart' in window) {
    document.documentElement.className = document.documentElement.className + ' touch';
} else {
    document.documentElement.className = document.documentElement.className + ' no-touch';
}

class Site {
    constructor() {
        GA.init();
    }
}

window.site = new Site({ });
