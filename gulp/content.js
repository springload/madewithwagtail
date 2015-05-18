var gulp = require("gulp");
var config = require("./config");
var fs = require("fs");
var path = require("path");

var shell = require("gulp-shell");


gulp.task('content', shell.task([
    "wrangler build " + config.paths.content + " " + config.paths.webroot + " --force"
]))
