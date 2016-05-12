var path = require("path");
var rootPath = path.join("./core");
var appPath = path.join(rootPath, "frontend");

module.exports = {

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
        minifier: false,
        sourcemaps: false,
        mqpacker: false,
        filters: true,
        rem: true,
        pseudoElements: true,
        opacity: true,
        autoprefixer: {
            "browsers": ["last 10 versions", "ie 8"]
        }
    }

};
