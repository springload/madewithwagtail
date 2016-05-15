
var gulp = require("gulp");
require("./gulp/watch");
require("./gulp/js");
require("./gulp/css");
require("./gulp/icons");
require("./gulp/svg");
// require("./gulp/content");
require("./gulp/clean");



gulp.task('build', ['js', 'css', 'svg'], function(done) {
    done();
});

gulp.task('default', ['build']);
