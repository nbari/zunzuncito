"""
TLD resource
"""

from . import tldextract

from zunzuncito import tools


class APIResource(object):

    def dispatch(self, request, response):
        request.log.debug(tools.log_json({
            'API': request.version,
            'Method': request.method,
            'URI': request.URI,
            'vroot': request.vroot
        }, True))

        if request.method == 'POST':
            domain = ''

            try:
                length = int(request.environ.get('CONTENT_LENGTH', '0'))
            except ValueError:
                length = 0

            if length != 0:
                domain = request.environ['wsgi.input'].read(length)
        else:
            domain = '/'.join(request.path)

        """
        extract callable that falls back to the included TLD snapshot, no live
        HTTP fetching
        """
        extract = tldextract.TLDExtract(suffix_list_url=False)
        ext = extract(domain)._asdict()

        # ext = tldextract.extract(domain)._asdict()

        return tools.log_json(ext, 4)
