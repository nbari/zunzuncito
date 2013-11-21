import re

# if (preg_match('#^\*\.#', $domain)) {
# * match subdomains excluding @ or domains starting with . or /

# $pattern = '#^(?:[^./@]+\.)*' . str_replace(array('*.','.'), array('','\.'), $domain) . '$#';

hosts = {}
hosts['*'] = []
hosts['*.site.tld'] = []
hosts['www.site.tld'] = []

routes = {}
routes['*'] = []
routes['*.site.tld'] = []
routes['www.site.tld'] = []


HTTP_HOST = 'ftp.site.tld:8080'

host = HTTP_HOST.split(':')[0]
sites = [k for k in sorted(routes, key=len, reverse=True)]

sites = routes.keys()
print host , '--->', sites

if host in sites:
    site = host
else:
    for s in sites:
        if re.match('^\*\.', s):
            domain = '^(?:[^./@]+\.)*%s$' % s.replace('*.', '').replace('.', '\.')
            if re.match(domain, s):
                site = s
                break

print s
