(function() {

  (function($) {

    return $.widget("IKS.citebutton", {
      options: {
        uuid: '',
        editable: null
      },
      populateToolbar: function(toolbar) {
        var button, widget;
 
        widget = this;
        getEnclosingCite = function() {
          var node;

          node = widget.options.editable.getSelection().commonAncestorContainer;
          return $(node).parents('cite').get(0);
        };

        button = $('<span></span>');
        button.hallobutton({
          uuid: this.options.uuid,
          editable: this.options.editable,
          label: 'Cite',
          icon: 'fa fa-comment-o',
          command: null,
          queryState: function(event) {
            var refreshedButton = button.hallobutton('checked', getEnclosingCite());
            if ($(refreshedButton).hasClass('ui-state-active')) {
              $(toolbar).find('button').not($(button).children()[0]).removeClass('ui-state-active');
            }
            return refreshedButton;
          }
        });
        toolbar.append(button);
        return button.on("click", function(event) {
          var lastSelection, parentElement, eol;
          var enclosingCite = getEnclosingCite();

          if (!enclosingCite) {
            lastSelection = widget.options.editable.getSelection();

            if (!lastSelection.collapsed) {
              parentElement = $(lastSelection.endContainer).parent();

              if (parentElement.is("blockquote")) {
                parentElement.append(lastSelection.createContextualFragment("<cite>" + lastSelection.toString() + "</cite>"));
                lastSelection.deleteContents();
                eol = $( "<br/>" ).insertAfter(parentElement);
                placeCaretAtEnd(eol[0]);
                widget.options.editable.element.trigger('change');
              }

            }

          }
          else {
            $(enclosingCite).replaceWith($(enclosingCite).text());
            button.hallobutton('checked', false);
            widget.options.editable.element.trigger('change');
          }
          return false;
        });
      }

    });

  })(jQuery);

}).call(this);