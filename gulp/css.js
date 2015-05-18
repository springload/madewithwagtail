var gulp = require("gulp");
var config = require("./config");
var fs = require("fs");
var path = require("path");

var sass = require("gulp-sass");
var plz = require("gulp-pleeease");
//var livereload = require('gulp-livereload');

/*
 ---------------------------------------------------------------------------
 Stylesheets
 ---------------------------------------------------------------------------
 */

gulp.task('css', function (done) {

    gulp.src(path.join(config.paths.sass, "**", "*.scss"))
        .pipe(sass({ errLogToConsole: true }))
        .pipe(plz(config.PleeeaseOptions))
        .pipe(gulp.dest( path.join(config.paths.assets, "css") ))
        //.pipe(livereload())
    ;

    done();

});