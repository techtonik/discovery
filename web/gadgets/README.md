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

Bring this code to http://jsfiddle.net/ to experiment.

The static image doesn't show current Flattr counter,
so it is not as attractive as it could be. To display
the counter, we need to use JavaScript, but Google
Code (where python-patch project is located) doesn't
allow to embed JavaScript into project pages.

So, we need to create a Gadget. The original
JavaScript looks like this:

   <script id='fbhpwmv'>(function(i){
     var f,s=document.getElementById(i);
     f=document.createElement('iframe');
     f.src='//api.flattr.com/button/view/?uid=techtonik&button=compact&url=http%3A%2F%2Fcode.google.com%2Fp%2Fpython-patch%2F';
     f.title='Flattr';
     f.height=20;
     f.width=110;
     f.style.borderWidth=0;
     s.parentNode.insertBefore(f,s);})('fbhpwmv');
   </script>

It creates <iframe> element that loads HTML (not
image) from api.flattr.com server.

The minimal Google Gadget is described at
https://developers.google.com/gadgets/docs/gs

    <?xml version="1.0" encoding="UTF-8" ?> 
    <Module>
      <ModulePrefs title="hello world example" /> 
      <Content type="html">
         <![CDATA[ 
           Hello, world!
         ]]>
      </Content> 
    </Module>
