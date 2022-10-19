const { series } = require('gulp');
const { js } = require('./js');
const { css } = require('./css');
const { svg } = require('./svg');

exports.build = series(js, css, svg);
exports.default = series(js, css, svg);
exports.svg = svg;
exports.js = js;
exports.css = css;
