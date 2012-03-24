if (typeof(busmon) == 'undefined') { busmon = {}; }

$.extend(busmon, {
    // A _regex that gets updated by user input.  Used by busmon.filter
    regex: new RegExp(".*"),

    // Filtration scheme applied to all onmessage callbacks.
    // Rejects the callback if json.topic doesn't match the current global
    // regex.
    filter: function(callback, json) {
        if ( busmon.regex.test(json.topic) ) { callback(); }
    },

    // A special version of busmon.filter() that checks the message body instead
    // of the topic.  Used by the ColorizedMessages widget.
    filter_content: function(callback, json) {
        if ( busmon.regex.test(json.msg) ) { callback(); }
    },

    apply_new_regex: function(value) {
        // Take in the new value.  This will affect all callbacks passed
        // through busmon.filter(callback, json);
        var re = new RegExp(value);
        busmon.regex = re;

        // Hard-coded id here... :/
        var selector = "topics-bar-chart";

        // We're going to run through all the items in the bar chart and remove
        // any that are not matched by the new regular expr.
        var removed = [];
        var kept = [];
        var keys = tw2.d3.util.keys(selector);
        for (var i = 0; i < keys.length; i++) {
            if (!busmon.regex.test(keys[i])) {
                tw2.d3.util.remove_key(selector, keys[i]);
                removed.push(keys[i]);
            } else {
                kept.push(keys[i]);
            }
        }

        // Notify the user about matches
        if ( value == "" ) {
            $.gritter.add({title: "busmon", text: "Filter removed.",});
        } else {
            $.gritter.add({
                title: "busmon",
                text: "Matched " + kept.join(", "),
            });
            $.gritter.add({
                title: "busmon",
                text: "Removed " + removed.join(", "),
            });
        }
    },
});

$(document).ready(function() {
    $('.filterbox input').change(function(e) {
        busmon.apply_new_regex($('.filterbox input').val());
    });
});
