Gadget is a HTML + JavaScript snippet with third party
content that can be securely run on your site.
Security is achieved by wrapping contents in <iframe>.


=== Tutorial: Making Flattr Gadget ===

Flattr is a web service with buttons for the third
party site. The simplest way to insert the button is
to use the following HTML code:

  <a href="https://flattr.com/submit/auto?user_id=techtonik&url=https%3A%2F%2Fcode.google.com%2Fp%2Fpython-patch%2F"
     target="_blank">
    <img src="//api.flattr.com/button/flattr-badge-large.png"
         alt="Flattr this" title="Flattr this" border="0"/>
  </a>

This loads 93x20 image that says "Flattr this!" from
api.flattr.com website. When you click the image, it
redirects you to donation page for python-patch
project.
