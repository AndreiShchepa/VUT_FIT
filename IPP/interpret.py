import xml.etree.ElementTree as ET
import sys
import re

class Program:
    def __init__(self):
        self._GF = dict()
        self._LF = None
        self._TF = None
        self._frames = []
        self._labels_dict = dict()
        self._return_lines = []
        self._line = 0
        self._num_of_instrs = 0
        self._data_stack = []

    def get_line(self):
        return self._line

    def set_line(self, val):
        self._line = val

    def get_num_of_instrs(self):
        return self._num_of_instrs

    def set_num_of_instrs(self, val):
        self._num_of_instrs = val

class Instruction():
    _instruction_list = []

    def __init__(self, opcode: str, num: int, dict_args):
        self._opcode: str = opcode
        self._num_of_arg: int = num
        self._arguments_dict: dict() = dict_args
        self._instruction_list.append(self)

    def get_opcode(self):
        return self._opcode

    def get_num_of_arg(self):
        return self._num_of_arg

    def get_arg(self, id):
        return self._arguments_dict[id]

    @classmethod
    def get_instr_list(cls):
        return cls._instruction_list

    def check_frame_none(self, frame):
        if frame == None:
            print("PIZDAAAAAAAAAA")
            exit(124356)

    def _get_var(self, var, prg, key):
        if key != "var":
            return None, key, var

        try:
            if var[0:2] == "LF":
                self.check_frame_none(prg._LF)
                type_value = prg._LF[var[3:]]
            elif var[0:2] == "GF":
                type_value = prg._GF[var[3:]]
            elif var[0:2] == "TF":
                self.check_frame_none(prg._TF)
                type_value = prg._TF[var[3:]]
        except:
            return None, None, None

        typ, value = type_value[0], type_value[1]
        return var[3:], typ, value

    def _add_var(self, name, frame, typ, value, prg):
        if frame == "GF":
            prg._GF[name] = [typ, value]
        elif frame == "LF":
            self.check_frame_none(prg._LF)
            prg._LF[name] = [typ, value]
        elif frame == "TF":
            self.check_frame_none(prg._TF)
            prg._TF[name] = [typ, value]

class Defvar(Instruction):
    def __init__(self, dict_args):
        super().__init__("DEFVAR", 1, dict_args)

    def check_args(self):
        num = super().get_num_of_arg()

    def execute(self, prg):
        (key, value), = self.get_arg(0).items()
        frame, new_name = value[0:2], value[3:]
        name, typ, value = self._get_var(value, prg, key)

        if name != None:
            print("Redeclarartion errr")
            exit(126666)

        self._add_var(new_name, frame, None, value, prg)

class Move(Instruction):
    def __init__(self, dict_args):
        super().__init__("MOVE", 2, dict_args)

    def check_args(self):
        num = super().get_num_of_arg()

    def execute(self, prg):
        (key1, value1), = self.get_arg(0).items()
        frame = value1[0:2]
        name1, typ1, value1 = self._get_var(value1, prg, key1)

        (key2, value2), = self.get_arg(1).items()
        name2, typ2, value2 = self._get_var(value2, prg, key2)

        # check compatibility of types
        self._add_var(name1, frame, typ2, value2, prg)

class Createframe(Instruction):
    def __init__(self, dict_args):
        super().__init__("CREATEFRAME", 0, dict_args)

    def check_args(self):
        num = super().get_num_of_arg()

    def execute(self, prg):
        prg._TF = dict()

class Popframe(Instruction):
    def __init__(self, dict_args):
        super().__init__("POPFRAME", 0, dict_args)

    def check_args(self):
        num = super().get_num_of_arg()

    def execute(self, prg):
        if len(prg._frames) == 0:
            print("ERRRRRRRRRRRRRR HOP")
            exit(9876)

        prg._TF = prg._frames.pop()

class Break(Instruction):
    def __init__(self, dict_args):
        super().__init__("BREAK", 0, dict_args)

    def check_args(self):
        num = super().get_num_of_arg()

    def execute(self, prg):
        print("Break is here!\n")

