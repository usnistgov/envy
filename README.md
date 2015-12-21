# envy - a web-browser-based phase envelope viewer

By Ian Bell, National Institute of Standards and Technology, 2015-

## Installation

  - Do a recursive clone of the repository using git (do **NOT** click on the download ZIP, you need to pull three.js as well)
  - Run the ``copy_js.py`` script (at console: ``python copy_js.py``) to copy the javascript files from within the guts of three.js library to the js directory
  - Run the ``generate_data.py`` script in python (at console: ``python generate_data.py``) to generate a phase envelope using [NIST REFPROP](http://www.nist.gov/srd/nist23.cfm) called through [CoolProp](www.coolprop.org).  Will create the file ``env.json``, and if the VLE data files are available at the hardcoded path, a set of data for the experimental data points
  - Open index.html in your browser
  - Click the button at the top to load the ``env.json`` file you generated
  - Zoom out to look at the phase envelope
  
## Information

The goal of this project is to plot three-dimensional phase envelopes in the browser with no other dependencies.  At the moment, the JSON data used for the surface is generated via an external script.  Eventually everything will happen in the browser.

This project leverages the open-source packages:
  - [three.js](http://www.threejs.org)
  - [jQuery](https://jquery.com/)
  - [jQueryUI](http://jqueryui.com/)

## Debugging

If you are having problems with WebGL, first [go to this link](http://webglreport.com/?v=1).  Make sure you don't have an error.  I found on my computer that installing newer drivers for my video card (ATI) fixed WebGL support in Firefox.
  
## License

  - Public Domain.  See LICENSE.txt
  - Uses other libraries, the licenses for which are nearly all MIT
  
## Disclaimers

  - Use or mention of technologies or programs in this web site is not intended to imply recommendation or endorsement by the National Institute of Standards and Technology, nor is it intended to imply that these items are necessarily the best available for the purpose. 