
def error(message, r=False, is_exit=False):
    string = '\033[91m%s\033[0m' % (message)
    if r:
        return string
    print(string)
    if is_exit:
        exit()
    

def success(message, r=False, is_exit=False):
    string = '\033[92m%s\033[0m' % (message)
    if r:
        return string
    print(string)
    if is_exit:
        exit()

def info(message, r=False, is_exit=False):
    string = '\033[93m%s\033[0m' % (message)
    if r:
        return string
    print(string)
    if is_exit:
        exit()
        
        
def title():
    print('\033[95m'+"""
    ***************************************************************************************
    *                                                                                     *
    *                         NGINX SIMPLE VIRTUAL HOST CREATOR                           *
    *                              For Ubuntu machines                                    *
    *                                                                                     *
    ***************************************************************************************
    """+'\033[0m')
