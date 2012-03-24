if (typeof(busmon) == 'undefined') { busmon = {}; }

$.extend(busmon, {
    // A _regex that gets updated by user input.  Used by busmon.filter
    regex: new RegExp("^.*$$"),

    // Filtration scheme applied to all onmessage callbacks.
    // Rejects the callback if json.topic doesn't match the current global
    // regex.
    filter: function(callback, json) {
        if ( busmon.regex.test(json.topic) ) { callback(); }
    },

    apply_new_regex: function(value) {
        // Take in the new value
        var re = new RegExp(value);
        busmon.regex = re;

        // Hard-coded id here... :/
        var selector = "topics-bar-chart";

        var keys = tw2.d3.util.keys(selector);
        for (var i = 0; i < keys.length; i++) {
            if (!busmon.regex.test(keys[i])) {
                tw2.d3.util.remove_key(selector, keys[i]);
            }
        }
    },
});

$(document).ready(function() {
    $('.filterbox input').change(function(e) {
        busmon.apply_new_regex($('.filterbox input').val());
    });
});
