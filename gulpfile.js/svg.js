const { series, dest, src } = require('gulp');
const svgstore = require('gulp-svgstore');
const svgmin = require('gulp-svgmin');
const path = require('path');
const rename = require('gulp-rename');
const config = require('./config');

function svg() {
    return src(path.join(config.paths.svg, '**', '*.svg'))
        .pipe(rename({ prefix: 'i-' }))
        .pipe(svgmin())
        .pipe(svgstore({ inlineSvg: true }))
        .pipe(rename('svg.html'))
        .pipe(dest(path.join(config.paths.templates, 'core', 'includes')));
}

exports.svg = series(svg);
