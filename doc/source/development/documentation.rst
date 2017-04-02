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

To automatically publish the Sphinx-generated documentation to https://hiveeyes.org/docs/beradio/
when pushing to git@git.elmyra.de:hiveeyes/beradio.git, follow these steps:

- Add or enable key ``www-data@pulp`` at https://git.elmyra.de/hiveeyes/beradio/deploy_keys::

    ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDEq0S3KQd22iuuHsdBPAdHctew89ex+RXtc6f0YJZSVtNyl0HCU7RdcDadNQA7muixJqVrZdOaz+YfC3InZt/6JMyhCfdwQNlsXuEH9QNfnll33bHeFCRJBayRub5BSzFF8gFs2VFDyqw1xj657NPp8BteXXiJiF1rCwAXrwPk4LA8PJwL3xCfZcrgBT8nTSzrK5ez/vM+sUKWE6SM+PRO9CljezO8z8vzi9qWoYWfsi5x/q4TO8xTiY6+v1FQKfJp0lggphfUFHmvkx1nvZofLXYdqXwLTPQJxpX7/i/rHL7kRh1cBI5UBZyEYzZ14p00iB+DHb89XO2XcacrCFiY4bakeVy652S47K21Hd8lRTVrKPeVuEcAyc+QhAu262V5N1Op1Ab/pZvDVVgeDXXUktT8DHvwPYtEEX3hEPsQMZHKu8ngedo4pavMqHqDTo2QF9VY5e53BaSkhRGfUOUv0Olm0TW5mzWMTbPLyzoYSTFeT0l+4zVHJNcEoxsSRPqcgaq03GFK2t/j+Mn69JwFCvB555cQ53SYR8o54QEn697Oxfv0G+ZSVS2d69hBV+XNz6BVXpBI0QCOS7tTehHokNODsgJHWJFp6+ueNWr+LWFj+8Q164IoMTtf4wym89A3wF/Bf7/474KC3xjW8NSoCC9+TcJc6RRW1rlQzjv8tQ== www-data@pulp

- Add web hook for "Push events" at https://git.elmyra.de/hiveeyes/beradio/hooks with URL::

    https://gitlab:KoabMulp@docs.elmyra.de/hiveeyes/.gitlab-webhook

- Perform a push event to the repository or use the "Test Web Hook" button in GitLab

- The documentation should now be available at
  https://hiveeyes.org/docs/beradio/


Hook into your domain namespace
===============================
The base publishing address is https://docs.elmyra.de/hiveeyes/, where
https://hiveeyes.org/docs/beradio/ is pointing to as a http reverse proxy.

::

    <VirtualHost *:443>

        ServerName hiveeyes.org
        # [...]

        # reverse proxy to documentation platform
        SSLProxyEngine on
        <Location "/docs">
            ProxyPass https://docs.elmyra.de/hiveeyes/
            ProxyPassReverse https://docs.elmyra.de/hiveeyes/
        </Location>

    </VirtualHost>

- Access documentation at
  https://hiveeyes.org/docs/beradio/