class Call(Instruction):
    def __init__(self, dict_args):
        super().__init__("CALL", 1, dict_args)

    def check_args(self):
        num = super().get_num_of_arg()

    def execute(self, prg):
        (key, value), = self.get_arg(0).items()

        try:
            prg._return_lines.append(prg.get_line())
            prg.set_line(prg._labels_dict[value] - 1)
        except:
            print("Label doenst exist")
            exit(6547)

class Jump(Instruction):
    def __init__(self, dict_args):
        super().__init__("JUMP", 1, dict_args)

    def check_args(self):
        num = super().get_num_of_arg()

    def execute(self, prg):
        (key, value), = self.get_arg(0).items()

        try:
            prg.set_line(prg._labels_dict[value] - 1)
        except:
            print("Label doenst exist")
            exit(6547)

class Pushs(Instruction):
    def __init__(self, dict_args):
        super().__init__("PUSHS", 1, dict_args)

    def check_args(self):
        num = super().get_num_of_arg()

    def execute(self, prg):
        (key, value), = self.get_arg(0).items()
        frame = value[0:2]
        name, typ, value = self._get_var(value, prg, key)

        if name == None and key == var:
            print("Not defind var")
            exit(999)

        prg._data_stack.append((typ, value))

class Exit(Instruction):
    def __init__(self, dict_args):
        super().__init__("EXIT", 1, dict_args)

    def check_args(self):
        num = super().get_num_of_arg()

    def execute(self, prg):
        (key, value), = self.get_arg(0).items()
        frame = value[0:2]
        name, typ, value = self._get_var(value, prg, key)

        # TODO
        if key == "var":
            print("smth")
        elif key != "int" or int(value) > 49 or int(value) < 0:
            print("err with exit cmd")
            exit(9999)

        print("write stats")
        exit(int(value))

class Jumpifeq(Instruction):
    def __init__(self, dict_args):
        super().__init__("JUMPIFEQ", 3, dict_args)

    def check_args(self):
        num = super().get_num_of_arg()

    def execute(self, prg):
        print("Jumpifeq is here!\n")

class Add(Instruction):
    def __init__(self, dict_args):
        super().__init__("ADD", 3, dict_args)

    def check_args(self):
        num = super().get_num_of_arg()

    def execute(self, prg):
        (key1, value1), = self.get_arg(0).items()
        frame = value1[0:2]
        name1, typ1, value1 = self._get_var(value1, prg, key1)

        if name1 == None:
            print("Where is name")
            exit(999)

        (key2, value2), = self.get_arg(1).items()
        name2, typ2, value2 = self._get_var(value2, prg, key2)

        (key3, value3), = self.get_arg(2).items()
        name3, typ3, value3 = self._get_var(value3, prg, key3)

        check_type(key1, key2, key3, "int")
        self._add_var(name1, frame, "int", str(int(value2) + int(value3)), prg)

class Mul(Instruction):
    def __init__(self, dict_args):
        super().__init__("MUL", 3, dict_args)

    def check_args(self):
        num = super().get_num_of_arg()

    def execute(self, prg):
        (key1, value1), = self.get_arg(0).items()
        frame = value1[0:2]
        name1, typ1, value1 = self._get_var(value1, prg, key1)

        if name1 == None:
            print("Where is name")
            exit(999)

        (key2, value2), = self.get_arg(1).items()
        name2, typ2, value2 = self._get_var(value2, prg, key2)

        (key3, value3), = self.get_arg(2).items()
        name3, typ3, value3 = self._get_var(value3, prg, key3)

        check_type(key1, key2, key3, "int")
        self._add_var(name1, frame, "int", str(int(value2) * int(value3)), prg)

class Lt(Instruction):
    def __init__(self, dict_args):
        super().__init__("LT", 3, dict_args)

    def check_args(self):
        num = super().get_num_of_arg()

    def execute(self, prg):
        print("Lt is here!\n")

class Eq(Instruction):
    def __init__(self, dict_args):
        super().__init__("EQ", 3, dict_args)

    def check_args(self):
        num = super().get_num_of_arg()

    def execute(self, prg):
        print("Eq is here!\n")

