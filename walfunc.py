directory=''
prompt='prelude'
functionsbase = {
    'else': {
        'args':[],
        'value': {
            'True':'True'
            }
        }
    }
functions = functionsbase

def evalexp(exp):
    while '#' in exp:
        s=exp.find('#')
        e=exp.find('#', s+1)
        exp=exp[:s]+str(evalfunc(exp[s:e+1]))+exp[e+1:]
    return eval(exp)#, {'__builtins__': [True,False]})

def evalfunc(func):
    func=func.strip('#')
    func=func.split('}')[:-1]
    arg=func[1:]
    com=func[0]
    for x in range(len(arg)):
        arg[x]=evalexp(arg[x])

    farg = functions[com]['args']

    argmap={}
    for x in range(len(farg)):
        argmap['$'+farg[x]+'$']=arg[x]
    for key in functions[com]['value']:
        pseudokey=key
        for x in argmap:
            pseudokey = pseudokey.replace(x, str(argmap[x]))
            #print 'key: '+key
            #print 'pseudokey: '+pseudokey

        if evalexp(pseudokey)==True:
            #print 'pseudokey True'
            #print 'value output: '+functions[com]['value'][key]
            exp=functions[com]['value'][key]
            break

    for x in argmap:
        exp = exp.replace(x, str(argmap[x]))

    return(evalexp(exp))

def evalcom(com):
    global directory, prompt
    if com[0]==':':
        com = com[1:]
        args=com.split(' ')[1:]
        com=com.split(' ')[0]
        #if com=='type' or com == 't':
        #    return type(args[0])
        if com == 'cd':
            directory=args[0].replace('\\','/')
            if directory[-1]!='/':
                directory=directory+'/'
            return('Directory changed to '+directory)
        elif com == 'load' or com == 'l':
            build(open(directory+args[0]).read().replace('\n','').replace('\t',''))
            prompt='main*'
            return('File '+directory+args[0]+' loaded')
        elif com == 'unload' or com == 'u':
            functions=functionsbase
            prompt = 'prelude'
            return('All modules unloaded')
        else:
            return('Unrecognized command')
    else:
        return evalfunc(com)

def build(c):
    c=c.split(';')[:-1]
    for x in c:
        x=x.split(':=')
        com=x[0].split('}')[0]
        arg=x[0].split('}')[1:-1]
        x[1]=x[1].split(',')
        for i in range(len(x[1])):
            x[1][i]=x[1][i].split(':')

        functions[com]={}
        functions[com]['args']=arg
        functions[com]['value']={}

        for i in range(len(x[1])):
            functions[com]['value'][x[1][i][0]]=x[1][i][1]

while True:
    print(evalcom(raw_input(prompt+'> ')))
