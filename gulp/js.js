var gulp = require("gulp");
var config = require("./config");
var fs = require("fs");
var path = require("path");

var browserify = require("browserify");
var _ = require("underscore");
var glob = require("glob");
var gutil = require("gulp-util");
var source = require('vinyl-source-stream');
//var gulpBrowserify = require("gulp-browserify");


gulp.task('browserify', function(done) {

    // Run a bundle through browserify
    function bundleThis(srcArray) {
        _.each(srcArray, function(src) {
            var localName = src.replace(".bundle.js", ".js");
            localName = path.relative(config.paths.js, localName);

            var bundle = browserify([ "./" + src ]).bundle();
            gutil.log("Browserifying", src);
            bundle.pipe(source(localName))
                .pipe(gulp.dest( path.join(config.paths.assets, "js") ))
                .on("end", function() {
                    done();
                })
            ;
        });
    };

    var entryPoints = glob.sync( path.join( config.paths.js, "**", "*.bundle.js") );

    if (entryPoints) {
        bundleThis(entryPoints);
    }

});


gulp.task("js", ['browserify'], function() {

});

