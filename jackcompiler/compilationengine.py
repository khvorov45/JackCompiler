"""CompilationEngine class.
Does not have a huge amount of error checking, will likely only work with
correctly written .jack classes.
"""

from .utilities import build_terminal
from .glossary import is_term, is_op, KEYWORD_CONSTANTS, UNARY_OP, OPER, SEGMENT
from .symboltable import SymbolTable

class UnexpectedToken(Exception):
    """Exception raised for unexpected tokens in input"""
    def __init__(self, tok):
        super().__init__("unexpected token: " + tok.token)

class CompilationEngine():
    """Controls compilation

    Arguments:
        self.tokens -- list of tokens (TokenInfo class).
            Should represent one class.
        out_file_path -- path to the file to write translation to
    """
    # pylint: disable=too-many-instance-attributes
    def __init__(self):
        self._tokens = None
        self._cur_ind = None
        self._xml_tree = None
        self._vmcode = None
        self._symbol_table = SymbolTable()
        self._tab_char = "  "
        self._tab_level = 1
        self._class_name = ""
        self._loop_counts = {"while": 0, "if": 0}

    @property
    def tokens(self):
        """A list of tokens"""
        return self._tokens

    @tokens.setter
    def tokens(self, toks):
        if not isinstance(toks, list):
            raise TypeError("tokens should be a list")
        self._tokens = toks
        self._cur_ind = 0
        self._xml_tree = ""
        self._vmcode = ""

    @property
    def tab_char(self):
        """Tab character"""
        return self._tab_char

    @tab_char.setter
    def tab_char(self, string):
        if not isinstance(string, str):
            raise TypeError("tab_char should be a string")
        self._tab_char = string

    def compile_class(self):
        """Compiles the entire class"""

        # First token is 'class'
        if self.tokens[self._cur_ind]["value"] != "class":
            raise UnexpectedToken(self.tokens[self._cur_ind])
        self._xml_tree += "<class>\n"
        self._append_xml_terminal()

        # Second token is the class name. These do not go into the symbol table.
        if self.tokens[self._cur_ind]["type"] != "identifier":
            raise UnexpectedToken(self.tokens[self._cur_ind])
        self._class_name = self.tokens[self._cur_ind].token
        self._append_xml_terminal()

        # Opening '{'
        self._append_xml_terminal()

        # Class variables
        while self.tokens[self._cur_ind]["value"] in ["static", "field"]:
            self.compile_class_var_dec()

        # Print the symbol table
        print(self._class_name + " SYMBOL TABLE")
        self._symbol_table.print(sub=False)

        # Subroutines
        while self.tokens[self._cur_ind].token in \
            ["constructor", "function", "method"]:
            self.compile_subroutine()

        # Closing '}'
        self._append_xml_terminal()

        # Finish up the class
        self._xml_tree += "</class>\n"

        # Write xml to translation file
        out_file = open(self.out_file_path, "w+")
        out_file.write(self._xml_tree)
        out_file.close()

        # Write VM
        vm_file = self.out_file_path.replace(".xml", ".vm")
        out_file = open(vm_file, "w+")
        out_file.write(self._vmcode)
        out_file.close()

    def compile_class_var_dec(self):
        """Compiles class variable declarations"""

        # Open up
        self._xml_tree += self._tab_level * self.tab_char + "<classVarDec>\n"
        self._tab_level += 1

        # All of these should be in the symbol table

        # 'static' or 'field'
        self._append_xml_terminal(increment=False)
        knd = self.tokens[self._cur_ind].token
        self._cur_ind += 1

        # type
        self._append_xml_terminal(increment=False)
        tpe = self.tokens[self._cur_ind].token
        self._cur_ind += 1

        # name(s)
        while self.tokens[self._cur_ind].token != ";":
            self._append_xml_terminal(increment=False)
            nme = self.tokens[self._cur_ind].token
            self._cur_ind += 1
            self._symbol_table.define(nme, tpe, knd)
            if self.tokens[self._cur_ind].token == ",":
                self._append_xml_terminal()

        self._append_xml_terminal() # ;

        # Close down
        self._tab_level -= 1
        self._xml_tree += self._tab_level * self.tab_char + "</classVarDec>\n"

    def compile_subroutine(self):
        """Compiles a subroutine"""

        # Open up
        self._xml_tree += self._tab_level * self.tab_char + "<subroutineDec>\n"
        self._tab_level += 1

        # Reset the subroutine's symbol table
        self._symbol_table.start_subroutine()

        # This reset is unnecessary, it is to conform to ECS's compiler
        self._loop_counts["while"] = 0
        self._loop_counts["if"] = 0

        # Subroutine type
        subroutine_type = self.tokens[self._cur_ind].token
        if subroutine_type not in \
            ["constructor", "function", "method"]:
            raise UnexpectedToken(subroutine_type)
        self._append_xml_terminal()

        # Next is the return type
        self._append_xml_terminal()

        # Then is the name, not placing this in the symbol table.
        subroutine_name = self.tokens[self._cur_ind].token
        self._append_xml_terminal()

        # Then is the parameter list.
        # All arguments should be in the symbol table.
        if subroutine_type == "method":
            self._symbol_table.subroutine_arg_ind += 1
        self.compile_parameter_list()

        # Then is the subroutine body
        self._xml_tree += self._tab_level * self.tab_char + "<subroutineBody>\n"
        self._tab_level += 1

        # First is the opening '{'
        self._append_xml_terminal()

        # Then all the variables. All of these will go into the symbol table.
        while self.tokens[self._cur_ind].token == "var":
            self.compile_var_dec()

        # Label the subroutine
        self._vmcode += "function " + self._class_name + "." + subroutine_name + \
            " " + str(self._symbol_table.var_count("var")) + "\n"

        # Possibly required extra stuff
        if subroutine_type == "constructor":
            field_count = self._symbol_table.var_count("field")
            self._vmcode += "push constant " + str(field_count) + "\n" + \
                "call Memory.alloc 1\npop pointer 0\n"
        elif subroutine_type == "method":
            self._vmcode += "push argument 0\npop pointer 0\n"

        # Then all the statements
        self.compile_statements()

        # Closing '}'
        self._append_xml_terminal()

        # Print the symbol table
        print(subroutine_name + " SYMBOL TABLE")
        self._symbol_table.print(cla=False)

        # Finish the subroutine
        self._tab_level -= 1
        self._xml_tree += self._tab_level * self.tab_char + "</subroutineBody>\n"
        self._tab_level -= 1
        self._xml_tree += self._tab_level * self.tab_char + "</subroutineDec>\n"

    def compile_parameter_list(self):
        """Compiles a parameter list (possibly empty)"""

        # First is the opening '('
        self._append_xml_terminal()

        # Open up
        self._xml_tree += self._tab_level * self.tab_char + "<parameterList>\n"
        self._tab_level += 1

        # Then come the parameters
        while self.tokens[self._cur_ind].token != ")":
            # Type
            tpe = self.tokens[self._cur_ind].token
            self._append_xml_terminal()
            # Name
            nme = self.tokens[self._cur_ind].token
            self._append_xml_terminal()
            self._symbol_table.define(nme, tpe, "arg")
            if self.tokens[self._cur_ind].token == ",":
                self._append_xml_terminal()

        # Close down
        self._tab_level -= 1
        self._xml_tree += self._tab_level * self.tab_char + "</parameterList>\n"

        # Finishes with closing ')'
        self._append_xml_terminal()

    def compile_var_dec(self):
        """Compiles a variable declaration.
        Should look like this: var 'type' 'identifier', 'identifier', ... ;
        """

        # Open up
        self._xml_tree += self._tab_level * self.tab_char + "<varDec>\n"
        self._tab_level += 1

        # var
        self._append_xml_terminal()

        # type
        self._append_xml_terminal(increment=False)
        tpe = self.tokens[self._cur_ind].token
        self._cur_ind += 1

        # name(s)
        while self.tokens[self._cur_ind].token != ";":
            self._append_xml_terminal(increment=False)
            nme = self.tokens[self._cur_ind].token
            self._cur_ind += 1
            self._symbol_table.define(nme, tpe, "var")
            if self.tokens[self._cur_ind].token == ",":
                self._append_xml_terminal()

        self._append_xml_terminal() # ;

        # Close down
        self._tab_level -= 1
        self._xml_tree += self._tab_level * self.tab_char + "</varDec>\n"

    def compile_statements(self):
        """Compiles a series of statements not including the enclosing {}"""

        # Open up
        self._xml_tree += self._tab_level * self.tab_char + "<statements>\n"
        self._tab_level += 1

        while True:
            if self.tokens[self._cur_ind].token == "let":
                self.compile_let()
            elif self.tokens[self._cur_ind].token == "if":
                self.compile_if()
            elif self.tokens[self._cur_ind].token == "while":
                self.compile_while()
            elif self.tokens[self._cur_ind].token == "do":
                self.compile_do()
            elif self.tokens[self._cur_ind].token == "return":
                self.compile_return()
            else:
                break

        # Close down
        self._tab_level -= 1
        self._xml_tree += self._tab_level * self.tab_char + "</statements>\n"

    def compile_do(self):
        """Compiles a do statement
        do subroutineCall ;
        """

        # Open up
        self._xml_tree += self._tab_level * self.tab_char + "<doStatement>\n"
        self._tab_level += 1

        self._append_xml_terminal() # do

        self.compile_subroutine_call()

        self._append_xml_terminal() # ;

        self._vmcode += "pop temp 0\n" # Need to ignore void return

        # Close down
        self._tab_level -= 1
        self._xml_tree += self._tab_level * self.tab_char + "</doStatement>\n"


    def compile_let(self):
        """Compiles a let statement
        let varName[expr] = expr;
        """

        # Open up
        self._xml_tree += self._tab_level * self.tab_char + "<letStatement>\n"
        self._tab_level += 1

        self._append_xml_terminal() # let

        # Variable name
        var_name = self.tokens[self._cur_ind].token
        self._append_xml_terminal()

        # Array entry
        is_array_entry = False
        if self.tokens[self._cur_ind].token == "[":
            is_array_entry = True
            self._append_xml_terminal() # [
            while is_term(self.tokens[self._cur_ind]):
                self.compile_expression()
            self._append_xml_terminal() # ]
            self.push_variable(var_name)
            self._vmcode += "add\n"

        self._append_xml_terminal() # =

        while is_term(self.tokens[self._cur_ind]):
            self.compile_expression()

        self._append_xml_terminal() # ;

        # Pop the top of the stack into the appropriate segment
        if is_array_entry:
            # Store return, store address of entry, push return and store
            self._vmcode += \
                "pop temp 0\npop pointer 1\npush temp 0\npop that 0\n"
        else:
            seg = SEGMENT[self._symbol_table.kind_of(var_name)]
            var_ind = self._symbol_table.index_of(var_name)
            self._vmcode += "pop " + seg + " " + str(var_ind) + "\n"

        # Close down
        self._tab_level -= 1
        self._xml_tree += self._tab_level * self.tab_char + "</letStatement>\n"


    def compile_while(self):
        """Compile a while statement
        while (expr) {statements}
        """

        # Remember this index and increment immediately
        this_ind = self._loop_counts["while"]
        self._loop_counts["while"] += 1

        # Open up
        self._xml_tree += self._tab_level * self.tab_char + "<whileStatement>\n"
        self._tab_level += 1

        # Label the beginning
        self._vmcode += "label WHILE_EXP" + str(this_ind) + "\n"

        self._append_xml_terminal() # while

        self._append_xml_terminal() # (
        while is_term(self.tokens[self._cur_ind]):
            self.compile_expression()
        self._append_xml_terminal() # )

        # Check the condition
        self._vmcode += "not\nif-goto WHILE_END" + str(this_ind) + "\n"

        self._append_xml_terminal() # {
        self.compile_statements()
        self._append_xml_terminal() # }

        # Close down
        self._tab_level -= 1
        self._xml_tree += self._tab_level * self.tab_char + "</whileStatement>\n"

        # Back to the start
        self._vmcode += "goto WHILE_EXP" + str(this_ind) + "\n"

        # Label the end
        self._vmcode += "label WHILE_END" + str(this_ind) + "\n"

    def compile_return(self):
        """Compiles a return statement
        return expression? ;
        """

        # Open up
        self._xml_tree += self._tab_level * self.tab_char + "<returnStatement>\n"
        self._tab_level += 1

        self._append_xml_terminal() # return

        is_void = True
        while is_term(self.tokens[self._cur_ind]):
            is_void = False
            self.compile_expression()

        # Void return
        if is_void:
            self._vmcode += "push constant 0\n"

        self._vmcode += "return\n"

        self._append_xml_terminal() # ;

        # Close down
        self._tab_level -= 1
        self._xml_tree += self._tab_level * self.tab_char + "</returnStatement>\n"

    def compile_if(self):
        """Compiles an if statement, possibly trailing else
        if (expr) {statements} else {statements}
        """

        # Remember this index and increment immediately
        this_ind = self._loop_counts["if"]
        self._loop_counts["if"] += 1

        # Open up
        self._xml_tree += self._tab_level * self.tab_char + "<ifStatement>\n"
        self._tab_level += 1

        self._append_xml_terminal() # if

        self._append_xml_terminal() # (
        while is_term(self.tokens[self._cur_ind]):
            self.compile_expression()
        self._append_xml_terminal() # )

        # Flow control here
        self._vmcode += "if-goto IF_TRUE" + str(this_ind) + "\n" + \
            "goto IF_FALSE" + str(this_ind) + "\n" + \
            "label IF_TRUE" + str(this_ind) + "\n"

        self._append_xml_terminal() # {
        self.compile_statements()
        self._append_xml_terminal() # }

        if self.tokens[self._cur_ind].token == "else":
            self._vmcode += "goto IF_END" + str(this_ind) + "\n"
            self._vmcode += "label IF_FALSE" + str(this_ind) + "\n"
            self._append_xml_terminal() # else
            self._append_xml_terminal() # {
            self.compile_statements()
            self._append_xml_terminal() # }
            self._vmcode += "label IF_END" + str(this_ind) + "\n"

        else:
            self._vmcode += "label IF_FALSE" + str(this_ind) + "\n"

        # Close down
        self._tab_level -= 1
        self._xml_tree += self._tab_level * self.tab_char + "</ifStatement>\n"

    def compile_expression(self):
        """Compiles an expression.
        term (op term)*
        """

        # Open up
        self._xml_tree += self._tab_level * self.tab_char + "<expression>\n"
        self._tab_level += 1

        self.compile_term()

        while is_op(self.tokens[self._cur_ind]):
            # Operator
            oper = self.tokens[self._cur_ind].token
            self._append_xml_terminal()
            self.compile_term()
            self._vmcode += OPER[oper]

        # Close down
        self._tab_level -= 1
        self._xml_tree += self._tab_level * self.tab_char + "</expression>\n"

    def compile_term(self):
        """Compiles a term"""

        # Open up
        self._xml_tree += self._tab_level * self.tab_char + "<term>\n"
        self._tab_level += 1

        # String
        if self.tokens[self._cur_ind].toktype == "stringConstant":
            stri = self.tokens[self._cur_ind].tokval
            print(stri)
            self._vmcode += "push constant " + str(len(stri)) + \
                "\ncall String.new 1\n"
            for char in stri:
                self._vmcode += "push constant " + str(ord(char)) + \
                    "\ncall String.appendChar 2\n"
            self._append_xml_terminal()

        # Integer
        elif self.tokens[self._cur_ind].toktype == "integerConstant":
            integ = self.tokens[self._cur_ind].token
            self._vmcode += "push constant " + integ + "\n"
            self._append_xml_terminal()

        # Keyword
        elif self.tokens[self._cur_ind].token in KEYWORD_CONSTANTS.keys():
            self._vmcode += KEYWORD_CONSTANTS[self.tokens[self._cur_ind].token]
            self._append_xml_terminal()

        # Experssion in brackets
        elif self.tokens[self._cur_ind].token == "(":
            self._append_xml_terminal() # (
            while is_term(self.tokens[self._cur_ind]):
                self.compile_expression()
            self._append_xml_terminal() # )

        # Unary operator
        elif self.tokens[self._cur_ind].token in UNARY_OP.keys():
            oper = self.tokens[self._cur_ind].token
            self._append_xml_terminal() # For the unary operator
            self.compile_term()
            self._vmcode += UNARY_OP[oper]

        # This has to be an identifier
        else:
            if self.tokens[self._cur_ind].toktype != "identifier":
                raise UnexpectedToken(self.tokens[self._cur_ind])

            # Array entry
            if self.tokens[self._cur_ind + 1].token == "[":

                # Array name
                array_name = self.tokens[self._cur_ind].token
                self._append_xml_terminal()

                self._append_xml_terminal() # [
                while is_term(self.tokens[self._cur_ind]):
                    self.compile_expression()
                self._append_xml_terminal() # ]

                # Get to the segment's content
                self.push_variable(array_name)
                self._vmcode += "add\npop pointer 1\npush that 0\n"

            # Subroutine call
            elif self.tokens[self._cur_ind + 1].token in ["(", "."]:
                self.compile_subroutine_call()

            # Presumably we found a variable identifier
            else:
                self.push_variable()

        # Close down
        self._tab_level -= 1
        self._xml_tree += self._tab_level * self.tab_char + "</term>\n"


    def compile_expression_list(self):
        """Compiles a possibly empty comma-separated list of expressions"""

        # Open up
        self._xml_tree += self._tab_level * self.tab_char + "<expressionList>\n"
        self._tab_level += 1

        exp_count = 0
        while is_term(self.tokens[self._cur_ind]):
            exp_count += 1
            self.compile_expression()
            if self.tokens[self._cur_ind].token == ",":
                self._append_xml_terminal()

        # Close down
        self._tab_level -= 1
        self._xml_tree += self._tab_level * self.tab_char + "</expressionList>\n"

        return exp_count

    def compile_subroutine_call(self):
        """"Compiles a call like
        ClassName.subName(exprList) or
        subName(exprList)
        """

        # Figure out the name of the call

        ## Class (or subroutine) name
        smth_nme = self.tokens[self._cur_ind].token
        smth_nme_class = self.resolve_symbol(smth_nme)
        ## I assume this is how methods work
        if smth_nme != smth_nme_class:
            self._vmcode += "push " + \
                SEGMENT[self._symbol_table.kind_of(smth_nme)] + " " + \
                str(self._symbol_table.index_of(smth_nme)) + "\n"
            add_arg = 1
        else:
            add_arg = 0
        smth_nme = smth_nme_class
        self._append_xml_terminal()
        ## See if there is a dot
        if self.tokens[self._cur_ind].token == ".":
            self._append_xml_terminal() # .
            smth_nme += "." + self.tokens[self._cur_ind].token
            self._append_xml_terminal() # subroutine name
        ## I guess if there isn't then it's a method
        else:
            self._vmcode += "push pointer 0\n"
            smth_nme = self._class_name + "." + smth_nme
            add_arg = 1

        self._append_xml_terminal() # (
        exp_n = self.compile_expression_list() + add_arg
        self._append_xml_terminal() # )

        # Write the VM code
        self._vmcode += "call " + smth_nme + " " + str(exp_n) + "\n"

    def _append_xml_terminal(self, increment=True):
        """Creates a string for xml writing"""
        self._xml_tree += self._tab_level * self.tab_char + \
            build_terminal(self.tokens[self._cur_ind])
        if increment:
            self._cur_ind += 1

    def resolve_symbol(self, smth_name):
        """Resolves a symbol (eg. replaces variable name with class name"""
        for iden in self._symbol_table.subroutine_scope:
            if iden.name == smth_name:
                return iden.type
        for iden in self._symbol_table.class_scope:
            if iden.name == smth_name:
                return iden.type
        return smth_name

    def push_variable(self, var_name=None):
        """Pushes the variable identiefied onto the stack"""
        advance = False
        if var_name is None:
            var_name = self.tokens[self._cur_ind].token
            advance = True
        seg = SEGMENT[self._symbol_table.kind_of(var_name)]
        var_ind = self._symbol_table.index_of(var_name)
        self._vmcode += "push " + seg + " " + str(var_ind) + "\n"
        if advance:
            self._append_xml_terminal()
