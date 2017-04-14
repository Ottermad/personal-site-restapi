"""Utils file."""
import requests


def forward_request_to_service(request, service, endpoint):
    """Forward incoming request to a Service and then returns the result."""
    url = "{}{}".format(service.host, endpoint)
    request_method = getattr(requests, request.method.lower())
    headers = dict(request.headers)

    # if current_identity._get_current_object() is not None:
    #     headers['User-Id'] = str(current_identity['id'])

    params = request.args
    resp = request_method(url, params=params, json=request.json,
                          headers=headers)
    return resp.text, resp.status_code
