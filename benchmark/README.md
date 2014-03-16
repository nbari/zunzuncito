Benchmark
---------

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
