'use strict';

module.exports = function(grunt) {

    var pkg = grunt.file.readJSON('package.json');

    grunt.initConfig({

        pkg: pkg,

        clean: {
            pngicons: "core/static/css/png",
            build: "build"
        },

        grunticon_pigment: {
            app: {
                files: [{
                    cwd: 'core/frontend/svg',
                    dest: 'core/static/css'
                }],
                options: {
                    svgFolder: "./",
                    svgColorFolder: "colourise",
                    defaultWidth: "32px",
                    defaultHeight: "32px",
                    tmpDir: "build",
                    previewTemplate: "core/frontend/svg/template/preview.hbs",
                    svgColors: [
                        "#ffffff", // white
                        "#767676", // grey
                        "#43B1B0", // teal
                        "#358c8b"  // hover
                    ],
                    customselectors: {
                        "wagtail-logo": [".wagtail"],
                        "springload-logo-dark": [".springload-dark"]
                    }
                }
            }
        }

    });


    /**
     * The cool way to load your grunt tasks
     * --------------------------------------------------------------------
     */
    Object.keys( pkg.devDependencies ).forEach( function( dep ){
        if( dep.substring( 0, 6 ) === 'grunt-' ) grunt.loadNpmTasks( dep );
    });


    grunt.registerTask("icon", [
        "clean:pngicons",
        "grunticon_pigment:app",
        "clean:build"
    ]);

};