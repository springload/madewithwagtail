var config = require('./config');
var gulp = require('gulp');
var svgstore = require('gulp-svgstore');
var svgmin = require('gulp-svgmin');
var path = require( 'path');
var size = require('gulp-size');
var rename = require('gulp-rename');

gulp.task('svg', function () {
    return gulp
        .src( path.join( config.paths.svg, "**", "*.svg" ) )
        .pipe(rename({prefix: 'i-'}))
        .pipe(svgmin())
        .pipe(svgstore({ inlineSvg: true }))
        .pipe(rename("svg.html"))
        .pipe(gulp.dest( path.join( config.paths.templates, "core", "includes" ) ));
});
