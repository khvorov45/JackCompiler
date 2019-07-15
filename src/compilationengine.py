"""CompilationEngine class.
Does not have a huge amount of errer checking, will likely only work with
correctly written .jack classes.
"""

from .utilities import UnexpectedToken, build_terminal
from .glossary import is_term, is_op, KEYWORD_CONSTANTS, UNARY_OP, OPER, SEGMENT
from .symboltable import SymbolTable

class CompilationEngine():
    """Controls compilation

    Arguments:
        self.toks -- list of tokens (TokenInfo class).
            Should represent one class.
        out_file_path -- path to the file to write translation to
    """
    # pylint: disable=too-many-instance-attributes
    def __init__(self, toks, out_file_path):
        self.toks = toks
        self.out_file_path = out_file_path
        self.cur_ind = 0
        self.tab_char = "  "
        self.tab_level = 1
        self.result = ""
        self.vmcode = ""
        self.symbol_table = SymbolTable()
        self.class_name = ""
        self.counts = {"while": 0, "if": 0}
        self.compile_class()

    def compile_class(self):
        """Compiles the entire class"""

        # First token is 'class'
        if self.toks[self.cur_ind].token != "class":
            raise UnexpectedToken(self.toks[self.cur_ind])
        self.result += "<class>\n"
        self.create_xml_terminal()

        # Second token is the class name. These do not go into the symbol table.
        if self.toks[self.cur_ind].toktype != "identifier":
            raise UnexpectedToken(self.toks[self.cur_ind])
        self.create_xml_terminal(increment=False)
        self.class_name = self.toks[self.cur_ind].token
        self.cur_ind += 1

        # Opening '{'
        self.create_xml_terminal()

        # Class variables
        while self.toks[self.cur_ind].token in ["static", "field"]:
            self.compile_class_var_dec()

        # Print the symbol table
        print(self.class_name + " SYMBOL TABLE")
        self.symbol_table.print(sub=False)

        # Subroutines
        while self.toks[self.cur_ind].token in \
            ["constructor", "function", "method"]:
            self.compile_subroutine()

        # Closing '}'
        self.create_xml_terminal()

        # Finish up the class
        self.result += "</class>\n"

        # Write xml to translation file
        out_file = open(self.out_file_path, "w+")
        out_file.write(self.result)
        out_file.close()

        # Write VM
        vm_file = self.out_file_path.replace(".xml", ".vm")
        out_file = open(vm_file, "w+")
        out_file.write(self.vmcode)
        out_file.close()

    def compile_class_var_dec(self):
        """Compiles class variable declarations"""

        # Open up
        self.result += self.tab_level * self.tab_char + "<classVarDec>\n"
        self.tab_level += 1

        # All of these should be in the symbol table

        # 'static' or 'field'
        self.create_xml_terminal(increment=False)
        knd = self.toks[self.cur_ind].token
        self.cur_ind += 1

        # type
        self.create_xml_terminal(increment=False)
        tpe = self.toks[self.cur_ind].token
        self.cur_ind += 1

        # name(s)
        while self.toks[self.cur_ind].token != ";":
            self.create_xml_terminal(increment=False)
            nme = self.toks[self.cur_ind].token
            self.cur_ind += 1
            self.symbol_table.define(nme, tpe, knd)
            if self.toks[self.cur_ind].token == ",":
                self.create_xml_terminal()

        self.create_xml_terminal() # ;

        # Close down
        self.tab_level -= 1
        self.result += self.tab_level * self.tab_char + "</classVarDec>\n"

    def compile_subroutine(self):
        """Compiles a subroutine"""

        # Open up
        self.result += self.tab_level * self.tab_char + "<subroutineDec>\n"
        self.tab_level += 1

        # Reset the subroutine's symbol table
        self.symbol_table.start_subroutine()

        # This reset is unnecessary, it is to conform to ECS's compiler
        self.counts["while"] = 0
        self.counts["if"] = 0

        # Subroutine type
        subroutine_type = self.toks[self.cur_ind].token
        if subroutine_type not in \
            ["constructor", "function", "method"]:
            raise UnexpectedToken(subroutine_type)
        self.create_xml_terminal()

        # Next is the return type
        self.create_xml_terminal()

        # Then is the name, not placing this in the symbol table.
        subroutine_name = self.toks[self.cur_ind].token
        self.create_xml_terminal()

        # Then is the parameter list.
        # All arguments should be in the symbol table.
        self.compile_parameter_list()

        # Then is the subroutine body
        self.result += self.tab_level * self.tab_char + "<subroutineBody>\n"
        self.tab_level += 1

        # First is the opening '{'
        self.create_xml_terminal()

        # Then all the variables. All of these will go into the symbol table.
        while self.toks[self.cur_ind].token == "var":
            self.compile_var_dec()

        # Label the subroutine
        self.vmcode += "function " + self.class_name + "." + subroutine_name + \
            " " + str(self.symbol_table.var_count("var")) + "\n"

        # Possibly required extra stuff
        if subroutine_type == "constructor":
            field_count = self.symbol_table.var_count("field")
            self.vmcode += "push constant " + str(field_count) + "\n" + \
                "call Memory.alloc 1\npop pointer 0\n"
        elif subroutine_type == "method":
            self.vmcode += "push argument 0\npop pointer 0\n"

        # Then all the statements
        self.compile_statements()

        # Closing '}'
        self.create_xml_terminal()

        # Print the symbol table
        print(subroutine_name + " SYMBOL TABLE")
        self.symbol_table.print(cla=False)

        # Finish the subroutine
        self.tab_level -= 1
        self.result += self.tab_level * self.tab_char + "</subroutineBody>\n"
        self.tab_level -= 1
        self.result += self.tab_level * self.tab_char + "</subroutineDec>\n"

    def compile_parameter_list(self):
        """Compiles a parameter list (possibly empty)"""

        # First is the opening '('
        self.create_xml_terminal()

        # Open up
        self.result += self.tab_level * self.tab_char + "<parameterList>\n"
        self.tab_level += 1

        # Then come the parameters
        while self.toks[self.cur_ind].token != ")":
            # Type
            self.create_xml_terminal(increment=False)
            tpe = self.toks[self.cur_ind].token
            self.cur_ind += 1
            # Name
            self.create_xml_terminal(increment=False)
            nme = self.toks[self.cur_ind].token
            self.cur_ind += 1
            self.symbol_table.define(nme, tpe, "arg")
            if self.toks[self.cur_ind].token == ",":
                self.create_xml_terminal()

        # Close down
        self.tab_level -= 1
        self.result += self.tab_level * self.tab_char + "</parameterList>\n"

        # Finishes with closing ')'
        self.create_xml_terminal()

    def compile_var_dec(self):
        """Compiles a variable declaration.
        Should look like this: var 'type' 'identifier', 'identifier', ... ;
        """

        # Open up
        self.result += self.tab_level * self.tab_char + "<varDec>\n"
        self.tab_level += 1

        # var
        self.create_xml_terminal()

        # type
        self.create_xml_terminal(increment=False)
        tpe = self.toks[self.cur_ind].token
        self.cur_ind += 1

        # name(s)
        while self.toks[self.cur_ind].token != ";":
            self.create_xml_terminal(increment=False)
            nme = self.toks[self.cur_ind].token
            self.cur_ind += 1
            self.symbol_table.define(nme, tpe, "var")
            if self.toks[self.cur_ind].token == ",":
                self.create_xml_terminal()

        self.create_xml_terminal() # ;

        # Close down
        self.tab_level -= 1
        self.result += self.tab_level * self.tab_char + "</varDec>\n"

    def compile_statements(self):
        """Compiles a series of statements not including the enclosing {}"""

        # Open up
        self.result += self.tab_level * self.tab_char + "<statements>\n"
        self.tab_level += 1

        while True:
            if self.toks[self.cur_ind].token == "let":
                self.compile_let()
            elif self.toks[self.cur_ind].token == "if":
                self.compile_if()
            elif self.toks[self.cur_ind].token == "while":
                self.compile_while()
            elif self.toks[self.cur_ind].token == "do":
                self.compile_do()
            elif self.toks[self.cur_ind].token == "return":
                self.compile_return()
            else:
                break

        # Close down
        self.tab_level -= 1
        self.result += self.tab_level * self.tab_char + "</statements>\n"

    def compile_do(self):
        """Compiles a do statement
        do subroutineCall ;
        """

        # Open up
        self.result += self.tab_level * self.tab_char + "<doStatement>\n"
        self.tab_level += 1

        self.create_xml_terminal() # do

        self.compile_subroutine_call()

        self.create_xml_terminal() # ;

        self.vmcode += "pop temp 0\n" # Need to ignore void return

        # Close down
        self.tab_level -= 1
        self.result += self.tab_level * self.tab_char + "</doStatement>\n"


    def compile_let(self):
        """Compiles a let statement
        let varName[expr] = expr;
        """

        # Open up
        self.result += self.tab_level * self.tab_char + "<letStatement>\n"
        self.tab_level += 1

        self.create_xml_terminal() # let

        # variable name
        var_name = self.toks[self.cur_ind].token
        self.create_xml_terminal()

        if self.toks[self.cur_ind].token == "[":
            self.create_xml_terminal()
            while is_term(self.toks[self.cur_ind]):
                self.compile_expression()
            self.create_xml_terminal()

        self.create_xml_terminal() # =

        while is_term(self.toks[self.cur_ind]):
            self.compile_expression()

        self.create_xml_terminal() # ;

        # Pop the top of the stack into the appropriate segment
        seg = SEGMENT[self.symbol_table.kind_of(var_name)]
        var_ind = self.symbol_table.index_of(var_name)
        self.vmcode += "pop " + seg + " " + str(var_ind) + "\n"

        # Close down
        self.tab_level -= 1
        self.result += self.tab_level * self.tab_char + "</letStatement>\n"


    def compile_while(self):
        """Compile a while statement
        while (expr) {statements}
        """

        # Remember this index and increment immediately
        this_ind = self.counts["while"]
        self.counts["while"] += 1

        # Open up
        self.result += self.tab_level * self.tab_char + "<whileStatement>\n"
        self.tab_level += 1

        # Label the beginning
        self.vmcode += "label WHILE_EXP" + str(this_ind) + "\n"

        self.create_xml_terminal() # while

        self.create_xml_terminal() # (
        while is_term(self.toks[self.cur_ind]):
            self.compile_expression()
        self.create_xml_terminal() # )

        # Check the condition
        self.vmcode += "not\nif-goto WHILE_END" + str(this_ind) + "\n"

        self.create_xml_terminal() # {
        self.compile_statements()
        self.create_xml_terminal() # }

        # Close down
        self.tab_level -= 1
        self.result += self.tab_level * self.tab_char + "</whileStatement>\n"

        # Back to the start
        self.vmcode += "goto WHILE_EXP" + str(this_ind) + "\n"

        # Label the end
        self.vmcode += "label WHILE_END" + str(this_ind) + "\n"

    def compile_return(self):
        """Compiles a return statement
        return expression? ;
        """

        # Open up
        self.result += self.tab_level * self.tab_char + "<returnStatement>\n"
        self.tab_level += 1

        self.create_xml_terminal() # return

        is_void = True
        while is_term(self.toks[self.cur_ind]):
            is_void = False
            self.compile_expression()

        # Void return
        if is_void:
            self.vmcode += "push constant 0\n"

        self.vmcode += "return\n"

        self.create_xml_terminal() # ;

        # Close down
        self.tab_level -= 1
        self.result += self.tab_level * self.tab_char + "</returnStatement>\n"

    def compile_if(self):
        """Compiles an if statement, possibly trailing else
        if (expr) {statements} else {statements}
        """

        # Remember this index and increment immediately
        this_ind = self.counts["if"]
        self.counts["if"] += 1

        # Open up
        self.result += self.tab_level * self.tab_char + "<ifStatement>\n"
        self.tab_level += 1

        self.create_xml_terminal() # if

        self.create_xml_terminal() # (
        while is_term(self.toks[self.cur_ind]):
            self.compile_expression()
        self.create_xml_terminal() # )

        # Flow control here
        self.vmcode += "if-goto IF_TRUE" + str(this_ind) + "\n" + \
            "goto IF_FALSE" + str(this_ind) + "\n" + \
            "label IF_TRUE" + str(this_ind) + "\n"

        self.create_xml_terminal() # {
        self.compile_statements()
        self.create_xml_terminal() # }

        if self.toks[self.cur_ind].token == "else":
            self.vmcode += "goto IF_END" + str(this_ind) + "\n"
            self.vmcode += "label IF_FALSE" + str(this_ind) + "\n"
            self.create_xml_terminal() # else
            self.create_xml_terminal() # {
            self.compile_statements()
            self.create_xml_terminal() # }
            self.vmcode += "label IF_END" + str(this_ind) + "\n"

        else:
            self.vmcode += "label IF_FALSE" + str(this_ind) + "\n"

        # Close down
        self.tab_level -= 1
        self.result += self.tab_level * self.tab_char + "</ifStatement>\n"

    def compile_expression(self):
        """Compiles an expression.
        term (op term)*
        """

        # Open up
        self.result += self.tab_level * self.tab_char + "<expression>\n"
        self.tab_level += 1

        self.compile_term()

        while is_op(self.toks[self.cur_ind]):
            # Operator
            oper = self.toks[self.cur_ind].token
            self.create_xml_terminal()
            self.compile_term()
            self.vmcode += OPER[oper]

        # Close down
        self.tab_level -= 1
        self.result += self.tab_level * self.tab_char + "</expression>\n"

    def compile_term(self):
        """Compiles a term"""

        # Open up
        self.result += self.tab_level * self.tab_char + "<term>\n"
        self.tab_level += 1

        if self.toks[self.cur_ind].toktype == "stringConstant":
            self.create_xml_terminal()
        elif self.toks[self.cur_ind].toktype == "integerConstant":
            integ = self.toks[self.cur_ind].token
            self.vmcode += "push constant " + integ + "\n"
            self.create_xml_terminal()
        elif self.toks[self.cur_ind].token in KEYWORD_CONSTANTS.keys():
            self.vmcode += KEYWORD_CONSTANTS[self.toks[self.cur_ind].token]
            self.create_xml_terminal()
        elif self.toks[self.cur_ind].token == "(":
            self.create_xml_terminal() # (
            while is_term(self.toks[self.cur_ind]):
                self.compile_expression()
            self.create_xml_terminal() # )
        elif self.toks[self.cur_ind].token in UNARY_OP:
            self.create_xml_terminal() # For the unary operator
            self.compile_term()
            self.vmcode += "not\n" # Both - and ~ corrspond to this
        else:
            if self.toks[self.cur_ind].toktype != "identifier":
                raise UnexpectedToken(self.toks[self.cur_ind])
            if self.toks[self.cur_ind + 1].token == "[":
                self.create_xml_terminal()
                self.create_xml_terminal()
                while is_term(self.toks[self.cur_ind]):
                    self.compile_expression()
                self.create_xml_terminal()
            elif self.toks[self.cur_ind + 1].token in ["(", "."]:
                self.compile_subroutine_call()

            # Presumably we found a variable identifier
            else:
                var_name = self.toks[self.cur_ind].token
                self.create_xml_terminal()
                seg = SEGMENT[self.symbol_table.kind_of(var_name)]
                var_ind = self.symbol_table.index_of(var_name)
                self.vmcode += "push " + seg + " " + str(var_ind) + "\n"

        # Close down
        self.tab_level -= 1
        self.result += self.tab_level * self.tab_char + "</term>\n"


    def compile_expression_list(self):
        """Compiles a possibly empty comma-separated list of expressions"""

        # Open up
        self.result += self.tab_level * self.tab_char + "<expressionList>\n"
        self.tab_level += 1

        exp_count = 0
        while is_term(self.toks[self.cur_ind]):
            exp_count += 1
            self.compile_expression()
            if self.toks[self.cur_ind].token == ",":
                self.create_xml_terminal()

        # Close down
        self.tab_level -= 1
        self.result += self.tab_level * self.tab_char + "</expressionList>\n"

        return exp_count

    def compile_subroutine_call(self):
        """"Compiles a call like
        ClassName.subName(exprList) or
        subName(exprList)
        """

        # Figure out the name of the call

        ## Class (or subroutine) name
        smth_nme = self.toks[self.cur_ind].token
        smth_nme_class = self.resolve_symbol(smth_nme)
        ## I assume this is how methods work
        if smth_nme != smth_nme_class:
            self.vmcode += "push " + \
                SEGMENT[self.symbol_table.kind_of(smth_nme)] + " " + \
                str(self.symbol_table.index_of(smth_nme)) + "\n"
            add_arg = 1
        else:
            add_arg = 0
        smth_nme = smth_nme_class
        self.create_xml_terminal()
        ## See if there is a dot
        if self.toks[self.cur_ind].token == ".":
            self.create_xml_terminal() # .
            smth_nme += "." + self.toks[self.cur_ind].token
            self.create_xml_terminal() # subroutine name
        ## I guess if there isn't then it's a method
        else:
            self.vmcode += "push pointer 0\n"
            smth_nme = self.class_name + "." + smth_nme
            add_arg = 1

        self.create_xml_terminal() # (
        exp_n = self.compile_expression_list() + add_arg
        self.create_xml_terminal() # )

        # Write the VM code
        self.vmcode += "call " + smth_nme + " " + str(exp_n) + "\n"

    def create_xml_terminal(self, increment=True):
        """Creates a string for xml writing"""
        self.result += self.tab_level * self.tab_char + \
            build_terminal(self.toks[self.cur_ind])
        if increment:
            self.cur_ind += 1

    def resolve_symbol(self, smth_name):
        """Resolves a symbol (eg. replaces variable name with class name"""
        for iden in self.symbol_table.subroutine_scope:
            if iden.name == smth_name:
                return iden.type
        for iden in self.symbol_table.class_scope:
            if iden.name == smth_name:
                return iden.type
        return smth_name
