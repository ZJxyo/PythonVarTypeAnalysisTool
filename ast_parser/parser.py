import ast
import os
import numpy as np
import json
from yattag import Doc
import matplotlib.pyplot as plt
import re
import graphviz
import glob

# TODO: write doc, include that you need to install yattag
# {class name: {function name: {var name: {line number: possible type}}}}
D = {}
C = {'Default': D}
L = {}
IdMap = {'Ambiguous': 'Ambiguous',
         '<class \'list\'>': 'List',
         '<class \'float\'>': 'Float',
         '<class \'str\'>': 'String',
         '<class \'int\'>': 'Integer',
         '<class \'tuple\'>': 'Tuple',
         '<class \'bool\'>': 'Boolean',
         '<class \'set\'>': 'Set',
         '<class \'dict\'>': 'Dictionary',
         'Error': 'Error',
         'Multiple': 'Multiple'
         }
errorMap = {}


def decode(obj):
    dup = {}
    for c in obj:
        dup[c] = {}
        for fn in obj[c]:
            dup[c][fn] = {}
            for var in obj[c][fn]:
                dup[c][fn][var] = {}
                for ln in obj[c][fn][var]:
                    if isinstance(ln, str):
                        val = obj[c][fn][var][ln]
                        s = set()
                        for tp in val:
                            if tp == str(int):
                                s.add(int)
                            elif tp == str(str):
                                s.add(str)
                            elif tp == str(float):
                                s.add(float)
                            elif tp == str(bool):
                                s.add(bool)
                            elif tp == str(list):
                                s.add(list)
                            elif tp == str(tuple):
                                s.add(list)
                            elif tp == str(set):
                                s.add(set)
                            elif tp == str(dict):
                                s.add(dict)
                            else:
                                print("something went wrong, check functions_return.json")
                        line_no = ln
                        try:
                            line_no = int(ln)
                        except:
                            pass
                        dup[c][fn][var][line_no] = s
    return dup


def main():
    with open(os.path.join('..', 'input_files', 'functions_return.json')) as in_file:
        libs = decode(json.load(in_file))

    for c in libs:
        C[c] = libs[c]

    file = os.path.join('..', 'input_files', 'input1.py')
    code = ""
    with open(file, 'r') as source:
        code = source.read()
    tree = ast.parse(code)
    analyzer = Analyzer()
    analyzer.visit(tree)

    htmlText = generateHighlightedCode(C['Default'], code.split('\n'))
    errorText = generateErrorReport(C['Default'], code.split('\n'))

    with open("../output/error_report/ErrorReport.html", "w") as file1:
        file1.writelines(errorText)

    with open("../output/analysis/analysis.html", "w") as file1:
        file1.writelines(htmlText)
    print(C)

    createFlowChart()
    groupPages()


def groupPages():
    doc, tag, text = Doc().tagtext()

    with tag('html'):
        with tag('body'):
            with tag('h2'):
                with tag('a', href='analysis/analysis.html'):
                    text("Type Analysis Highlighting")
                doc.stag('br')
                doc.stag('br')
            with tag('h2'):
                with tag('a', href='error_report/ErrorReport.html'):
                    text("Error Report")
                doc.stag('br')
                doc.stag('br')
            files = glob.glob('../output/flowchart/*')
            for f in files:
                if f.title().split(".")[-1] == "Html":
                    link = f.title().split("/")[-1].lower()
                    link = re.sub(r'\\', '/', link)
                    with tag('h2'):
                        with tag('a', href=link):
                            name = f.title().split("\\")[-1].split('.')[0].split('_')
                            text(name[0] + " for " + name[1].lower())
                        doc.stag('br')
                        doc.stag('br')

    result = doc.getvalue()

    with open(f"../output/Main.html", "w") as file1:
        file1.writelines(result)


def createFlowChart():
    files = glob.glob('../output/flowchart/*')
    for f in files:
        os.remove(f)

    for fn in D:
        lfn = []
        fn_s = fn.split("|")[0]
        fn_i = int(fn.split("|")[1])
        param = ''
        for i in range(fn_i + 1):
            param += ('arg' + str(i) + ',')

        fn_new = fn_s + '(' + param[0:(len(param) - 1)] + ')'
        for var in D[fn]:
            prev = None
            g = graphviz.Digraph(filename=f'../output/flowchart/flowchart_{fn_new}_{var}.gv', format='png')
            lfn.append(f'../output/flowchart/flowchart_{fn_new}_{var}.gv.png')
            if var == 'return':
                g.attr(label=f'Return Type')
            else:
                g.attr(label=f'Variable < {var} >')
            g.attr('node', shape='box')

            for ln_no in D[fn][var]:
                if ln_no < 0:
                    new_ln_no = "arg" + str(np.abs(ln_no) - 1)
                else:
                    new_ln_no = str(ln_no)
                tp_s = []
                if isinstance(D[fn][var][ln_no], set):
                    for tp in D[fn][var][ln_no]:
                        tp_s.append(IdMap[str(tp)])
                else:
                    tp_s.append(D[fn][var][ln_no])

                g.node(str(ln_no), new_ln_no + ": " + re.sub('\[|\]|\'', '', str(tp_s)))
                if prev is not None:
                    g.edge(prev, str(ln_no))
                prev = str(ln_no)

            g.render()

        for i in range(len(lfn)):
            lfn[i] = re.sub('../output/flowchart/', '', lfn[i])

        doc, tag, text = Doc().tagtext()

        with tag('html'):
            with tag('body'):
                with tag('h1'):
                    text("Function " + fn_new + " Type History")
                for fn in lfn:
                    doc.stag('img', src=fn)
                    doc.stag('br')
                    doc.stag('br')

        result = doc.getvalue()

        with open(f"../output/flowchart/flowchart_{fn_new}.html", "w") as file1:
            file1.writelines(result)


