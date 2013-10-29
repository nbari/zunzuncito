"""
HTTP status codes. see rfc2817
source http://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml
"""

# 1xx: Informational - Request received, continuing process
HTTP_100 = '100 Continue' # [RFC2616]
HTTP_101 = '101 Switching Protocols' # [RFC2616]
HTTP_102 = '102 Processing' # [RFC2518]

# 2xx: Success - The action was successfully received, understood, and accepted
HTTP_200 = '200 OK' # [RFC2616]
HTTP_201 = '201 Created' # [RFC2616]
HTTP_202 = '202 Accepted' # [RFC2616]
HTTP_203 = '203 Non-Authoritative Information' # [RFC2616]
HTTP_204 = '204 No Content' # [RFC2616]
HTTP_205 = '205 Reset Content' # [RFC2616]
HTTP_206 = '206 Partial Content' # [RFC2616]
HTTP_207 = '207 Multi-Status' # [RFC4918]
HTTP_208 = '208 Already Reported' # [RFC5842]
HTTP_226 = '226 IM Used' # [RFC3229]

# 3xx: Redirection - Further action must be taken in order to complete the request
HTTP_300 = '300 Multiple Choices' # [RFC2616]
HTTP_301 = '301 Moved Permanently' # [RFC2616]
HTTP_302 = '302 Found' # [RFC2616]
HTTP_303 = '303 See Other' # [RFC2616]
HTTP_304 = '304 Not Modified' # [RFC2616]
HTTP_305 = '305 Use Proxy' # [RFC2616]
HTTP_306 = '306 Reserved' # [RFC2616]
HTTP_307 = '307 Temporary Redirect' # [RFC2616]
HTTP_308 = '308 Permanent Redirect' # [RFC-reschke-http-status-308-07]

# 4xx: Client Error - The request contains bad syntax or cannot be fulfilled
HTTP_400 = '400 Bad Request' # [RFC2616]
HTTP_401 = '401 Unauthorized' # [RFC2616]
HTTP_402 = '402 Payment Required' # [RFC2616]
HTTP_403 = '403 Forbidden' # [RFC2616]
HTTP_404 = '404 Not Found' # [RFC2616]
HTTP_405 = '405 Method Not Allowed' # [RFC2616]
HTTP_406 = '406 Not Acceptable' # [RFC2616]
HTTP_407 = '407 Proxy Authentication Required' # [RFC2616]
HTTP_408 = '408 Request Timeout' # [RFC2616]
HTTP_409 = '409 Conflict' # [RFC2616]
HTTP_410 = '410 Gone' # [RFC2616]
HTTP_411 = '411 Length Required' # [RFC2616]
HTTP_412 = '412 Precondition Failed' # [RFC2616]
HTTP_413 = '413 Request Entity Too Large' # [RFC2616]
HTTP_414 = '414 Request-URI Too Long' # [RFC2616]
HTTP_415 = '415 Unsupported Media Type' # [RFC2616]
HTTP_416 = '416 Requested Range Not Satisfiable' # [RFC2616]
HTTP_417 = '417 Expectation Failed' # [RFC2616]
HTTP_422 = '422 Unprocessable Entity' # [RFC4918]
HTTP_423 = '423 Locked' # [RFC4918]
HTTP_424 = '424 Failed Dependency' # [RFC4918]
HTTP_425 = '425 Unassigned'
HTTP_426 = '426 Upgrade Required' # [RFC2817]
HTTP_427 = '427 Unassigned'
HTTP_428 = '428 Precondition Required' # [RFC6585]
HTTP_429 = '429 Too Many Requests' # [RFC6585]
HTTP_430 = '430 Unassigned'
HTTP_431 = '431 Request Header Fields Too Large' # [RFC6585]

# 5xx: Server Error - The server failed to fulfill an apparently valid request
HTTP_500 = '500 Internal Server Error' # [RFC2616]
HTTP_501 = '501 Not Implemented' # [RFC2616]
HTTP_502 = '502 Bad Gateway' # [RFC2616]
HTTP_503 = '503 Service Unavailable' # [RFC2616]
HTTP_504 = '504 Gateway Timeout' # [RFC2616]
HTTP_505 = '505 HTTP Version Not Supported' # [RFC2616]
HTTP_506 = '506 Variant Also Negotiates (Experimental)' # [RFC2295]
HTTP_507 = '507 Insufficient Storage' # [RFC4918]
HTTP_508 = '508 Loop Detected' # [RFC5842]
HTTP_509 = '509 Unassigned'
HTTP_510 = '510 Not Extended' # [RFC2774]
HTTP_511 = '511 Network Authentication Required' # [RFC6585]
