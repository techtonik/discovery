Gadget is a HTML + JavaScript snippet with third party
content that can be securely run on your site.
Security is achieved by wrapping contents in <iframe>.


Tutorial: Making Flattr Gadget
==============================

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

To test it, save it into .xml file, upload somewhere
and load in from site that supports gadgets, such as
Google Code. For example, the code to load the current
version of flattr.xml on GC from this repository: 

    <wiki:gadget url="https://bitbucket.org/techtonik/discovery/raw/ed9b95ad8fde9bdf5b0e4ba8fd3f0832852c5a18/web/gadgets/flattr.xml"/>

This renders 300x150 box with <h2> title element above
it if inserted in Google Code wiki page. To remove
border around it and shrink size, you need to add more
attributes to the element:

    <wiki:gadget border="0" width="110" height="20" url="https://bitbucket.org/techtonik/discovery/raw/e934594350c62806b4ceb213a67eb4c0402cf129/web/gadgets/flattr.xml"/>

Note that for this to work in Google Code, this should
be written as one line tag. This URL changed to remove
JavaScript from Gadget, which makes it faster to load.

It is possible to simplify Gadget code even more by
specifying URL instead of HTML.

    <?xml version="1.0" encoding="UTF-8" ?>
    <Module>
      <ModulePrefs/>
      <Content type="url"
        href="//api.flattr.com/button/view/?uid=techtonik&amp;button=compact&amp;url=http%3A%2F%2Fcode.google.com%2Fp%2Fpython-patch%2F"
        preferred_height="20"
        preferred_width="110">
      </Content> 
    </Module>
