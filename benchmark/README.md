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
    bobo          5002  19991     120     67
    bottle        1691  59151      53     31
    django       10376   9638     183     89
    falcon        1076  92978      29     25
    flask        14496   6899     257    119
    pylons       10032   9968     195     82
    pyramid       2935  34075      65     48
    pyramid       2954  33849      65     48
    tornado      10027   9973     188     67
    wsgi           172 580916       8      8
    zunzuncito   10810   9251     269     65

* msec - a total time taken in milliseconds
* rps - requests processed per second
* tcalls - total number of call made by corresponding web framework
* funcs -  number of unique functions used.
