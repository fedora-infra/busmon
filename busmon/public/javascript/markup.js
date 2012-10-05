function markup(json) {
    /* Taken from http://bit.ly/Q1Xh3U with love.  Thanks, Pumbaa80! */

    if (typeof json != 'string') {
        json = JSON.stringify(json, undefined, 2);
    }
    json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    json = json.replace(
        /("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g,
        function (match) {
            var cls = 'mf';
            if (/^"/.test(match)) {
                if (/:$/.test(match)) {
                    cls = 's2';  // keys
                } else {
                    cls = 's2';  // string values
                }
            } else if (/true|false/.test(match)) {
                cls = 'kc';  // This one isn't quite the right css class.
            } else if (/null/.test(match)) {
                cls = 'kc';
            }
            return '<span class="' + cls + '">' + match + '</span>';
        }
    );
    return "<pre>" + json + "</pre>"
}

