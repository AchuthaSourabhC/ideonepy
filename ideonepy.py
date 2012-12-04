from SOAPpy import WSDL
import time


class ideone:
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

    """Create a submission and returns a dict containing the result"""
    def submit(self, lang, code, inp, run, private ):

        wsdlObject = WSDL.Proxy(self.url)

        response = wsdlObject.createSubmission(self.data['user'], self.data['pass'],
     code, lang, inp, run, private)
        link = response['item'][1]['value']

        result = wsdlObject.getSubmissionStatus(self.data['user'], self.data['pass'], link)
        r = result['item'][1]
        t = r.value

        while t != 0:
            time.sleep(3.0)
            result = wsdlObject.getSubmissionStatus(self.data['user'], self.data['pass'], link)
            r = result['item'][1]
            t = r.value

        output = wsdlObject.getSubmissionDetails(self.data['user'], self.data['pass'], link, True,
                True, True, True)
        reslink = 'http://ideone.com/' + link
        res = {'link': reslink}

        #creating dict containing the result of the submission
        for item in output['item']:
            res[item['key']] = item.value

        return res
