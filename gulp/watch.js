var gulp = require("gulp");
var config = require("./config");
var path = require("path");
var bs = require('browser-sync').create('main');

gulp.task('watch', ['js', 'css', 'svg'], function() {
    bs.init({
        open: false,
        // server: config.paths.templates,
        proxy: 'localhost:8111'
    });

    var justReload = [
        path.join(config.paths.templates, '**', '*.html')
    ];

    gulp.watch(justReload, bs.reload);
    gulp.watch(path.join(config.paths.sass, '**', '*.scss'), ['css']);
    gulp.watch(path.join(config.paths.js, '**', '*.js'), ['js']);
    gulp.watch(path.join(config.paths.svg, '**', '*.svg'), ['svg']);
});
