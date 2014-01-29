Jinja2
======

`Jinja2 <http://jinja.pocoo.org/docs/>`_ is a modern and designer friendly templating language for Python,
modelled after Django’s templates. It is fast, widely used and secure with the
optional sandboxed template execution environment:

.. code-block:: guess
   :linenos:

    <title>{% block title %}{% endblock %}</title>
    <ul>
    {% for user in users %}
        <li><a href="{{ user.url }}">{{ user.username }}</a></li>
    {% endfor %}
    </ul>

Why ?
.....

**Zunzuncito** was made mainly for responding in `json format <http://www.json.org/>`_
not HTML, but also one of the design goals is to give the ability to create
almost anything easy, therefor if you need to display HTML, Jinja2 integrates
very easy.

Example
.......

The following code, handles the request for: `http://api.zunzun.io/jinja2 <http://api.zunzun.io/jinja2>`_.

.. code-block:: python
   :linenos:
   :emphasize-lines: 4, 26, 34

   import logging
   import os

   from jinja2 import Environment, FileSystemLoader
   from zunzuncito import tools

   jinja = Environment(autoescape=True, loader=FileSystemLoader(
       os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates')))


   class APIResource(object):

       def __init__(self, api):
           self.api = api
           self.log = logging.getLogger()
           self.log.info(tools.log_json({
               'vroot': api.vroot,
               'API': api.version,
               'URI': api.URI,
               'method': api.method
           }, True)
           )

       def dispatch(self, environ):

           self.api.headers['Content-Type'] = 'text/html; charset=UTF-8'

           template_values = {
               'IP': environ.get('REMOTE_ADDR', 0)
           }

           template = jinja.get_template('example.html')

           return template.render(template_values).encode('utf-8')


The example.html contains:

.. code-block:: guess
   :linenos:
   :emphasize-lines: 4, 8

   <html>
       <head>
           <meta charset="utf-8">
           <title>{{ IP }}</title>
       </head>

       <body>
       <h3>IP: {{ IP }}</h3>
       </body>
   </html>


Directory structure
...................

.. code-block:: rest
   :emphasize-lines: 10,12,14
   :linenos:

   /home/
     `--zunzun/
        |--app.py
        `--my_api
           |--__init__.py
           `--default
              |--__init__.py
              `--v0
                 |--__init__.py
                 `--zun_jinja2
                    |--__init__.py
                    |--zun_jinja2.py
                    `--templates
                       `--example.html


.. seealso::

   `zun_jinja2 API resource <https://github.com/nbari/zunzuncito/tree/master/my_api/default/v0/zun_jinja2>`_



GAE
...

When using google app engine you need to add this lines to your
`app.yaml <https://developers.google.com/appengine/docs/python/config/appconfig>`_
file in order to be available to import jinja2::

   libraries:
   - name: jinja2
     version: latest
