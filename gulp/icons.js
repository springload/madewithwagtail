var gulp = require("gulp");
var grunt = require('gulp-grunt')(gulp);

/*
 ---------------------------------------------------------------------------
 Icons
 ---------------------------------------------------------------------------
 */

gulp.task('icon', function() {

    gulp.run('grunt-icon');

});