class Or(Instruction):
    def __init__(self, dict_args):
        super().__init__("Or", 3, dict_args)

    def check_args(self):
        num = super().get_num_of_arg()

    def execute(self, prg):
        (key1, value1), = self.get_arg(0).items()
        frame = value1[0:2]
        name1, typ1, value1 = self._get_var(value1, prg, key1)

        if name1 == None:
            print("Where is name")
            exit(999)

        (key2, value2), = self.get_arg(1).items()
        name2, typ2, value2 = self._get_var(value2, prg, key2)

        (key3, value3), = self.get_arg(2).items()
        name3, typ3, value3 = self._get_var(value3, prg, key3)

        check_type(key1, key2, key3, "bool")
        self._add_var(name1, frame, "bool", str(bool(value2) or bool(value3)), prg)

class Concat(Instruction):
    def __init__(self, dict_args):
        super().__init__("CONCAT", 3, dict_args)

    def check_args(self):
        num = super().get_num_of_arg()

    def execute(self, prg):
        (key1, value1), = self.get_arg(0).items()
        frame = value1[0:2]
        name1, typ1, value1 = self._get_var(value1, prg, key1)

        if name1 == None:
            print("Where is name")
            exit(999)

        (key2, value2), = self.get_arg(1).items()
        name2, typ2, value2 = self._get_var(value2, prg, key2)

        (key3, value3), = self.get_arg(2).items()
        name3, typ3, value3 = self._get_var(value3, prg, key3)

        check_type(key1, key2, key3, "string")
        self._add_var(name1, frame, "string", value2 + value3, prg)

class Setchar(Instruction):
    def __init__(self, dict_args):
        super().__init__("SETCHAR", 3, dict_args)

    def check_args(self):
        num = super().get_num_of_arg()

    def execute(self, prg):
        print("Setchar is here!\n")

class Stri2int(Instruction):
    def __init__(self, dict_args):
        super().__init__("STRI2INT", 3, dict_args)

    def check_args(self):
        num = super().get_num_of_arg()

    def execute(self, prg):
        print("Stri2int is here!\n")

class Pops(Instruction):
    def __init__(self, dict_args):
        super().__init__("POPS", 1, dict_args)

    def check_args(self):
        num = super().get_num_of_arg()

    def execute(self, prg):
        print("Pops is here!\n")

class Pushframe(Instruction):
    def __init__(self, dict_args):
        super().__init__("PUSHFRAME", 0, dict_args)

    def check_args(self):
        num = super().get_num_of_arg()

    def execute(self, prg):
        if prg._TF is None:
            print("Not defined Temporary frame, exit with err")
            exit(12345)

        prg.frames.append(prg._TF)
        prg._LF = self._TF
        prg._TF = None

class Return(Instruction):
    def __init__(self, dict_args):
        super().__init__("Return", 0, dict_args)

    def check_args(self):
        num = super().get_num_of_arg()

    def execute(self, prg):
        if len(prg._return_lines) == 0:
            print("VUT FIT U ERR")
            exit(5555)

        prg.set_line(prg._return_lines.pop() - 1)

class Strlen(Instruction):
    def __init__(self, dict_args):
        super().__init__("STRLEN", 2, dict_args)

    def check_args(self):
        num = super().get_num_of_arg()

    def execute(self, prg):
        (key1, value1), = self.get_arg(0).items()
        frame = value1[0:2]
        name1, typ1, value1 = self._get_var(value1, prg, key1)

        if name1 == None:
            print("Where is name")
            exit(999)

        (key2, value2), = self.get_arg(1).items()
        name2, typ2, value2 = self._get_var(value2, prg, key2)

        check_2_keys(key1, "int", key2, "string")
        self._add_var(name1, frame, "int", strlen(value2), prg)

class Label(Instruction):
    def __init__(self, dict_args):
        super().__init__("LABEL", 1, dict_args)

    def check_args(self):
        num = super().get_num_of_arg()

    def execute(self, prg):
        #print(prg._labels_dict)
        pass

class Type(Instruction):
    def __init__(self, dict_args):
        super().__init__("TYPE", 2, dict_args)

    def check_args(self):
        num = super().get_num_of_arg()

    def execute(self, prg):
        (key, value1), = self.get_arg(0).items()
        frame = value1[0:2]
        name1, typ1, value1 = self._get_var(value1, prg, key)

        (key, value2), = self.get_arg(1).items()
        name2, typ2, value2 = self._get_var(value2, prg, key)

        if typ1 != "string" and typ2 != None:
            print("Semantic err")
            exit(1111111)

        self._add_var(name1, frame, "string", typ2, prg)