def generateHighlightedCode(typeMapping, codeList):
    doc, tag, text, line = Doc().ttl()
    lifetimeVariableMap = {}
    with tag('html'):
        with tag('head'):
            doc.stag('link', rel='stylesheet', href='analysis.css')
            doc.stag('link', rel='stylesheet', href='prism.css')
        with tag('body', klass='line-numbers'):
            with tag('script'):
                doc.attr(src='prism.js')
            highlightCodeLines(typeMapping, codeList, lifetimeVariableMap, doc, tag, text)
            with tag('ul', klass='legend'):
                for key in IdMap:
                    with tag('li'):
                        line('span', '', klass=IdMap[key])
                        text(IdMap[key])

    createGraphs(lifetimeVariableMap)
    return doc.getvalue()


def highlightCodeLines(typeMapping, codeList, lifetimeVariableMap, doc, tag, text):
    functionTypeMap = {}
    lineNumber = 1
    functionName = ''
    functionVariableMap = {}
    with tag('pre'):
        with tag('code', klass='language-python'):
            for code in codeList:
                codeSplit = code.split()
                if (len(codeSplit) > 0 and codeSplit[0] == 'def'):
                    functionName = codeSplit[1].split('(')[0]
                    numParameters = getNumParameters(code)
                    key = functionName + '|' + str(numParameters)
                    functionTypeMap = typeMapping[key]
                    functionVariableMap = {}

                    if ('return' in typeMapping[key]):
                        returnType = list(typeMapping[key]['return'].values())[0]

                        tagID = getClassIdFromType(returnType)
                        if (tagID == "Multiple"):
                            with tag('div', klass='tooltip'):
                                with tag('mark', klass=tagID):
                                    text(code)
                                with tag('span', klass='tooltiptext'):
                                    tooltipList = ''
                                    for varType in returnType:
                                        tooltipList = f'{tooltipList} {IdMap[str(varType)]}, '
                                    text(f'{tooltipList[:-2]} ')
                        else:
                            with tag('mark', klass=tagID):
                                text(code)
                    else:
                        text(code)
                elif len(codeSplit) > 0 and codeSplit[0] == '#':
                    text(f'{code}\n')
                    lineNumber += 1
                    continue
                else:
                    extractVariablesFromLine(code, functionTypeMap, lineNumber, functionVariableMap, doc, tag, text)
                    lifetimeVariableMap[functionName] = functionVariableMap
                lineNumber += 1
                text('\n')


# get all variables that exist in map and their indicies
def extractVariablesFromLine(codeLine, typeMap, lineNumber, functionVariableMap, doc, tag, text):
    printed = False
    for key in typeMap:
        if (lineNumber in typeMap[key]):
            typeOfVar = typeMap[key][lineNumber]
            codeSplitByEqual = codeLine.split('=')
            if (len(codeSplitByEqual) == 2):
                printed = True
                classId = getClassIdFromType(typeOfVar)
                locVar = codeSplitByEqual[0].index(key)
                variableName = codeSplitByEqual[0][locVar:locVar + len(key)]
                if (variableName in functionVariableMap):
                    functionVariableMap[variableName].append((lineNumber, typeOfVar))
                else:
                    functionVariableMap[variableName] = [(lineNumber, typeOfVar)]
                text(codeSplitByEqual[0][0:locVar])
                if (classId == "Multiple"):
                    with tag('div', klass='tooltip'):
                        with tag('mark', klass=classId):
                            text(variableName)
                        text(f'{codeSplitByEqual[0][locVar + len(key):]}={codeSplitByEqual[1]}')
                        with tag('span', klass='tooltiptext'):
                            tooltipList = ''
                            for varType in typeOfVar:
                                tooltipList = f'{tooltipList} {IdMap[str(varType)]}, '
                            text(f'{tooltipList[:-2]} ')
                else:
                    with tag('mark', klass=classId):
                        text(variableName)
                    text(f'{codeSplitByEqual[0][locVar + len(key):]}={codeSplitByEqual[1]}')
    if printed is False:
        text(codeLine)
        # TODO: support lines such as b = a = 35


def getClassIdFromType(typeOfVar):
    if isinstance(typeOfVar, set):
        if (len(typeOfVar) == 1):
            return IdMap[str(next(iter(typeOfVar)))]
        else:
            return "Multiple"
    elif isinstance(typeOfVar, str):
        return IdMap[typeOfVar]


def getNumParameters(codeSplit):
    methodName = codeSplit.split(" ", 1)[1]
    methodName = re.sub('\ ', '', methodName)
    if (len(methodName.split("(")[1]) == 2):
        return 0
    if (len(methodName.split(",")) == 1):
        return 1
    return len(methodName.split(","))


def createGraphs(lifetimeVariableMap):
    files = glob.glob('../output/type_history_scatter/*')
    for f in files:
        os.remove(f)

    for key in lifetimeVariableMap:
        methodVariables = lifetimeVariableMap[key]
        for variable in methodVariables:
            variableList = methodVariables[variable]
            lineNums = []
            typeVars = []
            y = list(IdMap.values())
            for tpl in variableList:
                typeVars.append(y.index(getClassIdFromType(tpl[1])))
                lineNums.append(tpl[0])
            # print(typeVars)
            fig, ax = plt.subplots(1, 1)
            ax.set_yticks(range(0, len(y)))
            ax.set_yticklabels(y)
            plt.title('Type History of Variable ' + '<' + variable + '>' + ' in method ' + key)
            plt.xlabel('Line Numbers')
            plt.ylabel('Type')

            plt.plot(lineNums, typeVars, '.')
            plt.savefig(f'../output/type_history_scatter/typeHistory-method-{key}-{variable}.png', bbox_inches='tight')


