(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
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

},{"./lib/analytics.js":2,"./lib/browser.js":3}],2:[function(require,module,exports){
/**
 * Analytics.js
 * http://springload.co.nz/
 *
 * Copyright 2014, Springload
 * Released under the MIT license.
 * http://www.opensource.org/licenses/mit-license.php
 *
 * Date: Mon 3 March, 2014
 */
window.GA = (function (window, document) {

    "use strict";

    var GA = {

        // Modifiable options
        options: {

            // The default category - the document uri
            default_category: "/" + document.location.pathname.substr(1),

            // The default action
            default_action: "Click",

            // The default attribute, event and element that will be used for the trackable events
            default_trackable_attribute: "analytics",

            default_trackable_event: "click",

            default_trackable_element: "a",

            // The default label attribute
            default_label_attribute: "href",

            // The default separator to use within the analytics attribute
            default_separator: "|",

            // Available default categories
            categories: {
                footer: "Footer",
                nav: "Navigation",
                ui_element: "UI element"
            },

            // Available default actions
            actions: {
                interaction: "Interaction"
            }

        },


        /**
         * Track an event with Google Analytics
         * @param category - The category for GA
         * @param action - The action for GA
         * @param label - The label for GA
         * @param value - The value for GA
         */
        event: function (category, action, label, value) {

            var self = this;

            //console.log("GA");
            //console.log("category", category);
            //console.log("action", action);
            //console.log("label", label);
            //console.log("value", value);

            category = category || self.options.default_category;
            action = action || self.options.default_action;

            if (typeof window._gaq === "object") {
                window._gaq.push(["_trackEvent", category, action, label, value]);
            } else if (typeof window.ga === "function") {
                window.ga('send', 'event', category, action, label, value);
            }

        },

        /**
         * Initialise the analytics module.
         * @param options
         */
        init: function (options) {

            var self = this;

            self.options = self.extend(self.options, options);

            self.setupTrackables(self.options.default_trackable_attribute, self.options.default_trackable_event, self.options.default_trackable_element, self.options.default_label_attribute);

        },

        /**
         * Deep extend object
         * @param out
         * @returns {*}
         */
        extend: function(out) {

            out = out || {};

            for (var i = 1; i < arguments.length; i++) {

                var obj = arguments[i];

                if (!obj) {
                    continue;
                }

                for (var key in obj) {
                    if (obj.hasOwnProperty(key)) {
                        if (typeof obj[key] === 'object') {
                            this.extend(out[key], obj[key]);
                        } else {
                            out[key] = obj[key];
                        }
                    }
                }

            }

            return out;

        },

        /**
         * on event handler
         * @param element
         * @param name
         * @param callback
         */
        on:  function (element, name, callback) {
            if ("addEventListener" in window) {
                element.addEventListener(name, callback, false);
            } else if ("attachEvent" in window){
                element.attachEvent("on" + name, function anon() {
                    callback.call(element);
                });
            } else {
                element["on" + name] = function anon() {
                    callback.call(element);
                };
            }
        },

        /**
         * Select any elements that match the selectors
         * @param trackable_attribute
         * @param trackable_element
         * @returns {NodeList}
         */
        selectElements: function(trackable_attribute, trackable_element) {

            return document.querySelectorAll("[data-" + trackable_attribute + "] " + trackable_element + ", " + trackable_element + "[data-" + trackable_attribute + "]");

        },

        /**
         * Find the closest parent element with an trackable attribute set on it and return the value of that attribute
         * @param element
         * @param trackable_attribute
         * @returns {string}
         */
        getParentElementTrackingData: function(element, trackable_attribute) {

            var parent = element.parentNode,
                tracking_data = "",
                parent_tracking_data;

            while (parent !== null) {
                var current_parent = parent;
                if (current_parent.hasAttribute("data-" + trackable_attribute)) {
                    parent_tracking_data = current_parent.getAttribute("data-" + trackable_attribute);
                    if (parent_tracking_data !== null) {
                        tracking_data = parent_tracking_data;
                    }
                    parent = null;
                } else {
                    parent = current_parent.parentNode;
                }
            }

            return tracking_data;

        },

        /**
         * Define the trackable elements and set the event handlers on them
         * @param trackable_attribute
         * @param trackable_event
         * @param trackable_element
         * @param label_attribute
         */
        setupTrackables: function (trackable_attribute, trackable_event, trackable_element, label_attribute) {

            // Only supporting modern browsers for selection
            if (document.querySelectorAll) {

                var self = this,
                    elements = self.selectElements(trackable_attribute, trackable_element),
                    i = 0;

                for (i; i < elements.length; i++) {

                    (function(el) {

                        var params = el.getAttribute("data-" + trackable_attribute),
                            category = null,
                            action = null,
                            label = el.getAttribute(label_attribute),
                            value = null;

                        // Check for a category on a parent element
                        if (params === null) {
                            params = self.getParentElementTrackingData(el, trackable_attribute);
                        }

                        // Grab the values from the data attribute
                        params = params.split(self.options.default_separator);

                        // Set the event tracking variables
                        category = params[0] !== undefined && params[0] !== '' ? params[0] : undefined;
                        action = params[1] !== undefined && params[1] !== '' ? params[1] : undefined;
                        label = params[2] !== undefined && params[2] !== '' ? params[2] : label;
                        value = params[3] !== undefined && params[3] !== '' ? params[3] : undefined;

                        self.on(el, trackable_event, function() {

                            // Fire off the event
                            self.event(category, action, label, value);

                        });

                    })(elements[i]);

                }


            }

        }

    };

    return {

        /**
         * Track an event.
         * @param label
         * @param category
         * @param action
         * @param value
         */
        track: function (label, category, action, value) {
            GA.event(category, action, label, value);
        },

        /**
         * Initialise the module
         * @param options
         */
        init: function (options) {
            GA.init(options);
        },

        /**
         * Setup additional trackable elements on the fly after initialisation
         * @param trackable_attribute data attribute
         * @param trackable_event event type. e.g. mouseenter
         * @param trackable_element - e.g. span
         * @param label_attribute - where the default label is ready from. e.g. data-label
         */
        setupTrackables: function (trackable_attribute, trackable_event, trackable_element, label_attribute) {
            GA.setupTrackables(trackable_attribute, trackable_event, trackable_element, label_attribute);
        },


        // Categories
        cat: GA.options.categories,

        // Actions
        act: GA.options.actions

    };

})(window, document);
},{}],3:[function(require,module,exports){
window.Browser = (function(window){
    /**
     * Browser helper library for common things we need to know.
     * Access via get method: Browser.get("clickEvent"); 
     * ----------------------------------------------------------------------------
     */
    var BrowserHelpers = {
        clickEvent: function() {
            return "ontouchstart" in window ? "touchend" : "click";
        },
        cssPrefix: function() {
            var el = document.createElement( "div" ),
            prefixes = ["Webkit", "Moz", "O", "ms"];
            for ( var i = 0; i < prefixes.length; i++ ) {
                if ( prefixes[i] + "Transition" in el.style ) {
                    return prefixes[i];
                }
            }
            return "transition" in el.style ? "" : false;
        },
        getPrefixedCssProp: function(baseProp) {
            var str = this.cssPrefix();
            if (!str) return false;
            str = str.replace(/([A-Z])/g, function(str,m1){ return '-' + m1.toLowerCase(); }).replace(/^ms-/,'-ms-');
            return str;
        },
        transitionEvent: function() {
            var prefix = this.cssPrefix(),
                cssProp = this.getPrefixedCssProp(prefix),
                transitionEvent;

            switch(prefix) {
                case "Moz":
                    transitionEvent = "transitionend";
                    break;
                case "Webkit":
                    transitionEvent = "webkitTransitionEnd";
                    break;
                case "O":
                    transitionEvent = "oTransitionEnd";
                    break;
                case "ms":
                    transitionEvent = "MSTransitionEnd";
                    break;
                case "":
                    transitionEvent = "transitionend";
                    break;
            }
            return transitionEvent;
        },
        animationEvent: function() {
            var prefix = this.cssPrefix(),
                cssProp = this.getPrefixedCssProp(prefix),
                animationEvent;

            switch(prefix) {
                case "Moz":
                    animationEvent = "animationend";
                    break;
                case "Webkit":
                    animationEvent = "webkitAnimationEnd";
                    break;
                case "O":
                    animationEvent = "oAnimationEnd";
                    break;
                case "ms":
                    animationEvent = "MSAnimationEnd";
                    break;
                case "":
                    animationEvent = "animationend";
                    break;
            }
            return animationEvent;
        },
        _getHelper: function(key) {
            if (!arguments.length) {
                return false;
            }
            var self = this,
                helperFunc;
            helperFunc = self[key];
            if (typeof(helperFunc) === "function") {
                return helperFunc.call(self);
            }
            return false;
        }
    };

    /**
     * Default tests
     * ----------------------------------------------------------------------------
     */
    var DefaultTests = {
        modern: function(){
            return 'querySelector' in document && 'localStorage' in window && 'addEventListener' in window;
        }
    };

    /**
     * Browser object 
     * ----------------------------------------------------------------------------
     */
    var Browser = {
        tests: {},
        results: {},
        init: function(tests) {
            var self = this;
            if (!arguments.length) {
                self.addTests(DefaultTests);
            } else {
                self.addTests(Tests);
            }
        },
        _getResult: function(key) {
            if (!arguments.length) {
                return false;
            }
            var self = this;
            return self.results[key];
        },
        _run: function(testName) {
            var self = this;
            var testFunc = self.tests[testName];
            if (typeof(testFunc) === "function") {
                self.results[testName] = testFunc();
            }
        },
        _remove: function(testName) {
            var self = this;
            var _test = self.tests[testName];
            var _result = self.results[testName];
            if (_test) {
                _test = undefined;
            }
            if (_result) {
                _result = undefined;
            }
        },
        addTests: function(object) {
            if (!arguments.length) {
                return false;
            }
            var self = this,
                testFunc;
            switch (typeof(object)) {
                case "object":
                    for (var testName in object) {
                        testFunc = object[testName];
                        self.addTest(testName, testFunc);
                    }
                    break;
                case "function":
                    this.addTest("userTest", object);
                    break;
                default:
                    return false;
            }

            return this;
        },
        runTests: function(){
            var self = this;
            if (!self.tests) {
                return false;
            }
            for (var testName in self.tests) {
                self._run(testName);
            }
            self.updateHtml();
            return self.results;
        },
        updateHtml: function() {
            var self = this;
            for (var res in self.results) {
                if (self.results[res]) {
                    document.documentElement.className += " " + res;
                }
            }
            document.documentElement.className = document.documentElement.className.replace("no-js", "js");
        },
        runTest: function(testName){
            var self = this;
            self._run(testName);
        },
        addTest: function(testName, testFunc){
            var self = this;
            if (!self.tests[testName]) {
                self.tests[testName] = testFunc;
            }
        },
        removeTest: function(testName){
            var self = this;
            self._remove(testName);
            return true;
        },
        removeTests: function() {
            var self = this;
            self.tests = {};
            self.results = {};
            return true;
        }
    };

    /**
     * Run the test package
     */
//    Browser.init();
//    Browser.runTests();

    /**
     * Expose the Browser object to the window
     */
    return {
        features: function() {
            return Browser.results;
        },
        is: function(key) {
            return Browser._getResult(key);
        },
        has: function(key) {
            return Browser._getResult(key);
        },
        supports: function(key) {
            return Browser._getResult(key);
        },
        get: function(key) {
            return BrowserHelpers._getHelper(key);
        },
        removeTest: function(testName){
            return Browser.removeTest(testName);
        },
        removeTests: function(){
            return Browser.removeTests();
        },
        addTest: function(testName, testFunc){
            return Browser.addTest();
        },
        addTests: function(tests){
            return Browser.addTests(tests);
        },
        runTest: function(testName){
            return Browser.runTest(testName);
        },
        runTests: function(){
            return Browser.runTests();
        },
        init: function(tests){
            return Browser.init(tests);
        }
    };

})(window);


/**
 * Your feature tests
 * ----------------------------------------------------------------------------
 */
var Tests = (function(window, Browser){

    // Define your test suite here. For more tests, visit the exhaustive list:
    // http://diveintohtml5.info/everything.html
    var Tests = {
        responsive: function() {
            return typeof(window.matchMedia) === "function" ? true : false;
        },
        modern: function(){
            return 'querySelector' in document && 'localStorage' in window && 'addEventListener' in window;
        },
        touchEvents: function() {
            return "ontouchstart" in window;
        },
        svg: function() {
            return document.implementation.hasFeature('http://www.w3.org/TR/SVG11/feature#Image', '1.1')
        },
        noTouchEvents: function() {
            return "ontouchstart" in window ? false : true;
        },
        placeholders: function() {
            return ('placeholder' in document.createElement('input'));
        },
        nativeOverflowScrolling: function() {
            var el = document.createElement('div');
            el.setAttribute('style', '-webkit-overflow-scrolling: touch;');
            return el.style.webkitOverflowScrolling == 'touch' ? true : false;
        },
        mobile: function() {
            var userAgent = navigator.userAgent.toLowerCase();
            return userAgent.match(/(iPhone|iPod|iPad|Android|BlackBerry)/) ? true : false;
        },
        fixed: function() {
            var test = document.createElement('div');
            var root = document.documentElement;
            test.style.cssText = 'position:fixed;top:0;';
            root.appendChild(test);
            var hasFixed = test.offsetTop === 0 ? true : false;
            root.removeChild(test);
            return hasFixed;
        },
        retina: function() {
            var mediaQuery = "(-webkit-min-device-pixel-ratio: 1.5), (min--moz-device-pixel-ratio: 1.5), (-o-min-device-pixel-ratio: 3/2), (min-resolution: 1.5dppx)";
            if (window.devicePixelRatio > 1) {
                return true;
            }
            if (window.matchMedia && window.matchMedia(mediaQuery).matches) {
                return true;
            }
            return false;
        },
        history: function() {
            return window.history && window.history.pushState ? true : false;
        },
        tel: function() {
            var i = document.createElement('input');
            i.setAttribute('type', 'tel');
            return i.type !== 'text';
        },
        postMessage: function() {
            return !!window.postMessage;
        },
        fileApi: function() {
            return typeof FileReader != 'undefined';
        },
        localStorage: function() {
            try {
              return 'localStorage' in window && window['localStorage'] !== null;
            } catch(e) {
              return false;
            }
        },
        transitions: function() {
            return Browser.get("transitionEvent")||false;
        }
    };

    return Tests;

})(window, Browser);

// Run the test package
Browser.init(Tests);
Browser.runTests();
},{}]},{},[1]);
