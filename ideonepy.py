from SOAPpy import WSDL
import time


class ideone(object):
    def __init__(self, user, passwd):
        self.url = 'http://ideone.com/api/1/service.wsdl'

        #contains data for submission
        self.data = {
                        'user': user, 'pass': passwd, 'lang': 1,
                        'code': '', 'input': 0, 'run': True, 'private': False
                        }

        #contains what all status codes mean
        self.status = {
                            0: 'Success', 1: 'Compiled',
                            3: 'Running', 11: 'Compilation Error',
                            12: 'Runtime Error', 13: 'Timelimit exceeded',
                            15: 'Success', 17: 'memory limit exceeded',
                            19: 'illegal system call', 20: 'internal error'
                            }
        self.error = {'status': 'error', 'output': 'Something went wrong :('}

    """Creates a Dictionary from soappy response"""
    def createDict(self, response):
        #creating dict containing the result of the submission
        res = {}
        for item in response['item']:
            res[item['key']] = item.value
        return res

    """ Dict of languages and their codes"""
    def languages(self):
        wsdlObject = WSDL.Proxy(self.url)
        langs = {}
        resp = wsdlObject.getLanguages(self.data['user'], self.data['pass'])
        for item in resp['item'][1]['value']['item']:
            langs[item['key']] = item.value
        return langs

    def create_submission(self, lang=1, code='', inp=0,
        run=True, private=False):
        wsdlObject = WSDL.Proxy(self.url)
        response = wsdlObject.createSubmission(self.data['user'],
            self.data['pass'], code, lang,
                 inp, run, private)
        sub = self.createDict(response)
        return sub

    """Create a submission, gets the submission status and details
         and returns a dict containing the result"""
    def submit(self, lang=1, code='', inp=0, run=True, private=False):

        wsdlObject = WSDL.Proxy(self.url)

        response = wsdlObject.createSubmission(self.data['user'],
            self.data['pass'], code, lang,
                 inp, run, private)
        link = response['item'][1]['value']

        result = wsdlObject.getSubmissionStatus(self.data['user'],
            self.data['pass'], link)
        r = result['item'][1]
        t = r.value

        while t != 0:
            time.sleep(3.0)
            result = wsdlObject.getSubmissionStatus(self.data['user'],
                self.data['pass'], link)
            r = result['item'][1]
            t = r.value

        output = wsdlObject.getSubmissionDetails(self.data['user'],
            self.data['pass'], link, True,
                True, True, True)
        reslink = 'http://ideone.com/' + link

        res = self.createDict(output)
        res['link'] = reslink
        return res
