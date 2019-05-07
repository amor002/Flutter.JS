import re, regex, os
from sys import argv
from xml.etree.ElementTree import fromstring


#add your custom if wanted
SYNTAX_SIMPLE = {
    'function': '',
    'let': 'var',
    'instanceof': 'is',
    'NaN': '0/0',
    'parseInt': 'int.parse',
    'parseFloat': 'double.parse',
    'Math.PI': 'Math.pi',
    '===': '==',
    'console.log': 'print',


}


# add more if you want
NO_CHILDS_WIDGETS = [ # fields that has no child arg
    'Text',
    'TextField',
    'TextFormField',
    'AssetImage',
    'Icon',
    'IconButton',
    'NetworkImage',
    'Image.asset',
    'Image.network',
    'FadeInImage',
    'FadeInImage.assetNetwork',
    'FadeInImage.memoryNetwork',

]

# syntax_complex
typeOf = lambda code: re.sub(r'typeof(\s+)+((\w+)|(("|\')\w+("|\')))', r'\2.runtimeType', code)
async = lambda code: re.sub(r'async (\s+)*(([A-Za-z0-9_]+)*)(\s+)*\((\s+)*((.*)*)(\s+)*\)', r'\2(\6) async',code)
Super = lambda code: re.sub(r'{(\s+)*(\n)*(\s+)*super\((.*)\)', r':super(\4) {\n', code)
constructor = lambda code: re.sub(r'class(\s+)(\w+)(.*?){(.*?)constructor', r'class\1\2\3{\4\2', code, flags=re.DOTALL)
default_args = lambda code: regex.sub(r'(\w+)(\s+)*\((\s+)*((\w+)(\s+)*=(\s+)*(.*))+(\s+)*\)(\s+)*{',
     r'\1({\4}) {', code)
Import = lambda code: re.sub(r'import(\s+)(\'|")(.*)\.js(\'|")', r'import \2\3.dart\4', code)
setTimeout = lambda code: re.sub(r'setTimeout(\s+)*\((.*?),(.*?)\)(\s+)*;', r'Future.delayed(Duration(milliseconds:\3), \2);', code, flags=re.DOTALL)


def add2string(code):
    res = re.sub(r'("|\')(\s+)*\+(\s+)*(\w+)', r'${\4}\1', code)
    res = re.sub(r'(\w+)(\s+)*\+(\s+)*("|\')', r'\4${\1}', res)
    return res


def args(code):
    
    res = re.findall(r'\((\s+)*(\w+)(\s+)*=(\s+)*([A-Za-z0-9_]+|\-?\d+)', code)
    res += re.findall(r',(\s+)*(\w+)(\s+)*=(\s+)*([A-Za-z0-9_]+|\-?\d+)', code)
    res += re.findall(r'\((\s+)*(\w+)(\s+)*=(\s+)*("(.*)")', code)
    res += re.findall(r'\((\s+)*(\w+)(\s+)*=(\s+)*(\'(.*)\')', code)
    
    kwargs = {}
    
    if res:
        for i in res:
            kwargs[i[1]] = i[4]

        for arg in kwargs:
            code = re.sub(r'(%s)(\s+)*=(\s+)*(%s)'%(arg, kwargs[arg]), r'\1:\4', code)
    return code
        

def convert2dart(js_code):
    for syntax in SYNTAX_SIMPLE:
        js_code = js_code.replace(syntax, SYNTAX_SIMPLE[syntax])

    return convertReact(
        Import(
            setTimeout(
                add2string(
                    constructor(
                        Super(
                            args(
                                default_args(
                                    typeOf(
                                        async(
                                            js_code))))))))))

