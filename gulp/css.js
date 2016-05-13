var gulp = require("gulp");
var config = require("./config");
var fs = require("fs");
var path = require("path");

var sass = require("gulp-sass");
var plz = require("gulp-pleeease");
var gutil = require('gulp-util');
var size = require('gulp-size');
var bs = require('browser-sync').get('main');
var sourcemaps = require('gulp-sourcemaps');
//var livereload = require('gulp-livereload');

/*
 ---------------------------------------------------------------------------
 Stylesheets
 ---------------------------------------------------------------------------
 */

gulp.task('css', function (done) {

    gulp.src(path.join(config.paths.sass, "**", "*.scss"))
        .pipe(config.prod ? gutil.noop() : sourcemaps.init())
        .pipe(sass())
        .on('error', function handleError(err) {
            gutil.log(err.message);
            bs.notify(err.message, 10000);
            this.emit('end');
        })
        .pipe(plz(config.PleeeaseOptions))
        .pipe(config.prod ? gutil.noop() : sourcemaps.write())
        .pipe(size({ title: config.prod ? 'CSS' : 'CSS (unminified)', showFiles: true, gzip: config.prod }))
        .pipe(gulp.dest( path.join(config.paths.assets, "css") ))
        .pipe(bs.stream());
    ;

    done();

});