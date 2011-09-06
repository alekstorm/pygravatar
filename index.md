---
---

<html><head>
  <meta charset="utf-8"/>

  <title>PyGravatar</title>

  <style type="text/css">
    body {
      margin-top: 1.0em;
      background-color: #6ae8fa;
      font-family: Helvetica, Arial, FreeSans, san-serif;
      color: #000000;
    }
    #container {
      margin: 0 auto;
      width: 700px;
    }
    h1 { font-size: 3.8em; color: #951705; margin-bottom: 3px; }
    h1 .small { font-size: 0.4em; }
    h1 a { text-decoration: none }
    h2 { font-size: 1.5em; color: #951705; }
    h3 { text-align: center; color: #951705; }
    a { color: #951705; }
    .description { font-size: 1.2em; margin-bottom: 30px; margin-top: 30px; font-style: italic;}
    .download { float: right; }
    pre { background: #000; color: #fff; padding: 15px;}
    hr { border: 0; width: 80%; border-bottom: 1px solid #aaa}
    .footer { text-align:center; padding-top:30px; font-style: italic; }
  </style>
</head>

<body>
  <a href="http://github.com/alekstorm/pygravatar"><img style="position: absolute; top: 0; right: 0; border: 0;" src="http://s3.amazonaws.com/github/ribbons/forkme_right_darkblue_121621.png" alt="Fork me on GitHub"></a>

  <div id="container">
    <div class="download">
      <a href="http://github.com/alekstorm/pygravatar/zipball/master">
        <img border="0" width="90" src="http://github.com/images/modules/download/zip.png"></a>
      <a href="http://github.com/alekstorm/pygravatar/tarball/master">
        <img border="0" width="90" src="http://github.com/images/modules/download/tar.png"></a>
    </div>

    <h1><a href="http://github.com/alekstorm/pygravatar">PyGravatar</a></h1>

    <div class="description">
      Python bindings for the Gravatar API
    </div>

    <h2>Author</h2>
    <p>Alek Storm (alek.storm@gmail.com)</p>

    <h2>Download</h2>
    <p>
        To install, run `pip install pygravatar`.
        You can download this project in either
        <a href="http://github.com/alekstorm/pygravatar/zipball/master">zip</a> or
        <a href="http://github.com/alekstorm/pygravatar/tarball/master">tar</a> formats.
        You can browse the source code online at <a href="http://github.com/alekstorm/pygravatar">its GitHub page</a>.
    </p>
    <p>You can also clone the project with <a href="http://git-scm.com">Git</a> by running:</p>

    `$ git clone git://github.com/alekstorm/pygravatar`

    <h2>Getting Started</h2>
    <p>
        To verify that the library is working and can connect to the server, run:

        ```python
        >>> import gravatar
        >>> user = gravatar.User(<email>, password=<password>) # substitute the email address and password of a Gravatar account
        >>> user.test()
        1315290974 # however many seconds have passed since 1970
        ```
    </p>

    <h2>Documentation</h2>
    <p>
        Full API documentation is available <a href="sphinx">here</a>.<br><br>
        The underlying XML-RPC API specification is also available <a href="http://en.gravatar.com/site/implement/xmlrpc/">here</a>.
    </p>
  </div>
</body>
</html>
