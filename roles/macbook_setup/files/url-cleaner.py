#!/usr/bin/env python3

from urllib.parse import urlparse, urljoin, parse_qs, urlunparse, urlencode
import re
import os
import sys


def remove_amazon_tracking(url):
    cleaned_url = ""

    try:
        parsed_url = urlparse(url)
    except ValueError:
        return url;

    if not re.match(".*amazon\..*", parsed_url.netloc, re.IGNORECASE):
        return url;

    # Strip the entire query string
    cleaned_url = urljoin(url, parsed_url.path)

    # Remove "ref=?" tokens from the path
    cleaned_url = re.sub(r'\/ref=.*', '', cleaned_url)

    return cleaned_url


def remove_utm_tracking(url):
    cleaned_url = ""

    try:
        parsed_url = urlparse(url)
    except ValueError:
        return url;

    common_utm_tokens = [
        'utm_source',
        'utm_medium',
        'utm_term',
        'utm_campaign',
        'utm_content',
        'utm_cid',
        'utm_reader'
    ]
    qs = parse_qs(parsed_url.query)
    for k in common_utm_tokens:
        qs.pop(k.lower(), None)

    # Rebuild the URL with the relevant tokens removed
    components = (parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, urlencode(qs, doseq=True), parsed_url.fragment)
    cleaned_url = urlunparse(components)

    return cleaned_url


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Usage: %s <url>' % sys.argv[0])
        sys.exit(1)

    input_url = sys.argv[1]
    input_url = remove_amazon_tracking(input_url)
    input_url = remove_utm_tracking(input_url)
    print(input_url.strip())
    sys.exit(0)
