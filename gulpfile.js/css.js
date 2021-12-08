const { series, src, dest } = require('gulp');
const path = require('path');

const sass = require('gulp-sass')(require('sass'));
const plz = require('gulp-pleeease');
const gutil = require('gulp-util');
const size = require('gulp-size');
const bs = require('browser-sync').create('css');
const sourcemaps = require('gulp-sourcemaps');

const config = require('./config');

/*
 ---------------------------------------------------------------------------
 Stylesheets
 ---------------------------------------------------------------------------
 */

function css() {
    return src(path.join(config.paths.sass, '**', '*.scss'))
        .pipe(config.prod ? gutil.noop() : sourcemaps.init())
        .pipe(sass())
        .on('error', function handleError(err) {
            gutil.log(err.message);
            bs.notify(err.message, 10000);
            this.emit('end');
        })
        .pipe(plz(config.PleeeaseOptions))
        .pipe(config.prod ? gutil.noop() : sourcemaps.write())
        .pipe(
            size({
                title: config.prod ? 'CSS' : 'CSS (unminified)',
                showFiles: true,
                gzip: config.prod,
            }),
        )
        .pipe(dest(path.join(config.paths.assets, 'css')))
        .pipe(bs.stream());
}

exports.css = series(css);
