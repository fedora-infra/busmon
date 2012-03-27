<html>
  <head>
    <link href="css/text.css" media="screen" type="text/css" rel="stylesheet"></link>
    <link href="css/960_24_col.css" media="screen" type="text/css" rel="stylesheet"></link>
    <link href="css/site.css" media="screen" type="text/css" rel="stylesheet"></link>
    <link href="css/voting.css" media="screen" type="text/css" rel="stylesheet"></link>

    <title>Fedora Busmon</title>
  </head>
  <body>
    <div id="header">
      <div><H1><span id="logo">Fedora</span> bus·mon</H1></div>
    </div>
    <div class="right pane">
      <div class="content filterbox">
        <input placeholder="Filter topics with a regular expression"/>
      </div>
    </div>
    <div class="clear"></div>
    ${self.body()}
    <div class="clear"></div>
    ${tmpl_context.moksha_socket.display() | n}
  </body>
</html>

