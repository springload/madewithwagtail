'use strict';

/*
 * Grabs screenshots from a URL using SlimerJS(/PhantomJS).
 * To run on a single site: slimerjs-screenshot.js http://example.com
 * To run on a list of sites: while read line; do slimerjs slimerjs-screenshot.js "$line"; done < wagtail-sites-urls.txt
 *
 * Then, to optimize all of the screenshots: pngquant --ext=.png --force *.png
 * Finally, run them through ImageOptim.
 *
 * Caveats: SlimerJS does not support HTTPS, PhantomJS does not support web fonts & has a very old rendering engine.
 */

var page = require('webpage').create();

var url = phantom.args[phantom.args.length - 1];
var parser = document.createElement('a');
parser.href = url;
var domain = parser.hostname;

var opts = {
    viewports: [
        [320, 1200],
        [768, 1200],
        [1440, 1200]
    ],
    scales: [1, 2],
    loadDelay: 8,
    resizeDelay: 3
};

function captureScreenshots() {
    var index = 0;
    opts.viewports.forEach(function(viewport, viewportIndex) {
        opts.scales.forEach(function(scale, scaleIndex) {
            index++;
            window.setTimeout(function() {

                shoot(domain, viewport[0], viewport[1], scale);

            }, index * opts.resizeDelay * 1000);
        });
    });
}

function shoot(domain, width, height, scale, index) {
    var filename = domain + '-' + width + 'x' + height + '-@' + scale + 'x.png';

    page.zoomFactor = scale;

    page.viewportSize = {
        width: width * scale,
        height: height * scale
    };

    page.clipRect = {
        top: 0,
        left: 0,
        width: width * scale,
        height: height * scale
    };

    page.render('shots/' + filename);
    console.log('Rendering ' + filename);

    if (width === opts.viewports[opts.viewports.length - 1][0] && scale === opts.scales[opts.scales.length - 1]) {
        page.close();
        phantom.exit();
    }
}

page.open(url)
    .then(function(status){
        if (status === 'success') {
            window.setTimeout(function() {
                captureScreenshots();
            }, opts.loadDelay * 1000);
        }
        else {
            console.error('Couldn\'t load url: ' + url);
            phantom.exit();
            return;
        }
});
