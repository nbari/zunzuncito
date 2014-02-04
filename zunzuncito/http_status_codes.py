"""
HTTP status codes. see rfc2817
source http://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml
"""

codes = {
# 1xx: Informational - Request received, continuing process
    100: '100 Continue', # [RFC2616]
    101: '101 Switching Protocols', # [RFC2616]
    102: '102 Processing', # [RFC2518]

# 2xx: Success - The action was successfully received, understood, and accepted
    200: '200 OK', # [RFC2616]
    201: '201 Created', # [RFC2616]
    202: '202 Accepted', # [RFC2616]
    203: '203 Non-Authoritative Information', # [RFC2616]
    204: '204 No Content', # [RFC2616]
    205: '205 Reset Content', # [RFC2616]
    206: '206 Partial Content', # [RFC2616]
    207: '207 Multi-Status', # [RFC4918]
    208: '208 Already Reported', # [RFC5842]
    226: '226 IM Used', # [RFC3229]

# 3xx: Redirection - Further action must be taken in order to complete the request
    300: '300 Multiple Choices', # [RFC2616]
    301: '301 Moved Permanently', # [RFC2616]
    302: '302 Found', # [RFC2616]
    303: '303 See Other', # [RFC2616]
    304: '304 Not Modified', # [RFC2616]
    305: '305 Use Proxy', # [RFC2616]
    306: '306 Reserved', # [RFC2616]
    307: '307 Temporary Redirect', # [RFC2616]
    308: '308 Permanent Redirect', # [RFC-reschke-http-status-308-07]

# 4xx: Client Error - The request contains bad syntax or cannot be fulfilled
    400: '400 Bad Request', # [RFC2616]
    401: '401 Unauthorized', # [RFC2616]
    402: '402 Payment Required', # [RFC2616]
    403: '403 Forbidden', # [RFC2616]
    404: '404 Not Found', # [RFC2616]
    405: '405 Method Not Allowed', # [RFC2616]
    406: '406 Not Acceptable', # [RFC2616]
    407: '407 Proxy Authentication Required', # [RFC2616]
    408: '408 Request Timeout', # [RFC2616]
    409: '409 Conflict', # [RFC2616]
    410: '410 Gone', # [RFC2616]
    411: '411 Length Required', # [RFC2616]
    412: '412 Precondition Failed', # [RFC2616]
    413: '413 Request Entity Too Large', # [RFC2616]
    414: '414 Request-URI Too Long', # [RFC2616]
    415: '415 Unsupported Media Type', # [RFC2616]
    416: '416 Requested Range Not Satisfiable', # [RFC2616]
    417: '417 Expectation Failed', # [RFC2616]
    422: '422 Unprocessable Entity', # [RFC4918]
    423: '423 Locked', # [RFC4918]
    424: '424 Failed Dependency', # [RFC4918]
    425: '425 Unassigned',
    426: '426 Upgrade Required', # [RFC2817]
    427: '427 Unassigned',
    428: '428 Precondition Required', # [RFC6585]
    429: '429 Too Many Requests', # [RFC6585]
    430: '430 Unassigned',
    431: '431 Request Header Fields Too Large', # [RFC6585]

# 5xx: Server Error - The server failed to fulfill an apparently valid request
    500: '500 Internal Server Error', # [RFC2616]
    501: '501 Not Implemented', # [RFC2616]
    502: '502 Bad Gateway', # [RFC2616]
    503: '503 Service Unavailable', # [RFC2616]
    504: '504 Gateway Timeout', # [RFC2616]
    505: '505 HTTP Version Not Supported', # [RFC2616]
    506: '506 Variant Also Negotiates (Experimental)', # [RFC2295]
    507: '507 Insufficient Storage', # [RFC4918]
    508: '508 Loop Detected', # [RFC5842]
    509: '509 Unassigned',
    510: '510 Not Extended', # [RFC2774]
    511: '511 Network Authentication Required', # [RFC6585]
}

# generic class responses as per RFC2616
# 6.1.1 Status Code and Reason Phrase
# http://www.ietf.org/rfc/rfc2616.txt
generic_reasons = {
    1: '100 Continue',
    2: '200 Success',
    3: '300 Multiple Choices',
    4: '400 Bad Request',
    5: '500 Internal Server Error'
}
