from suds.client import Client
from suds.xsd.doctor import ImportDoctor, Import
import time
import os


class ideone(object):
    def __init__(self, user, passwd,
        url='http://ideone.com/api/1/service.wsdl'):
        
        self.url = url

        #contains data for submission
        self.data = {
                    'user': user, 'pass': passwd, 'lang': 1,
                    'code': '', 'input': 0, 'run': True, 'private': False
                    }
        self.c = Client(self.url, cache=None,
            doctor=ImportDoctor(Import
                ('http://schemas.xmlsoap.org/soap/encoding/')
                    ))
        #contains what all status codes mean
        self.status = {
                        0: 'Success', 1: 'Compiled',
                        3: 'Running', 11: 'Compilation Error',
                        12: 'Runtime Error', 13: 'Timelimit exceeded',
                        15: 'Success', 17: 'memory limit exceeded',
                        19: 'illegal system call', 20: 'internal error'
                        }
        self.error = {'status': 'error', 'output': 'Something went wrong :('}
    
    """Converts a list to String and returns it"""
    def tostr(self, elm):
        s = str(elm).strip('[]')
        return s

    """Creates and returns a Dictionary from response"""
    def createDict(self, output):
        result = {}
        for res in output.item:
            result[self.tostr(res.key)] = self.tostr(res.value)
        return result

    """ Dict of languages and their codes"""
    def languages(self):
        cl = self.c.service.getLanguages('srb51', 'my1stIdeone')
        result = {}
        langlist = cl.item[1].value[0].item
        for res in langlist:
            key = str(res.key).strip('[]')
            value = str(res.value).strip('[]')
            result[value] = key
        return result


    """Create a submission, gets the submission status and details
         and returns a dict containing the result"""
    def submit(self, lang=1, code='', inp=0, run=True, private=False):
        #Submit and get link and error status
        response = self.c.service.createSubmission(self.data['user'],
            self.data['pass'], code, lang,
                 inp, run, private)

        link = self.tostr(response.item[1].value)
        error = self.tostr(response.item[0].value)
        
        #check status of submission if no error
        if error == 'OK':
            sub = self.c.service.getSubmissionStatus(self.data['user'],
                self.data['pass'], link)
            status = self.tostr(sub.item[1].value)
            while status != '0':
                time.sleep(2.0)
                sub = self.c.service.getSubmissionStatus(self.data['user'],
                    self.data['pass'], link)
                status = self.tostr(sub.item[1].value)
        
        #Get the output for submission and return the dict
        resDict = {}
        output = self.c.service.getSubmissionDetails(self.data['user'],
            self.data['pass'], link, True,
                True, True, True)
        reslink = 'http://ideone.com/' + link

        resDict = self.createDict(output)
        resDict['link'] = reslink #url of the result page
        return resDict