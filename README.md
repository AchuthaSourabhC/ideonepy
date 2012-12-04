ideonepy
========

1. Create an object of class 'ideone' with 
    username and password(not account API password ) 
2. Use the object to call 'submit' method with
    > code of language to use given in ideone api
    > code to submit
    > input
    > run -true or false whether to run the code
    > private -true or false whether the code is private or public
3. Need to install SoapPy to use this => pip install soappy   

Example usage
-------------
    `
    from ideonepy import ideone


    source = """
    #include<iostream>
    using namespace std;
    int main(){
        int a;
        cin>>a;
        cout<<"Python rocks = "<<a;
        return 0;
        }
    """

    obj = ideone('xxxx', 'xxxxxxx')
    items = obj.submit(1, source, 1, True, False)
    print items
`

Output:
------
    ` 
      {'status': 0, 'memory': 2728, 'langName': 'C++', 'output': 'Python rocks = 1', 'signal': 0, 'error': 
    'OK', 'langId': 1, 'source': '\n#include<iostream>\nusing namespace std;\nint main(){\n    int a;\n    
    cin>>a;\n    cout<<"Python rocks = "<<a;\n    return 0;\n    }\n', 'link': 'http://ideone.com/MCODJM', 
    'result': 15, 'stderr': '', 'time': 0.01, 'date': '2012-12-04 14:23:49', 'input': '1', 'langVersion': 
    'gcc-4.3.4', 'public': True}
    `