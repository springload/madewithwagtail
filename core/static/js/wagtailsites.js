(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({"/Users/sam/Sites/madewithwagtail2/core/frontend/js/wagtailsites.js":[function(require,module,exports){
'use strict';

var _springloadAnalytics = require('springload-analytics.js');

var _springloadAnalytics2 = _interopRequireDefault(_springloadAnalytics);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

if ('ontouchstart' in window) {
    document.documentElement.className = document.documentElement.className + ' touch';
} else {
    document.documentElement.className = document.documentElement.className + ' no-touch';
}

var Site = function Site() {
    _classCallCheck(this, Site);

    _springloadAnalytics2.default.init();
};

window.site = new Site({});

},{"springload-analytics.js":"/Users/sam/Sites/madewithwagtail2/node_modules/springload-analytics.js/analytics.js"}],"/Users/sam/Sites/madewithwagtail2/node_modules/springload-analytics.js/analytics.js":[function(require,module,exports){
(function (global){
'use strict';

var _typeof = typeof Symbol === "function" && typeof Symbol.iterator === "symbol" ? function (obj) { return typeof obj; } : function (obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol ? "symbol" : typeof obj; };

/**
 * Analytics.js
 * http://springload.co.nz/
 *
 * Copyright 2015, Springload
 * Released under the MIT license.
 * http://www.opensource.org/licenses/mit-license.php
 */
(function (root, factory) {
    if (typeof define === 'function' && define.amd) {
        // AMD. Register as an anonymous module.
        define([], function () {
            return root.GA = factory();
        });
    } else if ((typeof module === 'undefined' ? 'undefined' : _typeof(module)) === 'object' && module.exports) {
        // Node. Does not work with strict CommonJS, but
        // only CommonJS-like enviroments that support module.exports,
        // like Node.
        module.exports = root.GA = factory();
    } else {
        // Browser globals
        root.GA = factory();
    }
})(typeof global !== 'undefined' ? global : undefined.window || undefined.global, function () {
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
            // The node's text content is used as label
            default_label_is_text_content: false,
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
        event: function event(category, action, label, value) {
            var self = this;
            category = category || self.options.default_category;
            action = action || self.options.default_action;
            if (_typeof(window._gaq) === "object") {
                window._gaq.push(["_trackEvent", category, action, label, value]);
            } else if (typeof window.ga === "function") {
                window.ga('send', 'event', category, action, label, value);
            }
        },
        /**
         * Initialise the analytics module.
         * @param options
         */
        init: function init(options) {
            var self = this;
            self.options = self.extend(self.options, options);
            self.setupTrackables(self.options.default_trackable_attribute, self.options.default_trackable_event, self.options.default_trackable_element, self.options.default_label_attribute, self.options.default_label_is_text_content);
        },
        /**
         * Deep extend object
         * @param out
         * @returns {*}
         */
        extend: function extend(out) {
            out = out || {};
            for (var i = 1; i < arguments.length; i++) {
                var obj = arguments[i];
                if (!obj) {
                    continue;
                }
                for (var key in obj) {
                    if (obj.hasOwnProperty(key)) {
                        if (_typeof(obj[key]) === 'object') {
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
        on: function on(element, name, callback) {
            if ("addEventListener" in window) {
                element.addEventListener(name, callback, false);
            } else if ("attachEvent" in window) {
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
        selectElements: function selectElements(trackable_attribute, trackable_element) {
            return document.querySelectorAll("[data-" + trackable_attribute + "] " + trackable_element + ", " + trackable_element + "[data-" + trackable_attribute + "]");
        },
        /**
         * Find the closest parent element with an trackable attribute set on it and return the value of that attribute
         * @param element
         * @param trackable_attribute
         * @returns {string}
         */
        getParentElementTrackingData: function getParentElementTrackingData(element, trackable_attribute) {
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
         * @param label_is_text_content
         */
        setupTrackables: function setupTrackables(trackable_attribute, trackable_event, trackable_element, label_attribute, label_is_text_content) {
            // Only supporting modern browsers for selection
            if (document.querySelectorAll) {
                var self = this,
                    elements = self.selectElements(trackable_attribute, trackable_element),
                    i = 0;
                for (i; i < elements.length; i++) {
                    (function (el) {
                        var params = el.getAttribute("data-" + trackable_attribute),
                            category = null,
                            action = null,
                            label = label_is_text_content ? el.textContent : el.getAttribute(label_attribute),
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
                        self.on(el, trackable_event, function () {
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
        track: function track(label, category, action, value) {
            GA.event(category, action, label, value);
        },
        /**
         * Initialise the module
         * @param options
         */
        init: function init(options) {
            GA.init(options);
        },
        /**
         * Setup additional trackable elements on the fly after initialisation
         * @param trackable_attribute data attribute
         * @param trackable_event event type. e.g. mouseenter
         * @param trackable_element - e.g. span
         * @param label_attribute - where the default label is ready from. e.g. data-label
         * @param label_is_text_content - whether the node's text content is used as label
         */
        setupTrackables: function setupTrackables(trackable_attribute, trackable_event, trackable_element, label_attribute, label_is_text_content) {
            GA.setupTrackables(trackable_attribute, trackable_event, trackable_element, label_attribute, label_is_text_content);
        },
        // Categories
        cat: GA.options.categories,
        // Actions
        act: GA.options.actions
    };
});

}).call(this,typeof global !== "undefined" ? global : typeof self !== "undefined" ? self : typeof window !== "undefined" ? window : {})

},{}]},{},["/Users/sam/Sites/madewithwagtail2/core/frontend/js/wagtailsites.js"])
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIm5vZGVfbW9kdWxlcy9icm93c2VyaWZ5L25vZGVfbW9kdWxlcy9icm93c2VyLXBhY2svX3ByZWx1ZGUuanMiLCJjb3JlL2Zyb250ZW5kL2pzL3dhZ3RhaWxzaXRlcy5qcyIsIm5vZGVfbW9kdWxlcy9zcHJpbmdsb2FkLWFuYWx5dGljcy5qcy9hbmFseXRpY3MuanMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUE7OztBQ0NBOzs7Ozs7OztBQUVBLElBQUksa0JBQWtCLE1BQXRCLEVBQThCO0FBQzFCLGFBQVMsZUFBVCxDQUF5QixTQUF6QixHQUFxQyxTQUFTLGVBQVQsQ0FBeUIsU0FBekIsR0FBcUMsUUFBMUU7QUFDSCxDQUZELE1BRU87QUFDSCxhQUFTLGVBQVQsQ0FBeUIsU0FBekIsR0FBcUMsU0FBUyxlQUFULENBQXlCLFNBQXpCLEdBQXFDLFdBQTFFO0FBQ0g7O0lBRUssSSxHQUNGLGdCQUFjO0FBQUE7O0FBQ1Ysa0NBQUcsSUFBSDtBQUNILEM7O0FBR0wsT0FBTyxJQUFQLEdBQWMsSUFBSSxJQUFKLENBQVMsRUFBVCxDQUFkOzs7Ozs7Ozs7Ozs7Ozs7O0FDUEMsV0FBVSxJQUFWLEVBQWdCLE9BQWhCLEVBQXlCO0FBQ3RCLFFBQUksT0FBTyxNQUFQLEtBQWtCLFVBQWxCLElBQWdDLE9BQU8sR0FBM0MsRUFBZ0Q7O0FBRTVDLGVBQU8sRUFBUCxFQUFXLFlBQVk7QUFDbkIsbUJBQVEsS0FBSyxFQUFMLEdBQVUsU0FBbEI7QUFDSCxTQUZEO0FBR0gsS0FMRCxNQUtPLElBQUksUUFBTyxNQUFQLHlDQUFPLE1BQVAsT0FBa0IsUUFBbEIsSUFBOEIsT0FBTyxPQUF6QyxFQUFrRDs7OztBQUlyRCxlQUFPLE9BQVAsR0FBa0IsS0FBSyxFQUFMLEdBQVUsU0FBNUI7QUFDSCxLQUxNLE1BS0E7O0FBRUgsYUFBSyxFQUFMLEdBQVUsU0FBVjtBQUNIO0FBQ0osQ0FmQSxFQWVDLE9BQU8sTUFBUCxLQUFrQixXQUFsQixHQUFnQyxNQUFoQyxHQUF5QyxVQUFLLE1B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cEMsaUNBQUssS0FBTCxDQUFXLFFBQVgsRUFBcUIsTUFBckIsRUFBNkIsS0FBN0IsRUFBb0MsS0FBcEM7QUFDSCx5QkFIRDtBQUlILHFCQXRCRCxFQXNCRyxTQUFTLENBQVQsQ0F0Qkg7QUF1Qkg7QUFDSjtBQUNKO0FBMUtJLEtBQVQ7O0FBNktBLFdBQU87Ozs7Ozs7O0FBUUgsZUFBTyxlQUFVLEtBQVYsRUFBaUIsUUFBakIsRUFBMkIsTUFBM0IsRUFBbUMsS0FBbkMsRUFBMEM7QUFDN0MsZUFBRyxLQUFILENBQVMsUUFBVCxFQUFtQixNQUFuQixFQUEyQixLQUEzQixFQUFrQyxLQUFsQztBQUNILFNBVkU7Ozs7O0FBZUgsY0FBTSxjQUFVLE9BQVYsRUFBbUI7QUFDckIsZUFBRyxJQUFILENBQVEsT0FBUjtBQUNILFNBakJFOzs7Ozs7Ozs7QUEwQkgseUJBQWlCLHlCQUFVLG1CQUFWLEVBQStCLGVBQS9CLEVBQWdELGlCQUFoRCxFQUFtRSxlQUFuRSxFQUFvRixxQkFBcEYsRUFBMkc7QUFDeEgsZUFBRyxlQUFILENBQW1CLG1CQUFuQixFQUF3QyxlQUF4QyxFQUF5RCxpQkFBekQsRUFBNEUsZUFBNUUsRUFBNkYscUJBQTdGO0FBQ0gsU0E1QkU7O0FBOEJILGFBQUssR0FBRyxPQUFILENBQVcsVUE5QmI7O0FBZ0NILGFBQUssR0FBRyxPQUFILENBQVc7QUFoQ2IsS0FBUDtBQWtDSCxDQWpPQSxDQUFEIiwiZmlsZSI6ImdlbmVyYXRlZC5qcyIsInNvdXJjZVJvb3QiOiIiLCJzb3VyY2VzQ29udGVudCI6WyIoZnVuY3Rpb24gZSh0LG4scil7ZnVuY3Rpb24gcyhvLHUpe2lmKCFuW29dKXtpZighdFtvXSl7dmFyIGE9dHlwZW9mIHJlcXVpcmU9PVwiZnVuY3Rpb25cIiYmcmVxdWlyZTtpZighdSYmYSlyZXR1cm4gYShvLCEwKTtpZihpKXJldHVybiBpKG8sITApO3ZhciBmPW5ldyBFcnJvcihcIkNhbm5vdCBmaW5kIG1vZHVsZSAnXCIrbytcIidcIik7dGhyb3cgZi5jb2RlPVwiTU9EVUxFX05PVF9GT1VORFwiLGZ9dmFyIGw9bltvXT17ZXhwb3J0czp7fX07dFtvXVswXS5jYWxsKGwuZXhwb3J0cyxmdW5jdGlvbihlKXt2YXIgbj10W29dWzFdW2VdO3JldHVybiBzKG4/bjplKX0sbCxsLmV4cG9ydHMsZSx0LG4scil9cmV0dXJuIG5bb10uZXhwb3J0c312YXIgaT10eXBlb2YgcmVxdWlyZT09XCJmdW5jdGlvblwiJiZyZXF1aXJlO2Zvcih2YXIgbz0wO288ci5sZW5ndGg7bysrKXMocltvXSk7cmV0dXJuIHN9KSIsIlxuaW1wb3J0IEdBIGZyb20gJ3NwcmluZ2xvYWQtYW5hbHl0aWNzLmpzJztcblxuaWYgKCdvbnRvdWNoc3RhcnQnIGluIHdpbmRvdykge1xuICAgIGRvY3VtZW50LmRvY3VtZW50RWxlbWVudC5jbGFzc05hbWUgPSBkb2N1bWVudC5kb2N1bWVudEVsZW1lbnQuY2xhc3NOYW1lICsgJyB0b3VjaCc7XG59IGVsc2Uge1xuICAgIGRvY3VtZW50LmRvY3VtZW50RWxlbWVudC5jbGFzc05hbWUgPSBkb2N1bWVudC5kb2N1bWVudEVsZW1lbnQuY2xhc3NOYW1lICsgJyBuby10b3VjaCc7XG59XG5cbmNsYXNzIFNpdGUge1xuICAgIGNvbnN0cnVjdG9yKCkge1xuICAgICAgICBHQS5pbml0KCk7XG4gICAgfVxufVxuXG53aW5kb3cuc2l0ZSA9IG5ldyBTaXRlKHsgfSk7XG4iLCIvKipcbiAqIEFuYWx5dGljcy5qc1xuICogaHR0cDovL3NwcmluZ2xvYWQuY28ubnovXG4gKlxuICogQ29weXJpZ2h0IDIwMTUsIFNwcmluZ2xvYWRcbiAqIFJlbGVhc2VkIHVuZGVyIHRoZSBNSVQgbGljZW5zZS5cbiAqIGh0dHA6Ly93d3cub3BlbnNvdXJjZS5vcmcvbGljZW5zZXMvbWl0LWxpY2Vuc2UucGhwXG4gKi9cbihmdW5jdGlvbiAocm9vdCwgZmFjdG9yeSkge1xuICAgIGlmICh0eXBlb2YgZGVmaW5lID09PSAnZnVuY3Rpb24nICYmIGRlZmluZS5hbWQpIHtcbiAgICAgICAgLy8gQU1ELiBSZWdpc3RlciBhcyBhbiBhbm9ueW1vdXMgbW9kdWxlLlxuICAgICAgICBkZWZpbmUoW10sIGZ1bmN0aW9uICgpIHtcbiAgICAgICAgICAgIHJldHVybiAocm9vdC5HQSA9IGZhY3RvcnkoKSk7XG4gICAgICAgIH0pO1xuICAgIH0gZWxzZSBpZiAodHlwZW9mIG1vZHVsZSA9PT0gJ29iamVjdCcgJiYgbW9kdWxlLmV4cG9ydHMpIHtcbiAgICAgICAgLy8gTm9kZS4gRG9lcyBub3Qgd29yayB3aXRoIHN0cmljdCBDb21tb25KUywgYnV0XG4gICAgICAgIC8vIG9ubHkgQ29tbW9uSlMtbGlrZSBlbnZpcm9tZW50cyB0aGF0IHN1cHBvcnQgbW9kdWxlLmV4cG9ydHMsXG4gICAgICAgIC8vIGxpa2UgTm9kZS5cbiAgICAgICAgbW9kdWxlLmV4cG9ydHMgPSAocm9vdC5HQSA9IGZhY3RvcnkoKSk7XG4gICAgfSBlbHNlIHtcbiAgICAgICAgLy8gQnJvd3NlciBnbG9iYWxzXG4gICAgICAgIHJvb3QuR0EgPSBmYWN0b3J5KCk7XG4gICAgfVxufSh0eXBlb2YgZ2xvYmFsICE9PSAndW5kZWZpbmVkJyA/IGdsb2JhbCA6IHRoaXMud2luZG93IHx8IHRoaXMuZ2xvYmFsLCBmdW5jdGlvbiAoKSB7XG4gICAgXCJ1c2Ugc3RyaWN0XCI7XG5cbiAgICB2YXIgR0EgPSB7XG4gICAgICAgIC8vIE1vZGlmaWFibGUgb3B0aW9uc1xuICAgICAgICBvcHRpb25zOiB7XG4gICAgICAgICAgICAvLyBUaGUgZGVmYXVsdCBjYXRlZ29yeSAtIHRoZSBkb2N1bWVudCB1cmlcbiAgICAgICAgICAgIGRlZmF1bHRfY2F0ZWdvcnk6IFwiL1wiICsgZG9jdW1lbnQubG9jYXRpb24ucGF0aG5hbWUuc3Vic3RyKDEpLFxuICAgICAgICAgICAgLy8gVGhlIGRlZmF1bHQgYWN0aW9uXG4gICAgICAgICAgICBkZWZhdWx0X2FjdGlvbjogXCJDbGlja1wiLFxuICAgICAgICAgICAgLy8gVGhlIGRlZmF1bHQgYXR0cmlidXRlLCBldmVudCBhbmQgZWxlbWVudCB0aGF0IHdpbGwgYmUgdXNlZCBmb3IgdGhlIHRyYWNrYWJsZSBldmVudHNcbiAgICAgICAgICAgIGRlZmF1bHRfdHJhY2thYmxlX2F0dHJpYnV0ZTogXCJhbmFseXRpY3NcIixcbiAgICAgICAgICAgIGRlZmF1bHRfdHJhY2thYmxlX2V2ZW50OiBcImNsaWNrXCIsXG4gICAgICAgICAgICBkZWZhdWx0X3RyYWNrYWJsZV9lbGVtZW50OiBcImFcIixcbiAgICAgICAgICAgIC8vIFRoZSBkZWZhdWx0IGxhYmVsIGF0dHJpYnV0ZVxuICAgICAgICAgICAgZGVmYXVsdF9sYWJlbF9hdHRyaWJ1dGU6IFwiaHJlZlwiLFxuICAgICAgICAgICAgLy8gVGhlIG5vZGUncyB0ZXh0IGNvbnRlbnQgaXMgdXNlZCBhcyBsYWJlbFxuICAgICAgICAgICAgZGVmYXVsdF9sYWJlbF9pc190ZXh0X2NvbnRlbnQ6IGZhbHNlLFxuICAgICAgICAgICAgLy8gVGhlIGRlZmF1bHQgc2VwYXJhdG9yIHRvIHVzZSB3aXRoaW4gdGhlIGFuYWx5dGljcyBhdHRyaWJ1dGVcbiAgICAgICAgICAgIGRlZmF1bHRfc2VwYXJhdG9yOiBcInxcIixcbiAgICAgICAgICAgIC8vIEF2YWlsYWJsZSBkZWZhdWx0IGNhdGVnb3JpZXNcbiAgICAgICAgICAgIGNhdGVnb3JpZXM6IHtcbiAgICAgICAgICAgICAgICBmb290ZXI6IFwiRm9vdGVyXCIsXG4gICAgICAgICAgICAgICAgbmF2OiBcIk5hdmlnYXRpb25cIixcbiAgICAgICAgICAgICAgICB1aV9lbGVtZW50OiBcIlVJIGVsZW1lbnRcIlxuICAgICAgICAgICAgfSxcbiAgICAgICAgICAgIC8vIEF2YWlsYWJsZSBkZWZhdWx0IGFjdGlvbnNcbiAgICAgICAgICAgIGFjdGlvbnM6IHtcbiAgICAgICAgICAgICAgICBpbnRlcmFjdGlvbjogXCJJbnRlcmFjdGlvblwiXG4gICAgICAgICAgICB9XG4gICAgICAgIH0sXG4gICAgICAgIC8qKlxuICAgICAgICAgKiBUcmFjayBhbiBldmVudCB3aXRoIEdvb2dsZSBBbmFseXRpY3NcbiAgICAgICAgICogQHBhcmFtIGNhdGVnb3J5IC0gVGhlIGNhdGVnb3J5IGZvciBHQVxuICAgICAgICAgKiBAcGFyYW0gYWN0aW9uIC0gVGhlIGFjdGlvbiBmb3IgR0FcbiAgICAgICAgICogQHBhcmFtIGxhYmVsIC0gVGhlIGxhYmVsIGZvciBHQVxuICAgICAgICAgKiBAcGFyYW0gdmFsdWUgLSBUaGUgdmFsdWUgZm9yIEdBXG4gICAgICAgICAqL1xuICAgICAgICBldmVudDogZnVuY3Rpb24gKGNhdGVnb3J5LCBhY3Rpb24sIGxhYmVsLCB2YWx1ZSkge1xuICAgICAgICAgICAgdmFyIHNlbGYgPSB0aGlzO1xuICAgICAgICAgICAgY2F0ZWdvcnkgPSBjYXRlZ29yeSB8fCBzZWxmLm9wdGlvbnMuZGVmYXVsdF9jYXRlZ29yeTtcbiAgICAgICAgICAgIGFjdGlvbiA9IGFjdGlvbiB8fCBzZWxmLm9wdGlvbnMuZGVmYXVsdF9hY3Rpb247XG4gICAgICAgICAgICBpZiAodHlwZW9mIHdpbmRvdy5fZ2FxID09PSBcIm9iamVjdFwiKSB7XG4gICAgICAgICAgICAgICAgd2luZG93Ll9nYXEucHVzaChbXCJfdHJhY2tFdmVudFwiLCBjYXRlZ29yeSwgYWN0aW9uLCBsYWJlbCwgdmFsdWVdKTtcbiAgICAgICAgICAgIH0gZWxzZSBpZiAodHlwZW9mIHdpbmRvdy5nYSA9PT0gXCJmdW5jdGlvblwiKSB7XG4gICAgICAgICAgICAgICAgd2luZG93LmdhKCdzZW5kJywgJ2V2ZW50JywgY2F0ZWdvcnksIGFjdGlvbiwgbGFiZWwsIHZhbHVlKTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgfSxcbiAgICAgICAgLyoqXG4gICAgICAgICAqIEluaXRpYWxpc2UgdGhlIGFuYWx5dGljcyBtb2R1bGUuXG4gICAgICAgICAqIEBwYXJhbSBvcHRpb25zXG4gICAgICAgICAqL1xuICAgICAgICBpbml0OiBmdW5jdGlvbiAob3B0aW9ucykge1xuICAgICAgICAgICAgdmFyIHNlbGYgPSB0aGlzO1xuICAgICAgICAgICAgc2VsZi5vcHRpb25zID0gc2VsZi5leHRlbmQoc2VsZi5vcHRpb25zLCBvcHRpb25zKTtcbiAgICAgICAgICAgIHNlbGYuc2V0dXBUcmFja2FibGVzKHNlbGYub3B0aW9ucy5kZWZhdWx0X3RyYWNrYWJsZV9hdHRyaWJ1dGUsIHNlbGYub3B0aW9ucy5kZWZhdWx0X3RyYWNrYWJsZV9ldmVudCwgc2VsZi5vcHRpb25zLmRlZmF1bHRfdHJhY2thYmxlX2VsZW1lbnQsIHNlbGYub3B0aW9ucy5kZWZhdWx0X2xhYmVsX2F0dHJpYnV0ZSwgc2VsZi5vcHRpb25zLmRlZmF1bHRfbGFiZWxfaXNfdGV4dF9jb250ZW50KTtcbiAgICAgICAgfSxcbiAgICAgICAgLyoqXG4gICAgICAgICAqIERlZXAgZXh0ZW5kIG9iamVjdFxuICAgICAgICAgKiBAcGFyYW0gb3V0XG4gICAgICAgICAqIEByZXR1cm5zIHsqfVxuICAgICAgICAgKi9cbiAgICAgICAgZXh0ZW5kOiBmdW5jdGlvbihvdXQpIHtcbiAgICAgICAgICAgIG91dCA9IG91dCB8fCB7fTtcbiAgICAgICAgICAgIGZvciAodmFyIGkgPSAxOyBpIDwgYXJndW1lbnRzLmxlbmd0aDsgaSsrKSB7XG4gICAgICAgICAgICAgICAgdmFyIG9iaiA9IGFyZ3VtZW50c1tpXTtcbiAgICAgICAgICAgICAgICBpZiAoIW9iaikge1xuICAgICAgICAgICAgICAgICAgICBjb250aW51ZTtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgZm9yICh2YXIga2V5IGluIG9iaikge1xuICAgICAgICAgICAgICAgICAgICBpZiAob2JqLmhhc093blByb3BlcnR5KGtleSkpIHtcbiAgICAgICAgICAgICAgICAgICAgICAgIGlmICh0eXBlb2Ygb2JqW2tleV0gPT09ICdvYmplY3QnKSB7XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgdGhpcy5leHRlbmQob3V0W2tleV0sIG9ialtrZXldKTtcbiAgICAgICAgICAgICAgICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgb3V0W2tleV0gPSBvYmpba2V5XTtcbiAgICAgICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgIH1cbiAgICAgICAgICAgIHJldHVybiBvdXQ7XG4gICAgICAgIH0sXG4gICAgICAgIC8qKlxuICAgICAgICAgKiBvbiBldmVudCBoYW5kbGVyXG4gICAgICAgICAqIEBwYXJhbSBlbGVtZW50XG4gICAgICAgICAqIEBwYXJhbSBuYW1lXG4gICAgICAgICAqIEBwYXJhbSBjYWxsYmFja1xuICAgICAgICAgKi9cbiAgICAgICAgb246ICBmdW5jdGlvbiAoZWxlbWVudCwgbmFtZSwgY2FsbGJhY2spIHtcbiAgICAgICAgICAgIGlmIChcImFkZEV2ZW50TGlzdGVuZXJcIiBpbiB3aW5kb3cpIHtcbiAgICAgICAgICAgICAgICBlbGVtZW50LmFkZEV2ZW50TGlzdGVuZXIobmFtZSwgY2FsbGJhY2ssIGZhbHNlKTtcbiAgICAgICAgICAgIH0gZWxzZSBpZiAoXCJhdHRhY2hFdmVudFwiIGluIHdpbmRvdyl7XG4gICAgICAgICAgICAgICAgZWxlbWVudC5hdHRhY2hFdmVudChcIm9uXCIgKyBuYW1lLCBmdW5jdGlvbiBhbm9uKCkge1xuICAgICAgICAgICAgICAgICAgICBjYWxsYmFjay5jYWxsKGVsZW1lbnQpO1xuICAgICAgICAgICAgICAgIH0pO1xuICAgICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgICAgICBlbGVtZW50W1wib25cIiArIG5hbWVdID0gZnVuY3Rpb24gYW5vbigpIHtcbiAgICAgICAgICAgICAgICAgICAgY2FsbGJhY2suY2FsbChlbGVtZW50KTtcbiAgICAgICAgICAgICAgICB9O1xuICAgICAgICAgICAgfVxuICAgICAgICB9LFxuICAgICAgICAvKipcbiAgICAgICAgICogU2VsZWN0IGFueSBlbGVtZW50cyB0aGF0IG1hdGNoIHRoZSBzZWxlY3RvcnNcbiAgICAgICAgICogQHBhcmFtIHRyYWNrYWJsZV9hdHRyaWJ1dGVcbiAgICAgICAgICogQHBhcmFtIHRyYWNrYWJsZV9lbGVtZW50XG4gICAgICAgICAqIEByZXR1cm5zIHtOb2RlTGlzdH1cbiAgICAgICAgICovXG4gICAgICAgIHNlbGVjdEVsZW1lbnRzOiBmdW5jdGlvbih0cmFja2FibGVfYXR0cmlidXRlLCB0cmFja2FibGVfZWxlbWVudCkge1xuICAgICAgICAgICAgcmV0dXJuIGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3JBbGwoXCJbZGF0YS1cIiArIHRyYWNrYWJsZV9hdHRyaWJ1dGUgKyBcIl0gXCIgKyB0cmFja2FibGVfZWxlbWVudCArIFwiLCBcIiArIHRyYWNrYWJsZV9lbGVtZW50ICsgXCJbZGF0YS1cIiArIHRyYWNrYWJsZV9hdHRyaWJ1dGUgKyBcIl1cIik7XG4gICAgICAgIH0sXG4gICAgICAgIC8qKlxuICAgICAgICAgKiBGaW5kIHRoZSBjbG9zZXN0IHBhcmVudCBlbGVtZW50IHdpdGggYW4gdHJhY2thYmxlIGF0dHJpYnV0ZSBzZXQgb24gaXQgYW5kIHJldHVybiB0aGUgdmFsdWUgb2YgdGhhdCBhdHRyaWJ1dGVcbiAgICAgICAgICogQHBhcmFtIGVsZW1lbnRcbiAgICAgICAgICogQHBhcmFtIHRyYWNrYWJsZV9hdHRyaWJ1dGVcbiAgICAgICAgICogQHJldHVybnMge3N0cmluZ31cbiAgICAgICAgICovXG4gICAgICAgIGdldFBhcmVudEVsZW1lbnRUcmFja2luZ0RhdGE6IGZ1bmN0aW9uKGVsZW1lbnQsIHRyYWNrYWJsZV9hdHRyaWJ1dGUpIHtcbiAgICAgICAgICAgIHZhciBwYXJlbnQgPSBlbGVtZW50LnBhcmVudE5vZGUsXG4gICAgICAgICAgICAgICAgdHJhY2tpbmdfZGF0YSA9IFwiXCIsXG4gICAgICAgICAgICAgICAgcGFyZW50X3RyYWNraW5nX2RhdGE7XG4gICAgICAgICAgICB3aGlsZSAocGFyZW50ICE9PSBudWxsKSB7XG4gICAgICAgICAgICAgICAgdmFyIGN1cnJlbnRfcGFyZW50ID0gcGFyZW50O1xuICAgICAgICAgICAgICAgIGlmIChjdXJyZW50X3BhcmVudC5oYXNBdHRyaWJ1dGUoXCJkYXRhLVwiICsgdHJhY2thYmxlX2F0dHJpYnV0ZSkpIHtcbiAgICAgICAgICAgICAgICAgICAgcGFyZW50X3RyYWNraW5nX2RhdGEgPSBjdXJyZW50X3BhcmVudC5nZXRBdHRyaWJ1dGUoXCJkYXRhLVwiICsgdHJhY2thYmxlX2F0dHJpYnV0ZSk7XG4gICAgICAgICAgICAgICAgICAgIGlmIChwYXJlbnRfdHJhY2tpbmdfZGF0YSAhPT0gbnVsbCkge1xuICAgICAgICAgICAgICAgICAgICAgICAgdHJhY2tpbmdfZGF0YSA9IHBhcmVudF90cmFja2luZ19kYXRhO1xuICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgICAgIHBhcmVudCA9IG51bGw7XG4gICAgICAgICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgICAgICAgICAgcGFyZW50ID0gY3VycmVudF9wYXJlbnQucGFyZW50Tm9kZTtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9XG4gICAgICAgICAgICByZXR1cm4gdHJhY2tpbmdfZGF0YTtcbiAgICAgICAgfSxcbiAgICAgICAgLyoqXG4gICAgICAgICAqIERlZmluZSB0aGUgdHJhY2thYmxlIGVsZW1lbnRzIGFuZCBzZXQgdGhlIGV2ZW50IGhhbmRsZXJzIG9uIHRoZW1cbiAgICAgICAgICogQHBhcmFtIHRyYWNrYWJsZV9hdHRyaWJ1dGVcbiAgICAgICAgICogQHBhcmFtIHRyYWNrYWJsZV9ldmVudFxuICAgICAgICAgKiBAcGFyYW0gdHJhY2thYmxlX2VsZW1lbnRcbiAgICAgICAgICogQHBhcmFtIGxhYmVsX2F0dHJpYnV0ZVxuICAgICAgICAgKiBAcGFyYW0gbGFiZWxfaXNfdGV4dF9jb250ZW50XG4gICAgICAgICAqL1xuICAgICAgICBzZXR1cFRyYWNrYWJsZXM6IGZ1bmN0aW9uICh0cmFja2FibGVfYXR0cmlidXRlLCB0cmFja2FibGVfZXZlbnQsIHRyYWNrYWJsZV9lbGVtZW50LCBsYWJlbF9hdHRyaWJ1dGUsIGxhYmVsX2lzX3RleHRfY29udGVudCkge1xuICAgICAgICAgICAgLy8gT25seSBzdXBwb3J0aW5nIG1vZGVybiBicm93c2VycyBmb3Igc2VsZWN0aW9uXG4gICAgICAgICAgICBpZiAoZG9jdW1lbnQucXVlcnlTZWxlY3RvckFsbCkge1xuICAgICAgICAgICAgICAgIHZhciBzZWxmID0gdGhpcyxcbiAgICAgICAgICAgICAgICAgICAgZWxlbWVudHMgPSBzZWxmLnNlbGVjdEVsZW1lbnRzKHRyYWNrYWJsZV9hdHRyaWJ1dGUsIHRyYWNrYWJsZV9lbGVtZW50KSxcbiAgICAgICAgICAgICAgICAgICAgaSA9IDA7XG4gICAgICAgICAgICAgICAgZm9yIChpOyBpIDwgZWxlbWVudHMubGVuZ3RoOyBpKyspIHtcbiAgICAgICAgICAgICAgICAgICAgKGZ1bmN0aW9uKGVsKSB7XG4gICAgICAgICAgICAgICAgICAgICAgICB2YXIgcGFyYW1zID0gZWwuZ2V0QXR0cmlidXRlKFwiZGF0YS1cIiArIHRyYWNrYWJsZV9hdHRyaWJ1dGUpLFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIGNhdGVnb3J5ID0gbnVsbCxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICBhY3Rpb24gPSBudWxsLFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIGxhYmVsID0gKGxhYmVsX2lzX3RleHRfY29udGVudCkgPyBlbC50ZXh0Q29udGVudCA6IGVsLmdldEF0dHJpYnV0ZShsYWJlbF9hdHRyaWJ1dGUpLFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIHZhbHVlID0gbnVsbDtcbiAgICAgICAgICAgICAgICAgICAgICAgIC8vIENoZWNrIGZvciBhIGNhdGVnb3J5IG9uIGEgcGFyZW50IGVsZW1lbnRcbiAgICAgICAgICAgICAgICAgICAgICAgIGlmIChwYXJhbXMgPT09IG51bGwpIHtcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICBwYXJhbXMgPSBzZWxmLmdldFBhcmVudEVsZW1lbnRUcmFja2luZ0RhdGEoZWwsIHRyYWNrYWJsZV9hdHRyaWJ1dGUpO1xuICAgICAgICAgICAgICAgICAgICAgICAgfVxuXG4gICAgICAgICAgICAgICAgICAgICAgICAvLyBHcmFiIHRoZSB2YWx1ZXMgZnJvbSB0aGUgZGF0YSBhdHRyaWJ1dGVcbiAgICAgICAgICAgICAgICAgICAgICAgIHBhcmFtcyA9IHBhcmFtcy5zcGxpdChzZWxmLm9wdGlvbnMuZGVmYXVsdF9zZXBhcmF0b3IpO1xuICAgICAgICAgICAgICAgICAgICAgICAgLy8gU2V0IHRoZSBldmVudCB0cmFja2luZyB2YXJpYWJsZXNcbiAgICAgICAgICAgICAgICAgICAgICAgIGNhdGVnb3J5ID0gcGFyYW1zWzBdICE9PSB1bmRlZmluZWQgJiYgcGFyYW1zWzBdICE9PSAnJyA/IHBhcmFtc1swXSA6IHVuZGVmaW5lZDtcbiAgICAgICAgICAgICAgICAgICAgICAgIGFjdGlvbiA9IHBhcmFtc1sxXSAhPT0gdW5kZWZpbmVkICYmIHBhcmFtc1sxXSAhPT0gJycgPyBwYXJhbXNbMV0gOiB1bmRlZmluZWQ7XG4gICAgICAgICAgICAgICAgICAgICAgICBsYWJlbCA9IHBhcmFtc1syXSAhPT0gdW5kZWZpbmVkICYmIHBhcmFtc1syXSAhPT0gJycgPyBwYXJhbXNbMl0gOiBsYWJlbDtcbiAgICAgICAgICAgICAgICAgICAgICAgIHZhbHVlID0gcGFyYW1zWzNdICE9PSB1bmRlZmluZWQgJiYgcGFyYW1zWzNdICE9PSAnJyA/IHBhcmFtc1szXSA6IHVuZGVmaW5lZDtcbiAgICAgICAgICAgICAgICAgICAgICAgIHNlbGYub24oZWwsIHRyYWNrYWJsZV9ldmVudCwgZnVuY3Rpb24oKSB7XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgLy8gRmlyZSBvZmYgdGhlIGV2ZW50XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgc2VsZi5ldmVudChjYXRlZ29yeSwgYWN0aW9uLCBsYWJlbCwgdmFsdWUpO1xuICAgICAgICAgICAgICAgICAgICAgICAgfSk7XG4gICAgICAgICAgICAgICAgICAgIH0pKGVsZW1lbnRzW2ldKTtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICB9O1xuXG4gICAgcmV0dXJuIHtcbiAgICAgICAgLyoqXG4gICAgICAgICAqIFRyYWNrIGFuIGV2ZW50LlxuICAgICAgICAgKiBAcGFyYW0gbGFiZWxcbiAgICAgICAgICogQHBhcmFtIGNhdGVnb3J5XG4gICAgICAgICAqIEBwYXJhbSBhY3Rpb25cbiAgICAgICAgICogQHBhcmFtIHZhbHVlXG4gICAgICAgICAqL1xuICAgICAgICB0cmFjazogZnVuY3Rpb24gKGxhYmVsLCBjYXRlZ29yeSwgYWN0aW9uLCB2YWx1ZSkge1xuICAgICAgICAgICAgR0EuZXZlbnQoY2F0ZWdvcnksIGFjdGlvbiwgbGFiZWwsIHZhbHVlKTtcbiAgICAgICAgfSxcbiAgICAgICAgLyoqXG4gICAgICAgICAqIEluaXRpYWxpc2UgdGhlIG1vZHVsZVxuICAgICAgICAgKiBAcGFyYW0gb3B0aW9uc1xuICAgICAgICAgKi9cbiAgICAgICAgaW5pdDogZnVuY3Rpb24gKG9wdGlvbnMpIHtcbiAgICAgICAgICAgIEdBLmluaXQob3B0aW9ucyk7XG4gICAgICAgIH0sXG4gICAgICAgIC8qKlxuICAgICAgICAgKiBTZXR1cCBhZGRpdGlvbmFsIHRyYWNrYWJsZSBlbGVtZW50cyBvbiB0aGUgZmx5IGFmdGVyIGluaXRpYWxpc2F0aW9uXG4gICAgICAgICAqIEBwYXJhbSB0cmFja2FibGVfYXR0cmlidXRlIGRhdGEgYXR0cmlidXRlXG4gICAgICAgICAqIEBwYXJhbSB0cmFja2FibGVfZXZlbnQgZXZlbnQgdHlwZS4gZS5nLiBtb3VzZWVudGVyXG4gICAgICAgICAqIEBwYXJhbSB0cmFja2FibGVfZWxlbWVudCAtIGUuZy4gc3BhblxuICAgICAgICAgKiBAcGFyYW0gbGFiZWxfYXR0cmlidXRlIC0gd2hlcmUgdGhlIGRlZmF1bHQgbGFiZWwgaXMgcmVhZHkgZnJvbS4gZS5nLiBkYXRhLWxhYmVsXG4gICAgICAgICAqIEBwYXJhbSBsYWJlbF9pc190ZXh0X2NvbnRlbnQgLSB3aGV0aGVyIHRoZSBub2RlJ3MgdGV4dCBjb250ZW50IGlzIHVzZWQgYXMgbGFiZWxcbiAgICAgICAgICovXG4gICAgICAgIHNldHVwVHJhY2thYmxlczogZnVuY3Rpb24gKHRyYWNrYWJsZV9hdHRyaWJ1dGUsIHRyYWNrYWJsZV9ldmVudCwgdHJhY2thYmxlX2VsZW1lbnQsIGxhYmVsX2F0dHJpYnV0ZSwgbGFiZWxfaXNfdGV4dF9jb250ZW50KSB7XG4gICAgICAgICAgICBHQS5zZXR1cFRyYWNrYWJsZXModHJhY2thYmxlX2F0dHJpYnV0ZSwgdHJhY2thYmxlX2V2ZW50LCB0cmFja2FibGVfZWxlbWVudCwgbGFiZWxfYXR0cmlidXRlLCBsYWJlbF9pc190ZXh0X2NvbnRlbnQpO1xuICAgICAgICB9LFxuICAgICAgICAvLyBDYXRlZ29yaWVzXG4gICAgICAgIGNhdDogR0Eub3B0aW9ucy5jYXRlZ29yaWVzLFxuICAgICAgICAvLyBBY3Rpb25zXG4gICAgICAgIGFjdDogR0Eub3B0aW9ucy5hY3Rpb25zXG4gICAgfTtcbn0pKTtcbiJdfQ==
