import logging
import textwrap

import requests


class HttpFormatter(logging.Formatter):
    def _formatHeaders(self, d):
        return '\n'.join(f'{k}: {v}' for k, v in d.items())

    def formatMessage(self, record):
        result = super().formatMessage(record)
        if record.name == 'httplogger':
            result += textwrap.dedent('''
                ---------------- request ----------------
                {req.method} {req.url}
                {reqhdrs}
                {req.body}
                ---------------- response ----------------
                {res.status_code} {res.reason} {res.url}
                {reshdrs}
                {res.text}
            ''').format(
                req=record.req,
                res=record.res,
                reqhdrs=self._formatHeaders(record.req.headers),
                reshdrs=self._formatHeaders(record.res.headers),
            )
        return result


formatter = HttpFormatter('{asctime} {levelname} {name} {message}', style='{')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logging.basicConfig(level=logging.DEBUG, handlers=[handler])
logger = logging.getLogger('httplogger')


def logRoundtrip(response, *args, **kwargs):
    extra = {'req': response.request, 'res': response}
    logger.debug('HTTP roundtrip', extra=extra)


session = requests.Session()
session.hooks['response'].append(logRoundtrip)
session.get('http://secariolabs.com')


# https://secariolabs.com/logging-raw-http-requests-in-python/