class Write(Instruction):
    def __init__(self, dict_args):
        super().__init__("WRITE", 1, dict_args)

    def check_args(self):
        num = super().get_num_of_arg()

    def execute(self, prg):
        (key, value), = self.get_arg(0).items()
        name, key, value = self._get_var(value, prg, key)

        value = value if "string" != key else re.sub(r'\\([0-9]{3})', lambda x: chr(int(x[1])), value)
        print("" if key == "nil" else value, end='', file=sys.stdout)

class Dprint(Instruction):
    def __init__(self, dict_args):
        super().__init__("DPRINT", 1, dict_args)

    def check_args(self):
        num = super().get_num_of_arg()

    def execute(self, prg):
        (key, value), = self.get_arg(0).items()
        name, key, value = self._get_var(value, prg, key)

        value = value if "string" != key else re.sub(r'\\([0-9]{3})', lambda x: chr(int(x[1])), value)
        print("" if key == "nil" else value, end='', file=sys.stderr)

class Int2char(Instruction):
    def __init__(self, dict_args):
        super().__init__("INT2CHAR", 2, dict_args)

    def check_args(self):
        num = super().get_num_of_arg()

    def execute(self, prg):
        print("Int2char is here!\n")

class Jumpifneq(Instruction):
    def __init__(self, dict_args):
        super().__init__("JUMPIFNEQ", 3, dict_args)

    def check_args(self):
        num = super().get_num_of_arg()

    def execute(self, prg):
        print("Jumpifneq is here!\n")

class Sub(Instruction):
    def __init__(self, dict_args):
        super().__init__("SUB", 3, dict_args)

    def check_args(self):
        num = super().get_num_of_arg()

    def execute(self, prg):
        (key1, value1), = self.get_arg(0).items()
        frame = value1[0:2]
        name1, typ1, value1 = self._get_var(value1, prg, key1)

        if name1 == None:
            print("Where is name")
            exit(999)

        (key2, value2), = self.get_arg(1).items()
        name2, typ2, value2 = self._get_var(value2, prg, key2)

        (key3, value3), = self.get_arg(2).items()
        name3, typ3, value3 = self._get_var(value3, prg, key3)

        check_type(key1, key2, key3, "int")
        self._add_var(name1, frame, "int", str(int(value2) - int(value3)), prg)

