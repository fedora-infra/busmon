function compute_prefix(depth) {
    var prefix = ""
    for (var i = 0; i < depth*4; i++) {prefix += " ";}
    return prefix;
}

function handle_primitive(value) {
    if (value == null ||
        typeof value == "number" ||
        typeof value == "boolean") {
        return "<span class=\"kc\">" + value + "</span>"
    } else if (typeof value == "string") {
        return "<span class=\"s2\">\"" + value + "\"</span>";
    } else {
        return " * ERROR * ";
    }
}

function _markup(obj, depth) {
    var result, prefix;
    result = "";
    prefix = compute_prefix(depth);

    $.each(obj, function(key, value) {
        result += prefix + key + ": ";
        if (value == null ||
            typeof value == "string" ||
            typeof value == "number" ||
            typeof value == "boolean") {
            result += handle_primitive(value);
        } else if (value instanceof Array) {
            result += "[" + $.map(value, handle_primitive).join(', ') + "]";
        } else {
            result += markup(value, depth+1)
        }
        result += ",\n";
    });
    return result;
}

function markup(obj, depth) {
    var prefix, previous;
    if (depth === undefined) { depth = 1; }
    prefix = compute_prefix(depth);
    // I'd like to avoid doing this twice, but...
    previous = compute_prefix(depth-1);
    return "{\n" + _markup(obj, depth) + previous + "}";
}
