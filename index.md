---
title: PyGravatar
layout: default
---

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

    <pre>$ git clone git://github.com/alekstorm/pygravatar</pre>

    <h2>Getting Started</h2>
    <p>
        To verify that the library is working and can connect to the server, run:

        <pre>
>>> import gravatar
>>> user = gravatar.User(&lt;email&gt;, password=&lt;password&gt;) # substitute the email address and password of a Gravatar account
>>> user.test()
1315290974 # however many seconds have passed since 1970</pre>
    </p>

    <h2>Documentation</h2>
    <p>
        Full API documentation is available <a href="sphinx">here</a>.<br><br>
        The underlying XML-RPC API specification is also available <a href="http://en.gravatar.com/site/implement/xmlrpc/">here</a>.
    </p>
  </div>