def generateErrorReport(typeMapping, codeList):
    doc, tag, text = Doc().tagtext()
    with tag('html'):
        with tag('head'):
            doc.stag('link', rel='stylesheet', href='error.css')
    with tag('body'):
        generateErrors(typeMapping, codeList, doc, tag, text)
    return doc.getvalue()


def generateErrors(typeMapping, codeList, doc, tag, text):
    functionTypeMap = {}
    lineNumber = 1
    with tag('code'):
        text("Error Log")
        for code in codeList:
            codeSplit = code.split()
            if (len(codeSplit) > 0 and codeSplit[0] == 'def'):
                functionName = codeSplit[1].split('(')[0]
                numParameters = getNumParameters(code)
                key = functionName + '|' + str(numParameters)
                functionTypeMap = typeMapping[key]
            elif len(codeSplit) > 0 and codeSplit[0] == '#':
                lineNumber += 1
                continue
            else:
                getErrorLineFromCode(code, functionTypeMap, lineNumber, doc, tag, text)
            lineNumber += 1
        for key in sorted(errorMap):
            with tag('p'):
                text(f"{str(key)}: {errorMap[key]}")


def getErrorLineFromCode(code, typeMap, lineNumber, doc, tag, text):
    printed = False
    for key in typeMap:
        if (lineNumber in typeMap[key]):
            typeOfVar = typeMap[key][lineNumber]
            codeSplitByEqual = code.split('=')
            if (len(codeSplitByEqual) == 2):
                printed = True
                classId = getClassIdFromType(typeOfVar)
                with tag('p', klass=classId):
                    locVar = codeSplitByEqual[0].index(key)
                    # text(codeSplitByEqual[0][0:locVar])
                    # with tag('mark'):
                    # text(codeSplitByEqual[0][locVar:locVar+len(key)])
                    # text(f'{codeSplitByEqual[0][locVar+len(key):]}={codeSplitByEqual[1]}')
                    if (typeOfVar == 'Ambiguous'):
                        errorMap[
                            lineNumber] = 'Warning, there may be any error on this line due to the ambigious nature of the variables'
                    if (typeOfVar == 'Error'):
                        errorMap[lineNumber] = 'Error, there is an error on this line caused by type mismatch'
    # if printed is False:
    # with tag('p'):
    # text(code)
    # TODO: support multiple
    # TODO: hover functionality if multiple types


