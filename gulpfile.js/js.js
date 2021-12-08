const { series, dest } = require('gulp');
const path = require('path');
const browserify = require('browserify');
const browserifyInc = require('browserify-incremental');
const uglify = require('gulp-uglify');
const buffer = require('vinyl-buffer');
const gutil = require('gulp-util');
const size = require('gulp-size');
const source = require('vinyl-source-stream');
const bs = require('browser-sync').create('js');
const config = require('./config');

const browserifyInstance = config.prod ? browserify : browserifyInc;

const bundler = browserifyInstance({
    cache: {},
    // transform: [babelify],
    packageCache: {},
    debug: !config.prod,
    fullPaths: !config.prod,
}).transform('babelify', { presets: ['es2015'], global: true });
// });

bundler.add(path.resolve(config.paths.js, config.paths.appName));

function js() {
    return bundler
        .bundle()
        .on('error', function handleError(err) {
            gutil.log(err.message);
            bs.notify(err.message, 10000);
            this.emit('end');
        })
        .pipe(source(config.paths.appName))
        .pipe(buffer())
        .pipe(config.prod ? uglify() : gutil.noop())
        .pipe(
            size({
                title: config.prod ? 'JS' : 'JS (unminified)',
                showFiles: true,
                gzip: config.prod,
            }),
        )
        .pipe(dest(path.join(config.paths.assets, 'js')))
        .pipe(bs.stream());
}

exports.js = series(js);
