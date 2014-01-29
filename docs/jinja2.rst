Jinja2
======

`Jinja2 <http://jinja.pocoo.org/docs/>`_ is a modern and designer friendly templating language for Python,
modelled after Django’s templates. It is fast, widely used and secure with the
optional sandboxed template execution environment::

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
almost anything easy.
