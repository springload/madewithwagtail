/* Wagtail sites frontend JS */

(function(document, window) {

    "use strict";

    var browser = require('./lib/browser.js');
    var analytics = require('./lib/analytics.js');

    var Site = function() {
       var self = this;

       if ("addEventListener" in window) {
           document.onreadystatechange = function () {
               if (document.readyState === "complete") {
                   self.init.call(self);
               }
           };
       } else {
           window.onload = function() {
               self.init.call(self);
           };
       }

   };


   Site.prototype = {

       init: function() {

           GA.init();

       }
   };

   var site = new Site();
   window.wagtailsites = site;
   return site;

})(document, window);
