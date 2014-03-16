import bobo


@bobo.query('/welcome')
def welcome():
    return "Hello World!"


main = bobo.Application(bobo_resources=__name__)