def component2widget(components, parent=None, first_parent=False):

    for component in components:
        component.parent = parent

    if parent.tag == 'Scaffold':

        return 'Scaffold(\n\t%s %s)'%(','.join(':'.join([component.tag, component2widget(
            component.getchildren(), parent=component, first_parent=False
        )]) for component in components) + ("," if parent.items() else ""), ','.join([':'.join(item) for item in parent.items()]))


    if parent.tag in NO_CHILDS_WIDGETS:
        
        if parent.tag == 'IconButton':
            return "%s(icon: %s, %s)"%(parent.tag, component2widget(parent.getchildren()[0].getchildren(),
             parent=parent.getchildren()[0], first_parent=False), ',\n\t'.join([':'.join(item) for item in parent.items()]))
        
        if parent.text == None:
            for i in parent.items():
                if i[0] == 'value':
                    value = i[1]
                    break
            return "%s(%s, %s)"%(parent.tag, value, ',\n\t'.join([':'.join(item) if item[0] != 'value' else '' for item in parent.items()]))

        return "%s('%s', %s)"%(parent.tag, parent.text, ',\n\t'.join([':'.join(item) for item in parent.items()]))

    if len(components) > 1 and parent.tag != 'appBar':

        return "%s(children: [%s], %s)"%(parent.tag,
                                         ',\n\t'.join([component2widget(component,
                                                                    parent=component,
                                                                    first_parent=False) for component in components]),
                                         ',\n\t'.join([':'.join(item) for item in parent.items()]))


    try:
        if parent.parent.tag == 'Scaffold':
            if parent.tag == 'appBar':
                return 'AppBar(%s %s)'%(
                    ',\n\t'.join([':'.join([component.tag, component2widget(
                        component.getchildren()[0].getchildren(),
                        parent=component.getchildren()[0],first_parent=False)]
                         ) if component.tag != 'actions' else 'actions:[%s]'%(
                         ','.join([component2widget(comp.getchildren(),
                            parent=comp,first_parent=False
                            ) for comp in component.getchildren()]) 

                         ) for component in components])+\
                         (",\n\t" if parent.items() else ""), ',\n\t'.join([':'.join(item) for item in parent.items()]))

            return '%s'%(component2widget(components[0].getchildren(), parent=components[0], first_parent=False))
    except:
        pass

    if len(components) == 0:
        return '%s(%s)'%(parent.tag, ',\n\t'.join([':'.join(item) for item in parent.items()]))
    return '%s(%s %s)'%(parent.tag,
                        ("child: \n\t"+component2widget(components[0].getchildren(),
                                                    parent=components[0],
                                                    first_parent=False)+",")
                        if len(components) > 0 else "",
                        ',\n\t'.join([':'.join(item) for item in parent.items()]))



def convertReact(code):
    
    widgets = re.findall(r'<(\s+)*(\w+)(\s+)+((\w+)(\s+)*=(\s+)*{(.*)})(\s+)*(>|/>)', code)
    widgets += re.findall(r'<(\s+)*(\w+\.\w+)(\s+)+((\w+)(\s+)*=(\s+)*{(.*)})(\s+)*(>|/>)', code)

    for widget in widgets:
        partitions = widget[3].split('=')
        for i in range(len(partitions)):

            partitions[i] =partitions[i].replace(r'"', "'")
            partitions[i] = re.sub(r'{(.*)}', r'"\1"', partitions[i], count=1)

        correction = '='.join(partitions)
        code = code.replace(widget[3], correction)


    forms = re.findall(r'(<(\w+)(.*?)>)(.*?)(</\2>)', code, re.DOTALL)
    for form in forms:

        form = list(form)
        form.pop(2)
        form.pop(1)
        
        try:
            component = fromstring(''.join(form))
        except:
            print 'error while compiling react'
            print '*'*50
            print ''.join(form)
            print '*'*50
        widget =component2widget(component.getchildren(), parent=component, first_parent=True)
        code = code.replace(''.join(form), widget)

    return code


def create_dart_files(files):
    dart_files = []
    for i in range(len(files)):
        
        with open('javascript/'+files[i], 'r') as js_file:
            dart_code = convert2dart(js_file.read())

        with open('lib/'+files[i].split('.')[0]+'.dart', 'w+') as new_dart_file:
            new_dart_file.write(dart_code)


        




if __name__ == '__main__':
    files = []
    for file in os.listdir('javascript'):
        if file.endswith('.js'):
            files += [file]

    create_dart_files(files)

    for arg in argv:
        if arg == '--run':
            os.system('flutter run')

    



