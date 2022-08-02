#######################
Documentation authoring
#######################

*****
Local
*****

Documentation generation and publishing
=======================================
To build html documentation locally, just run::

    make docs-html

    # open in browser
    open doc/build/html/index.html

    # on Linux
    xdg-open doc/build/html/index.html


******
Public
******

Automatic rebuild through ``git push`` event
============================================

When pushing to the repository, the Sphinx-based documentation will
automatically be refreshed and published to https://hiveeyes.org/docs/beradio/.
