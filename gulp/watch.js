var gulp = require("gulp");
var config = require("./config");
var fs = require("fs");
var path = require("path");

var livereload = require('gulp-livereload');



gulp.task("watch", function() {
    livereload.listen(); // install Chrome livereload plugin :)
    gulp.watch(path.join( config.paths.content, "**", "*.json"), ["content"]);
    gulp.watch(path.join( config.paths.templates, "**", "*.j2"), ["content"]);
    gulp.watch(path.join( config.paths.sass, "**", "*.scss"), ["css"]);
    gulp.watch(path.join( config.paths.js, "**", "*.js"), ["js"]);
    gulp.watch(path.join( config.paths.assets, "css", "*.css"), ["reload_css"]);
});


gulp.task('reload_css', function (done) {

    gulp.src(path.join(config.paths.assets, "css", "*.css"))
        .pipe(livereload())
    ;
    done();

});
