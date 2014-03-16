Benchmark
---------

Source: http://mindref.blogspot.pt/2012/09/python-fastest-web-framework.html


Setup:

    virtualenv env

Install uwsgi and zunzuncito

    pip install uwsgi

    pip install zunzuncito

Run

    ./env/bin/uwsgi uwsgi.ini

Test:

     curl -i http://127.0.0.1:8080/welcome

will output something like:

    HTTP/1.1 200 OK
    Request-ID: 94cdc117-acf7-11e3-96ef-02ff10000e0b
    Content-Type: text/html; charset=UTF-8

    Hello World!


Running the benchmark:

python benchmark.py:

                  msec    rps  tcalls  funcs
    bobo          5043  19828     120     67
    bottle        1797  55648      53     31
    django       10575   9456     183     89
    falcon        1130  88466      29     25
    flask        14786   6763     257    119
    pylons       10014   9986     195     82
    pyramid       2990  33450      65     48
    pyramid       2993  33408      65     48
    tornado      10030   9970     188     67
    wsgi           175 570568       8      8
    zunzuncito   10702   9344     261     65

* msec - a total time taken in milliseconds
* rps - requests processed per second
* tcalls - total number of call made by corresponding web framework
* funcs -  number of unique functions used.
