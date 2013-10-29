# uwsgi --http :8080 --wsgi-file app.py --callable app --master

import os
import zunzuncito

document_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sandbox/api/')

app = api = zunzuncito.ZunZun(document_root)
