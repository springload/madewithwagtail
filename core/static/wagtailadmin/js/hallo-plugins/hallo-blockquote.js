(function() {

  (function($) {
    
    return $.widget("IKS.blockquotebutton", {
      options: {
        uuid: '',
        editable: null
      },
      populateToolbar: function(toolbar) {
        var button, widget;
 
        widget = this;
        
        getEnclosingQuote = function() {
          var node;

          node = widget.options.editable.getSelection().commonAncestorContainer;
          return $(node).parents('blockquote').get(0);
        };

        button = $('<span></span>');
        button.hallobutton({
          uuid: this.options.uuid,
          editable: this.options.editable,
          label: 'Pull Out Quote',
          icon: 'fa fa-quote-left',
          queryState: function(event) {
            return button.hallobutton('checked', getEnclosingQuote());
          }
        });
        toolbar.append(button);
        return button.on("click", function(event) {
          var lastSelection;
          var enclosingQuote = getEnclosingQuote();

          if (!enclosingQuote) {
            lastSelection = widget.options.editable.getSelection();

            if (!lastSelection.collapsed) {
              var newNode = document.createElement("blockquote");
              newNode.appendChild(document.createTextNode(lastSelection.toString()));

              lastSelection.deleteContents();
              lastSelection.insertNode(newNode);
              lastSelection.setStartAfter(newNode);
              lastSelection.setEndAfter(newNode);

              newNode = document.createElement("br");
              lastSelection.insertNode(newNode);
              lastSelection.setStartAfter(newNode);
              lastSelection.setEndAfter(newNode);

              widget.options.editable.element.trigger('change');
            }
          }
          else {
            $(enclosingQuote).replaceWith($(enclosingQuote).text());
            button.hallobutton('checked', false);
            widget.options.editable.element.trigger('change');
          }
          return false;
        });
      }
    });

  })(jQuery);
 
}).call(this);