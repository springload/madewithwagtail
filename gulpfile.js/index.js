require("./watch");
require("./js");
require("./css");
require("./svg");

var gulp = require("gulp");

gulp.task('build', ['js', 'css', 'svg']);
gulp.task('default', ['build']);