class Idiv(Instruction):
    def __init__(self, dict_args):
        super().__init__("IDIV", 3, dict_args)

    def check_args(self):
        num = super().get_num_of_arg()

    def execute(self, prg):
        (key1, value1), = self.get_arg(0).items()
        frame = value1[0:2]
        name1, typ1, value1 = self._get_var(value1, prg, key1)

        if name1 == None:
            print("Where is name")
            exit(999)

        (key2, value2), = self.get_arg(1).items()
        name2, typ2, value2 = self._get_var(value2, prg, key2)

        (key3, value3), = self.get_arg(2).items()
        name3, typ3, value3 = self._get_var(value3, prg, key3)

        check_type(key1, key2, key3, "int")
        if int(value3) == 0:
            print("Psel nahuy")
            exit(57)

        self._add_var(name1, frame, "int", str(int(value2) // int(value3)), prg)

class Gt(Instruction):
    def __init__(self, dict_args):
        super().__init__("GT", 3, dict_args)

    def check_args(self):
        num = super().get_num_of_arg()

    def execute(self, prg):
        print("Gt is here!\n")

class And(Instruction):
    def __init__(self, dict_args):
        super().__init__("AND", 3, dict_args)

    def check_args(self):
        num = super().get_num_of_arg()

    def execute(self, prg):
        (key1, value1), = self.get_arg(0).items()
        frame = value1[0:2]
        name1, typ1, value1 = self._get_var(value1, prg, key1)

        if name1 == None:
            print("Where is name")
            exit(999)

        (key2, value2), = self.get_arg(1).items()
        name2, typ2, value2 = self._get_var(value2, prg, key2)

        (key3, value3), = self.get_arg(2).items()
        name3, typ3, value3 = self._get_var(value3, prg, key3)

        check_type(key1, key2, key3, "bool")
        self._add_var(name1, frame, "bool", str(bool(value2) and bool(value3)), prg)

class Not(Instruction):
    def __init__(self, dict_args):
        super().__init__("NOT", 2, dict_args)

    def check_args(self):
        num = super().get_num_of_arg()

    def execute(self, prg):
        print("Not is here!\n")

class Getchar(Instruction):
    def __init__(self, dict_args):
        super().__init__("GETCHAR", 3, dict_args)

    def check_args(self):
        num = super().get_num_of_arg()

    def execute(self, prg):
        print("Getchar is here!\n")

class Read(Instruction):
    def __init__(self, dict_args):
        super().__init__("READ", 2, dict_args)

    def check_args(self):
        num = super().get_num_of_arg()

    def execute(self, prg):
        print("Read is here!\n")

class Argument:
    def __init__(self, type_arg: str, str_arg):
        self._type = type_arg
        self._arg = str_arg

class Factory:
    _dict_func = {"DEFVAR"  : Defvar , "CREATEFRAME" : Createframe, "POPFRAME" : Popframe,
                  "BREAK"   : Break  , "CALL"        : Call       , "JUMP"     : Jump    ,
                  "EXIT"    : Exit   , "MOVE"        : Move       , "ADD"      : Add     ,
                  "CONCAT"  : Concat , "STRI2INT"    : Stri2int   , "LT"       : Lt      ,
                  "RETURN"  : Return , "INT2CHAR"    : Int2char   , "EQ"       : Eq      ,
                  "STRLEN"  : Strlen , "PUSHFRAME"   : Pushframe  , "OR"       : Or      ,
                  "DPRINT"  : Dprint , "JUMPIFNEQ"   : Jumpifneq  , "POPS"     : Pops    ,
                  "GETCHAR" : Getchar, "JUMPIFEQ"    : Jumpifeq   , "LABEL"    : Label   ,
                  "WRITE"   : Write  , "TYPE"        : Type       , "IDIV"     : Idiv    ,
                  "READ"    : Read   , "AND"         : And        , "GT"       : Gt      ,
                  "PUSHS"   : Pushs  , "MUL"         : Mul        , "SUB"      : Sub     ,
                  "SETCHAR" : Setchar, "NOT"         : Not
                  }

    @classmethod
    def resolve(cls, string: str, dict_args: dict()):
        try:
            return cls._dict_func[string](dict_args)
        except:
            print("ERROR with name of instruction, add exit error")

def check_type(key1, key2, key3, typ):
    if ((key1 != typ and key1 != "var" ) or
    key2 != typ or key3 != typ):
        print("Sem ERRRRRRR")
        exit(9876)

def check_2_keys(key1, typ1, key2, typ2):
    if ((key1 != typ1 and key1 != "var") or
    key2 != typ2):
        print("SEm errrr")
        exit(245)

def check_label(prg, opcode, dict):
    if opcode.upper() == "LABEL":
        if dict["label"] in prg._labels_dict:
            print("JOPAAAAAAA")
            exit(453235)

        prg._labels_dict[dict["label"]] = prg.get_num_of_instrs()

def check_order(prg, order):
    if prg.get_num_of_instrs() != int(order):
        print("ER UUUUU")
        exit(2987)

# MAIN
tree = ET.parse('out.xml')
root = tree.getroot()
prg = Program()

for child in root:
    dict_args = dict()
    prg.set_num_of_instrs(prg.get_num_of_instrs() + 1)
    check_order(prg, child.attrib["order"])
    idx = 0
    for ch in child:
        dict_args[idx] = {ch.attrib["type"] : ch.text}
        idx += 1

    instr = Factory.resolve(child.attrib["opcode"], dict_args)
    try:
        check_label(prg, child.attrib["opcode"], dict_args[0])
    except:
        pass

while prg.get_line() < prg.get_num_of_instrs():
    Instruction.get_instr_list()[prg.get_line()].execute(prg)
    prg.set_line(prg.get_line() + 1)
