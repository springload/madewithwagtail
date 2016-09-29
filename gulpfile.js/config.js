var path = require("path");
var rootPath = path.join("./core");
var appPath = path.join(rootPath, "frontend");

var prod = process.env.NODE_ENV === 'production';

module.exports = {
    prod: prod,

    paths: {
        root: rootPath,
        sass: path.join(appPath, "sass"),
        js: path.join(appPath, "js"),
        svg: path.join(appPath, "svg"),
        appName: 'wagtailsites.js',
        build: path.join(rootPath, "build"),
        content: path.join(rootPath, "content"),
        templates: path.join(rootPath, "templates"),
        //webroot: path.join(rootPath, "www"),
        assets: path.join(rootPath, "static")
    },

    PleeeaseOptions: {
        minifier: prod,
        sourcemaps: false,
        mqpacker: false,
        filters: true,
        rem: true,
        pseudoElements: true,
        opacity: true,
        autoprefixer: {
            browsers: ['> 1%'],
        },
    },

};
