# -*- coding: utf-8 -*-
import urllib, httplib
import json
import re
import time

class Token(object):
    def __init__(self, client_id, client_secret):
        self.client_id = client_id;
        self.client_secret = client_secret
        self.init = True
        self.token = None

    def getToken(self, re_init=False):
        if not self.init and not re_init:
            if time.time() - self.start_time < 580:
                return self.token
        self.init = False
        self.start_time = time.time()
        params = urllib.urlencode({'client_id': self.client_id, 'client_secret': self.client_secret,
                'scope': "http://api.microsofttranslator.com", "grant_type":"client_credentials"})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

        conn = httplib.HTTPSConnection("datamarket.accesscontrol.windows.net")
        conn.request("POST", "/v2/OAuth2-13", params)
        rs = json.loads ( conn.getresponse().read() )
        self.token = rs[u'access_token']
        return self.token

class BingTranslator(object):
    def __init__(self, client_id, client_secret):
        self.token_obj = Token(client_id, client_secret)

    def unicode2utf8(self, text):
        try:
            if isinstance(text, unicode):
                text = text.encode('utf-8')
        except Exception as (e, msg):
            print e, msg
            pass
        return text

    def getText(self, xml):
        text = re.sub(r"<.+?>", " ", xml).strip()
        return text

    def getTranslation(self, text, src, tgt, reinit_token = False):
        token = self.token_obj.getToken(reinit_token)
        headers = {'Authorization':'bearer %s' % token}
        conn = httplib.HTTPConnection('api.microsofttranslator.com')
        dic = {}
        dic['from'] = src
        dic['to'] = tgt
        dic['text'] = self.unicode2utf8(text)
        addr = '/V2/Http.svc/Translate?' + urllib.urlencode(dic)
        conn.request("GET", addr, headers=headers)
        xml = conn.getresponse().read()
        return self.getText(xml)

if __name__ == "__main__":
    client_id = ""
    client_secret = ""
    translator = BingTranslator (client_id, client_secret)
    print translator.getTranslation ("""We can read of things that happened 5,000 years ago in the Near East.""", "en", "de")
