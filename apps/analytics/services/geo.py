"""
Geo lookup via ipinfo.io.

Free tier returns:
  ip, country (code), country_name, continent, continent_name,
  asn, as_name, as_domain

We do NOT cache — every visit triggers a lookup.
If the daily/monthly limit is hit, fields come back blank,
but the visit is still recorded.
"""

import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)

IPINFO_TIMEOUT = 3  # seconds — don't block requests long


def lookup_ip(ip: str) -> dict:
    """
    Return a dict with the geo fields we care about.
    Missing fields are empty strings.
    Never raises — returns blanks on any error.
    """
    blank = {
        'country':      '',
        'country_code': '',
        'continent':    '',
        'region':       '',
        'city':         '',
        'postal':       '',
        'coordinates':  '',
        'asn':          '',
        'as_name':      '',
        'as_domain':    '',
        'as_type':      '',
        'hostname':     '',
    }

    if not ip or ip in ('127.0.0.1', '::1'):
        return blank

    token = getattr(settings, 'IPINFO_TOKEN', '').strip()
    url = f"https://api.ipinfo.io/lite/{ip}"
    params = {'token': token} if token else {}

    try:
        resp = requests.get(url, params=params, timeout=IPINFO_TIMEOUT)
        if resp.status_code == 429:
            logger.warning("ipinfo.io rate limit reached")
            return blank
        if resp.status_code != 200:
            logger.warning("ipinfo.io returned %s", resp.status_code)
            return blank

        data = resp.json()

        # ipinfo returns country as "ZA" — map to full name
        country_code = data.get('country', '') or ''
        country_name = data.get('country_name', '') or ''

              # Lite API returns: country (full name), country_code (2-letter),
        # continent (full name), continent_code (2-letter), asn, as_name, as_domain
        return {
            'country':      data.get('country', '') or '',
            'country_code': data.get('country_code', '') or '',
            'continent':    data.get('continent', '') or '',

            # Not provided by Lite — stay blank
            'region':       '',
            'city':         '',
            'postal':       '',
            'coordinates':  '',

            'asn':          data.get('asn', '') or '',
            'as_name':      data.get('as_name', '') or '',
            'as_domain':    data.get('as_domain', '') or '',
            'as_type':      '',
            'hostname':     '',
        }

    except requests.RequestException as e:
        logger.warning("ipinfo.io request failed: %s", e)
        return blank
    except Exception as e:
        logger.exception("Unexpected error in lookup_ip: %s", e)
        return blank