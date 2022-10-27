from django.conf import settings


class CrossDomainSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.cookies:
            host = request.get_host()
            if settings.SESSION_COOKIE_NAME in response.cookies.values():
                session_cookie = response.cookies[settings.SESSION_COOKIE_NAME]
                default_session_domain = session_cookie['domain']
                if host in settings.SR_SESSION_COOKIE_DOMAINS:
                    session_cookie['domain'] = host
                # print(session_cookie['domain'])
                # print(host)
                
            # print(f"host! {host}")
            # # check if it's a different domain
            # if host not in settings.SESSION_COOKIE_DOMAIN:
            #     domain = ".{domain}".format(domain=host)
                
            #     for cookie in response.cookies:
            #         if 'domain' in response.cookies[cookie]:
            #             print(f"found! {domain}")
            #             response.cookies[cookie]['domain'] = domain
        return response
