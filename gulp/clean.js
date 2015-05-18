var gulp = require("gulp");
var config = require("./config");
var path = require("path");
var del = require('del');

gulp.task('clean', function() {
    return del([
        path.join( config.paths.build )
    ]);
});