class Analyzer(ast.NodeVisitor):
    # list of valid type
    valid_types = {int, str, float, bool, list, tuple, dict, set}
    var_name = None
    line_no = None
    fn_name = None
    bin_l = set()
    bin_r = set()
    bin_t = None

    def process_if(self, n):
        self.recurse_if(n, n.lineno)

    # covers if/elif/else
    def recurse_if(self, n, s):
        # checks the contents with if
        if hasattr(n, 'body'):
            for b in n.body:
                if isinstance(b, ast.If):
                    self.recurse_if(b, b.lineno)
                else:
                    self.recurse(b)
        # checks the contents within elif
        if hasattr(n, 'orelse'):
            if len(n.orelse) > 0:
                # len > 0 in the last else case
                for b in n.orelse:
                    if isinstance(b, ast.If):
                        self.recurse_if(b, n.lineno)
                    else:
                        self.recurse(b)

        for var in list(D[self.fn_name].keys()):
            for ln in list(D[self.fn_name][var].keys()):
                if ln in range(n.lineno, self.line_no + 1):
                    if self.line_no + 0.5 not in D[self.fn_name][var]:
                        keys = list(D[self.fn_name][var].keys())
                        dup = list(D[self.fn_name][var].keys())
                        for i in keys:
                            if i > s and len(dup) > 1:
                                dup.remove(i)
                        D[self.fn_name][var][self.line_no + 0.5] = D[self.fn_name][var][np.max(dup)]
                    D[self.fn_name][var][self.line_no + 0.5] = \
                        D[self.fn_name][var][self.line_no + 0.5] | D[self.fn_name][var][ln]

    # covers for var in range(#) loops
    # covers for var in [...] loops
    # covers else of for loop
    def process_for(self, n):
        self.var_name = n.target.id
        self.line_no = n.lineno
        self.dictionary_helper()

        self.traverse_list(n.body)
        self.traverse_list(n.orelse)

        self.var_name = n.target.id
        self.line_no = n.lineno
        self.process_list_for(n.iter)

    def process_list_for(self, n):
        for i in n.elts:
            self.recurse(i)

    # covers while loops
    # covers else of while loop
    def process_while(self, n):
        self.traverse_list(n.body)
        self.traverse_list(n.orelse)

    # covers try case, orelse of try, except of try, finally of try
    def process_try(self, n):
        self.traverse_list(n.body)
        self.traverse_list(n.orelse)
        self.process_except(n.handlers)
        self.traverse_list(n.finalbody)

    # processes the list of except handlers and their contents
    def process_except(self, eh):
        for e in eh:
            self.traverse_list(e.body)

    # processes contents within lists such as body and final orelse
    def traverse_list(self, lt):
        for b in lt:
            self.recurse(b)

    # unary operators on literals specifically boolean, int, float
    # unary operators on variables
    def process_unaryop(self, n):
        self.unary_helper(n, n.operand)
        # if isinstance(n.operand, ast.Constant):
        #     self.unary_helper(n, n.operand.value, "Constant", n.operand)
        # elif isinstance(n.operand, ast.Name):
        #     self.unary_helper(n, n.operand.id, "Name/Call", n.operand)
        # elif isinstance(n.operand, ast.Call):
        #     self.unary_helper(n, n.operand, "Name/Call", n.operand)
        # else:
        #     print("not an unary operator type")

    # switch between each of the four types of unary ops: -, +, ~, not
    def unary_helper(self, n, opt):
        if isinstance(n.op, ast.USub):
            self.unary_helper_helper("-", opt)
        elif isinstance(n.op, ast.UAdd):
            self.unary_helper_helper("+", opt)
        elif isinstance(n.op, ast.Invert):
            self.unary_helper_helper("~", opt)
        elif isinstance(n.op, ast.Not):
            self.unary_helper_helper("not", opt)

    # checks if correct type is used for such unary operator
    # else print error msg
    def unary_helper_helper(self, op, opt):
        if isinstance(opt, ast.Name) or isinstance(opt, ast.Call):
            try:
                if isinstance(opt, ast.Name):
                    keys = list(D[self.fn_name][opt.id].keys())
                    types = D[self.fn_name][opt.id][np.max(keys)]
                else:
                    types = self.process_call_rt_update(opt, 1)

                if len(types) > 1:
                    b = False
                    for tp in types:
                        b = b or self.unary_type_check(op, tp)
                    if b:
                        if isinstance(opt, ast.Name) and self.param_check(D[self.fn_name][opt.id]):
                            vs = []
                            for tp in types:
                                if self.unary_type_check(op, tp):
                                    vs.append(tp)
                            new_s = set()
                            for v in vs:
                                new_s.add(v)

                            keys = list(D[self.fn_name][opt.id].keys())
                            D[self.fn_name][opt.id][np.max(keys)] = new_s
                            if new_s != types:
                                self.unary_helper_helper(op, opt)
                            else:
                                D[self.fn_name][self.var_name][self.line_no] = "Ambiguous"
                        else:
                            D[self.fn_name][self.var_name][self.line_no] = "Ambiguous"
                    else:
                        D[self.fn_name][self.var_name][self.line_no] = "Error"
                elif len(types) == 1:
                    if int in types and self.unary_type_check(op, int):
                        D[self.fn_name][self.var_name][self.line_no] = {self.op_translate(op, 1)}
                    elif float in types and self.unary_type_check(op, float):
                        D[self.fn_name][self.var_name][self.line_no] = {self.op_translate(op, 1.0)}
                    elif bool in types and self.unary_type_check(op, bool):
                        D[self.fn_name][self.var_name][self.line_no] = {self.op_translate(op, True)}
                    else:
                        D[self.fn_name][self.var_name][self.line_no] = "Error"
                else:
                    D[self.fn_name][self.var_name][self.line_no] = "Something is broken, check code..."
            except:
                print("Uninitialized variable", opt.lineno)
                errorMap[opt.lineno] = "Uninitialized variable"
        elif isinstance(opt, ast.Constant):
            if self.unary_type_check(op, type(opt.value)):
                D[self.fn_name][self.var_name][self.line_no] = {self.op_translate(op, opt.value)}
            else:
                D[self.fn_name][self.var_name][self.line_no] = "Error"
        else:
            print("not an unary operator type")

    def op_translate(self, op, v):
        if op == "-":
            return type(-v)
        elif op == "+":
            return type(+v)
        elif op == "not":
            return type(not v)
        elif op == "~":
            return type(~v)

    # check if the given value works for the unary op
    # -, +, not can take int, float, boolean
    # ~ can take int and boolean
    def unary_type_check(self, op, t):
        if op == "-" or op == "+" or op == "not":
            return t == int or t == float or t == bool
        elif op == "~":
            return t == int or t == bool

    # processes the contents of expressions
    def process_exp(self, n):
        return self.recurse(n.value)

    # processes the content of assign
    def process_assign(self, n):
        # print('\n', n.lineno, n.targets[0].id, "=", end=' ')
        for var in n.targets:
            self.var_name = var.id
            self.line_no = n.lineno
            self.dictionary_helper()
            self.recurse(n.value)

    def dictionary_helper(self):
        if self.fn_name not in D:
            D[self.fn_name] = {}
        if self.var_name not in D[self.fn_name]:
            D[self.fn_name][self.var_name] = {}
        if self.line_no not in D[self.fn_name][self.var_name]:
            D[self.fn_name][self.var_name][self.line_no] = set()

    def process_binop(self, n):
        D[self.fn_name][self.var_name][self.line_no] = self.process_binop_recursion(n)

    def binop_rt(self, n):
        return self.process_binop_recursion(n)

    def process_binop_recursion(self, n):
        if isinstance(n.op, ast.Add):
            return self.process_add(n.left, n.right)
        elif isinstance(n.op, ast.Sub):
            return self.process_sub(n.left, n.right)
        elif isinstance(n.op, ast.Div):
            return self.process_div(n.left, n.right)
        elif isinstance(n.op, ast.Mult):
            return self.process_mult(n.left, n.right)
        elif isinstance(n.op, ast.Mod):
            return self.process_mod(n.left, n.right)
        elif isinstance(n.op, ast.Pow):
            return self.process_pow(n.left, n.right)

    def binop_helper(self, left, right, op, valid):
        if self.type_checker(left, right) in valid or isinstance(left, ast.Name) or isinstance(right, ast.Name) \
                or isinstance(left, ast.BinOp) or isinstance(right, ast.BinOp) \
                or isinstance(left, ast.Call) or isinstance(right, ast.Call):
            lt = set()
            rt = set()

            if isinstance(left, ast.BinOp):
                lt = self.process_binop_recursion(left)

            if isinstance(right, ast.BinOp):
                rt = self.process_binop_recursion(right)

            l_n_b = isinstance(left, ast.Name) or isinstance(left, ast.BinOp) or isinstance(left, ast.Call)
            r_n_b = isinstance(right, ast.Name) or isinstance(right, ast.BinOp) or isinstance(right, ast.Call)
            l_c = isinstance(left, ast.Constant) or isinstance(left, ast.List) or isinstance(left, ast.Tuple)
            r_c = isinstance(right, ast.Constant) or isinstance(right, ast.List) or isinstance(right, ast.Tuple)
            case_1 = l_n_b and r_n_b
            case_2 = l_n_b and r_c
            case_3 = l_c and r_n_b

            if l_n_b or r_n_b:
                if case_1:
                    return self.bin_helper_3(left, right, lt, rt, valid, op)
                elif case_2:
                    return self.bin_helper_1_2(0, left, rt, lt, right, valid, op)
                elif case_3:
                    return self.bin_helper_1_2(1, right, rt, lt, left, valid, op)
                else:
                    print("case not covered, review code", left.lineno)
                    errorMap[left.lineno] = "case not covered, review code"
            elif l_c and r_c:
                return {self.bin_translator(op, self.type_checker(left, right))}
            else:
                print("case not covered, review code", left.lineno)
                errorMap[left.lineno] = "case not covered, review code"
        else:
            print("error, invalid binaryOp type", left.lineno)
            errorMap[left.lineno] = "error, invalid binaryOp type"
            return "Error"

    def bin_helper_3(self, left, right, lt, rt, valid, op):
        types_l = self.bin_helper_types(left, lt, rt, 0)
        types_r = self.bin_helper_types(right, lt, rt, 1)

        if "Ambiguous" in types_r or "Ambiguous" in types_l:
            return "Ambiguous"
        if "Error" in types_r or "Error" in types_l:
            return "Error"

        if (len(types_r) > 1 or len(types_l) > 1) or (len(types_r) == 1 and len(types_l) == 1):
            return self.bin_helper_3_helper(types_l, types_r, valid, op, left, right)
        else:
            print("Something is broken, check code...")

    def bin_helper_types(self, o, lt, rt, case):
        if not isinstance(o, ast.BinOp):
            if not isinstance(o, ast.Call):
                keys = list(D[self.fn_name][o.id].keys())
                if np.max(keys) == o.lineno and len(keys) > 1:
                    keys.remove(np.max(keys))
                return D[self.fn_name][o.id][np.max(keys)]
            else:
                return self.process_call_rt_update(o, 1)
        else:
            if case == 0:
                return lt
            elif case == 1:
                return rt
            else:
                print("something broke")

    def bin_helper_3_helper(self, types_l, types_r, valid, op, left, right):
        b = False
        tp = (None, None)
        for t_l in types_l:
            for t_r in types_r:
                tp = (t_l, t_r)
                b = b or (tp in valid)
        if b:
            if len(types_r) > 1 or len(types_l) > 1:
                if ((isinstance(right, ast.Name) and self.param_check(D[self.fn_name][right.id])) or
                        (isinstance(left, ast.Name) and self.param_check(D[self.fn_name][left.id]))):
                    vs = []
                    for t_l in types_l:
                        for t_r in types_r:
                            if (t_l, t_r) in valid:
                                vs.append((t_l, t_r))
                    new_r = set()
                    new_l = set()
                    for v in vs:
                        new_r.add(v[1])
                        new_l.add(v[0])
                    if isinstance(right, ast.Name):
                        keys = list(D[self.fn_name][right.id].keys())
                        D[self.fn_name][right.id][np.max(keys)] = new_r
                    if isinstance(left, ast.Name):
                        keys = list(D[self.fn_name][left.id].keys())
                        D[self.fn_name][left.id][np.max(keys)] = new_l
                    # possible infinite recursion here...perhaps idk
                    if (len(new_l) != 0 and new_l != types_l) or (len(new_r) != 0 and new_r != types_r):
                        if isinstance(right, ast.Name):
                            types_r = new_r
                        if isinstance(left, ast.Name):
                            types_l = new_l
                        return self.bin_helper_3_helper(types_l, types_r, valid, op, left, right)
                    else:
                        return "Ambiguous"
                else:
                    return "Ambiguous"
            else:
                return {self.bin_translator(op, tp)}
        else:
            return "Error"

    def bin_helper_1_2(self, case, o, rt, lt, v, valid, op):
        types = self.bin_helper_types(o, lt, rt, case)

        if 'Ambiguous' in types:
            return "Ambiguous"
        if 'Error' in types:
            return "Error"

        if len(types) >= 1:
            return self.bin_helper_helper(types, v, case, valid, op, o)
        else:
            print("Something is broken, check code...")

    def param_check(self, n):
        keys = list(n.keys())
        rt = False
        for k in keys:
            rt = (k < 0) or rt
        return rt

    def bin_helper_helper(self, types, v, case, valid, op, o):
        b = False
        tp = (None, None)
        for t in types:
            if case == 1:
                tp = (self.type_checker(v, None)[0], t)
            elif case == 0:
                tp = (t, self.type_checker(None, v)[1])
            b = b or (tp in valid)
        if b:
            if len(types) > 1:
                if isinstance(o, ast.Name) and self.param_check(D[self.fn_name][o.id]):
                    vs = []
                    for t in types:
                        if case == 1:
                            tp = (self.type_checker(v, None)[0], t)
                        elif case == 0:
                            tp = (t, self.type_checker(None, v)[1])
                        if tp in valid:
                            vs.append(tp)
                    new_s = set()
                    for i in vs:
                        new_s.add(i[case])
                    # possible infinite recursion here...perhaps idk
                    if len(new_s) != 0 and new_s != types:
                        keys = list(D[self.fn_name][o.id].keys())
                        D[self.fn_name][o.id][np.max(keys)] = new_s
                        types = new_s
                        return self.bin_helper_helper(types, v, case, valid, op, o)
                    else:
                        return "Ambiguous"
                else:
                    return "Ambiguous"
            else:
                return {self.bin_translator(op, tp)}
        else:
            return "Error"

    def bin_type_translator(self, t):
        if t == int:
            return 1
        elif t == float:
            return 1.0
        elif t == bool:
            return True
        elif t == str:
            return "aaa"
        elif t == list:
            return [1, 1]
        elif t == tuple:
            return (0, 0)

    def bin_translator(self, op, tp):
        lf = self.bin_type_translator(tp[0])
        rt = self.bin_type_translator(tp[1])
        if op == "-":
            return type(lf - rt)
        elif op == "+":
            return type(lf + rt)
        elif op == "/":
            return type(lf / rt)
        elif op == "*":
            return type(lf * rt)
        elif op == "%":
            return type(lf % rt)
        elif op == "**":
            return type(lf ** rt)

    def process_add(self, left, right):
        valid_add = [(int, int), (float, float), (bool, bool), (int, float), (float, int), (int, bool), (bool, int),
                     (float, bool), (bool, float), (list, list), (tuple, tuple), (str, str)]
        return self.binop_helper(left, right, "+", valid_add)

    def process_sub(self, left, right):
        valid_sub = [(int, int), (float, float), (bool, bool), (int, float), (float, int), (int, bool), (bool, int),
                     (float, bool), (bool, float)]
        return self.binop_helper(left, right, "-", valid_sub)

    def process_div(self, left, right):
        valid_div = [(int, int), (float, float), (bool, bool), (int, float), (float, int), (int, bool), (bool, int),
                     (float, bool), (bool, float)]
        return self.binop_helper(left, right, "/", valid_div)

    def process_mult(self, left, right):
        valid_mult = [(int, int), (float, float), (bool, bool), (int, float), (float, int), (int, bool), (bool, int),
                      (float, bool), (bool, float), (int, list), (list, int), (int, tuple), (tuple, int), (bool, list),
                      (list, bool), (bool, tuple), (tuple, bool), (str, int), (int, str), (str, bool), (bool, str)]
        return self.binop_helper(left, right, "*", valid_mult)

    def process_mod(self, left, right):
        valid_mod = [(int, int), (float, float), (bool, bool), (int, float), (float, int), (int, bool), (bool, int),
                     (float, bool), (bool, float)]
        return self.binop_helper(left, right, "%", valid_mod)

    def process_pow(self, left, right):
        valid_pow = [(int, int), (float, float), (bool, bool), (int, float), (float, int), (int, bool), (bool, int),
                     (float, bool), (bool, float)]
        return self.binop_helper(left, right, "**", valid_pow)

    def type_checker(self, left, right):
        x = None
        y = None
        if left is not None:
            if isinstance(left, ast.Constant):
                x = type(left.value)
            elif isinstance(left, ast.List):
                x = list
            elif isinstance(left, ast.Tuple):
                x = tuple
        if right is not None:
            if isinstance(right, ast.Constant):
                y = type(right.value)
            elif isinstance(right, ast.List):
                y = list
            elif isinstance(right, ast.Tuple):
                y = tuple
        return x, y

    def boo(self, n):
        cur = set()
        for v in n.values:
            if isinstance(v, ast.BoolOp):
                r = self.boo(v)
                cur = self.bool_translator(cur, r, n.op)
            else:
                t = set()
                if isinstance(v, ast.Name):
                    keys = list(D[self.fn_name][v.id].keys())
                    if np.max(keys) == n.lineno and len(keys) > 1:
                        keys.remove(np.max(keys))
                    else:
                        print("uninitialized variable, check code")
                        errorMap[n.lineno] = "uninitialized variable, check code"
                    t = D[self.fn_name][v.id][np.max(keys)]
                else:
                    if isinstance(v, ast.Constant):
                        t = {type(v.value)}
                    elif isinstance(v, ast.List):
                        t = {list}
                    elif isinstance(v, ast.Tuple):
                        t = {tuple}
                    else:
                        print("case not covered")
                cur = self.bool_translator(cur, t, n.op)
        return cur

    def process_boolop(self, n):
        D[self.fn_name][self.var_name][self.line_no] = self.boo(n)

    def boolop_rt(self, n):
        return self.boo(n)

    def bool_translator(self, cur, v, op):
        if len(v) > 1 or 'Ambiguous' in cur or 'Ambiguous' in v:
            return {'Ambiguous'}
        elif 'Error' in cur or 'Error' in v:
            return {'Error'}
        else:
            if len(cur) == 0:
                return v
            elif len(v) == 0:
                return cur

            a = cur.pop()
            cur.add(a)
            b = v.pop()
            v.add(b)

            if isinstance(op, ast.And):
                return {type(self.bin_type_translator(a) and self.bin_type_translator(b))}
            elif isinstance(op, ast.Or):
                return {type(self.bin_type_translator(a) or self.bin_type_translator(b))}
            else:
                print("Something broke")

    def process_constant(self, n):
        D[self.fn_name][self.var_name][self.line_no].add(type(n.value))
        # print(n.value, end=' ')

    def process_name(self, n):
        try:
            keys = list(D[self.fn_name][n.id].keys())
            D[self.fn_name][self.var_name][n.lineno] = D[self.fn_name][n.id][np.max(keys)]
            # print(n.id, end=' ')
        except:
            print("Uninitialized Variable", n.id)
            errorMap[n.lineno] = "Uninitialized Variable"

    def process_tuple(self, n):
        # print('tuple', end=' ')
        D[self.fn_name][self.var_name][self.line_no].add(tuple)
        # for i in n.elts:
        #     self.recurse(i)

    def process_list(self, n):
        # print('list', end=' ')
        D[self.fn_name][self.var_name][self.line_no].add(list)
        # for i in n.elts:
        #     self.recurse(i)
        # self.map_list(n)

    def map_list(self, n):
        lt = []
        self.list_reconstructor(n, lt)
        if self.fn_name not in L:
            L[self.fn_name] = {}
        if self.var_name not in L[self.fn_name]:
            L[self.fn_name][self.var_name] = {}

        L[self.fn_name][self.var_name][self.line_no] = lt

    def list_reconstructor(self, n, lt):
        for e in n.elts:
            if isinstance(e, ast.Constant):
                lt.append(e.value)
            elif isinstance(e, ast.List):
                lt.append(self.list_reconstructor(e, []))
        return lt

    def process_call(self, n):
        if isinstance(n.func, ast.Name):
            self.process_call_param(n)
        else:
            self.process_call_rt_update(n, 0)

    def process_fn_def(self, n):
        self.process_call_arg(n)

    def process_call_param(self, n):
        if isinstance(n.func, ast.Name):
            fn_name = n.func.id + '|' + str(len(n.args))
            num = -1
            a_list = []
            for p in n.args:
                if isinstance(p, ast.Constant):
                    a_list.append(self.call_param_type({type(p.value)}, fn_name, num))
                elif isinstance(p, ast.List):
                    a_list.append(self.call_param_type({list}, fn_name, num))
                elif isinstance(p, ast.Tuple):
                    a_list.append(self.call_param_type({tuple}, fn_name, num))
                elif isinstance(p, ast.UnaryOp):
                    old_line_no = self.line_no
                    self.line_no = np.inf
                    D[self.fn_name][self.var_name][self.line_no] = set()
                    self.process_unaryop(p)
                    a_list.append(self.call_param_type(D[self.fn_name][self.var_name][self.line_no], fn_name, num))
                    D[self.fn_name][self.var_name].pop(self.line_no)
                    self.line_no = old_line_no
                elif isinstance(p, ast.BinOp):
                    a_list.append(self.call_param_type(self.binop_rt(p), fn_name, num))
                elif isinstance(p, ast.BoolOp):
                    a_list.append(self.call_param_type(self.boolop_rt(p), fn_name, num))
                elif isinstance(p, ast.Call):
                    rt = self.process_call_rt_update(p, 1)
                    if len(rt) != 0:
                        a_list.append(self.call_param_type(rt, fn_name, num))
                    else:
                        a_list.append(0)
                elif isinstance(p, ast.Name):
                    keys = list(D[self.fn_name][p.id].keys())
                    if np.max(keys) == n.lineno and len(keys) > 1:
                        keys.remove(np.max(keys))
                    rt = D[self.fn_name][p.id][np.max(keys)]
                    a_list.append(self.call_param_type(rt, fn_name, num))
                else:
                    a_list.append(0)
                num = num - 1

            if 0 in a_list:
                D[self.fn_name][self.var_name][self.line_no] = 'Error'
            elif 2 in a_list:
                D[self.fn_name][self.var_name][self.line_no] = 'Ambiguous'
            else:
                self.process_call_rt_update(n, 0)
        else:
            print("review code, case not covered")

    def call_param_type(self, types, fn, num):
        if fn in D.keys():
            params = []
            for var in D[fn]:
                if self.param_check(D[fn][var]):
                    params.append(var)
            for p in params:
                if num in D[fn][p]:
                    t = D[fn][p][num]
                    break
            rt_1 = True
            rt_2 = False
            for tp in types:
                rt_1 = rt_1 and (tp in t)
                rt_2 = rt_2 or (tp in t)
            if rt_1:
                return 1
            elif rt_2:
                return 2
            else:
                return 0
        else:
            print("function does not exist")

    def attr_to_string(self, attr):
        if not isinstance(attr.value, ast.Attribute):
            if isinstance(attr.value, ast.Name):
                if attr.value.id in D[self.fn_name]:
                    keys = list(D[self.fn_name][attr.value.id].keys())
                    types = D[self.fn_name][attr.value.id][max(keys)]
                    if len(types) == 1:
                        for t in types:
                            return str(t) + '.' + attr.attr
                    elif len(types) > 1:
                        return 'Ambiguous' + '.' + attr.attr
                    else:
                        return 'Error' + '.' + attr.attr
                else:
                    return attr.value.id + '.' + attr.attr
            elif isinstance(attr.value, ast.Constant):
                return str(type(attr.value.value)) + '.' + attr.attr
            elif isinstance(attr.value, ast.List):
                return str(list) + '.' + attr.attr
            elif isinstance(attr.value, ast.Tuple):
                return str(tuple) + '.' + attr.attr
            elif isinstance(attr.value, ast.Call):
                types = self.process_call_rt_update(attr.value, 1)
                if len(types) == 1:
                    for t in types:
                        return str(t) + '.' + attr.attr
                elif len(types) > 1:
                    return 'Ambiguous' + '.' + attr.attr
                else:
                    return 'Error' + '.' + attr.attr
            else:
                print("review code, case not covered")
        else:
            return self.attr_to_string(attr.value) + '.' + attr.attr

    def class_translator(self, lt):
        s = []
        for c in lt:
            if c == str(int):
                s.append("int")
            elif c == str(str):
                s.append("str")
            elif c == str(float):
                s.append("float")
            elif c == str(bool):
                s.append("bool")
            elif c == str(list):
                s.append("list")
            elif c == str(tuple):
                s.append("list")
            elif c == str(set):
                s.append("set")
            elif c == str(dict):
                s.append("dict")
            else:
                s.append(c)
        return s

    def process_call_rt_update_recurse(self, class_name, fn_name):
        if class_name in C.keys():
            if fn_name in C[class_name].keys():
                if 'return' in C[class_name][fn_name].keys():
                    return C[class_name][fn_name]['return'][0]
                else:
                    print("not a return function")
                    return D[self.fn_name][self.var_name][self.line_no]
            else:
                print("no such function")
                return 'Error'
        else:
            print("class not found")
            return 'Error'

    def process_call_rt_update(self, n, rt):
        if isinstance(n.func, ast.Attribute):
            cl = self.attr_to_string(n.func).split(".")
            cl = self.class_translator(cl)
            fn_name = cl[len(cl) - 1] + '|' + str(len(n.args))
            class_name = cl[0]
            for i in range(len(cl) - 2):
                class_name = class_name + '.' + cl[i + 1]
            if rt:
                return self.process_call_rt_update_recurse(class_name, fn_name)
            else:
                D[self.fn_name][self.var_name][self.line_no] = self.process_call_rt_update_recurse(class_name, fn_name)
        elif isinstance(n.func, ast.Name):
            fn_name = n.func.id + '|' + str(len(n.args))
            if fn_name in D.keys():
                if 'return' in D[fn_name].keys():
                    for ln in D[fn_name]['return']:
                        if rt:
                            return D[fn_name]['return'][ln]
                        else:
                            D[self.fn_name][self.var_name][self.line_no] = D[fn_name]['return'][ln]
                else:
                    print("not a return function")
        else:
            print("review code, case not covered")
            if rt:
                return "Error"
            else:
                D[self.fn_name][self.var_name][self.line_no] = "Error"

    def process_call_arg(self, n):
        args = n.args.args
        ln = -1
        self.fn_name = self.fn_name + '|' + str(len(args))
        for a in args:
            self.var_name = a.arg

            if self.fn_name not in D:
                D[self.fn_name] = {}
            if self.var_name not in D[self.fn_name]:
                D[self.fn_name][self.var_name] = {}
            if self.line_no not in D[self.fn_name][self.var_name]:
                D[self.fn_name][self.var_name][ln] = self.valid_types
            ln = ln - 1

    def process_return(self, n):
        self.var_name = 'return'
        self.line_no = n.lineno
        self.dictionary_helper()
        self.recurse(n.value)

    def process_aug(self, n):
        # print('\n', n.lineno, n.targets[0].id, "=", end=' ')
        self.var_name = n.target.id
        self.line_no = n.lineno
        self.dictionary_helper()
        if len(list(D[self.fn_name][self.var_name].keys())) == 1:
            D[self.fn_name][self.var_name][self.line_no] = 'Error'
        else:
            self.recurse(ast.BinOp(n.target, n.op, n.value))

    # def process_subscript(self, n):

    # magic switch recursion thing
    # content covers nested for, nested if/elif/else, nested while, assignment, try/except/finally,
    # unaryOp (+,-,~, not), Expr,
    def recurse(self, n):
        if isinstance(n, ast.For):
            self.process_for(n)
        elif isinstance(n, ast.If):
            self.process_if(n)
        elif isinstance(n, ast.While):
            self.process_while(n)
        elif isinstance(n, ast.Try):
            self.process_try(n)
        elif isinstance(n, ast.UnaryOp):
            self.process_unaryop(n)
        elif isinstance(n, ast.Expr):
            self.process_exp(n)
        elif isinstance(n, ast.Assign):
            self.process_assign(n)
        elif isinstance(n, ast.BinOp):
            self.process_binop(n)
        elif isinstance(n, ast.BoolOp):
            self.process_boolop(n)
        elif isinstance(n, ast.Constant):
            self.process_constant(n)
        elif isinstance(n, ast.Tuple):
            self.process_tuple(n)
        elif isinstance(n, ast.List):
            self.process_list(n)
        elif isinstance(n, ast.Name):
            self.process_name(n)
        elif isinstance(n, ast.Call):
            self.process_call(n)
        elif isinstance(n, ast.Return):
            self.process_return(n)
        elif isinstance(n, ast.AugAssign):
            self.process_aug(n)
        # elif isinstance(n, ast.Subscript):
        #     self.process_subscript(n)

    def visit_FunctionDef(self, node):
        # print('function', node.name)
        self.fn_name = node.name
        self.process_fn_def(node)
        for n in node.body:
            self.recurse(n)

    # def visit_ClassDef(self, node):
    #     global D
    #     D = {}
    #     C[node.name] = D
    #
    #     for n in node.body:
    #         self.process_FunctionDef(n)


if __name__ == "__main__":
    main()
