import os
import sys


conf_dir = os.path.dirname(os.path.abspath(__file__))
conf_dir = os.path.join(conf_dir, 'helloworld')
sys.path.insert(0, conf_dir)
from helloworld.config.middleware import make_app
main = make_app({}, full_stack=False, static_files=False, cache_dir='')
