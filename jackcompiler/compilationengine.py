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
        super().__init__("unexpected token: " + tok["value"])

class Vmtranslator():
    """Creates VM code"""
    def __init__(self):
        self._class_name = None
        self._vmcode = None
        self._loop_counts = None

    @property
    def class_name(self):
        """Name of the current class"""
        return self._class_name

    @class_name.setter
    def class_name(self, nme):
        if not isinstance(nme, str):
            raise TypeError("class_name should be a string")
        self._class_name = nme
        self._vmcode = ""
        self._loop_counts = {"while": 0, "if": 0}

    def get_vmcode(self):
        """Returns the VM code"""
        return self._vmcode

    def get_loop_counts(self):
        """Returns the loop indeces"""
        return self._loop_counts

    def start_subroutine(self, subname, varcount, subtype, fieldcount):
        """Resets for a new subroutine"""
        self._loop_counts["while"] = 0
        self._loop_counts["if"] = 0
        self._vmcode += "function " + self._class_name + "." + subname + \
            " " + str(varcount) + "\n"
        if subtype == "constructor":
            self._vmcode += "push constant " + str(fieldcount) + "\n" + \
                "call Memory.alloc 1\npop pointer 0\n"
        elif subtype == "method":
            self._vmcode += "push argument 0\npop pointer 0\n"

    def ignore_void_return(self):
        """Writes the void return"""
        self._vmcode += "pop temp 0\n"

    def return_statement(self, void):
        """Writes the void return"""
        if void:
            self._vmcode += "push constant 0\n"
        self._vmcode += "return\n"

    def let_statement(self, is_array_entry, seg, var_ind):
        """Writes code for a let statement"""
        if is_array_entry:
            # Store return, store address of entry, push return and store
            self._vmcode += "pop temp 0\npop pointer 1\n" + \
                "push temp 0\npop that 0\n"
        else:
            self._vmcode += "pop " + seg + " " + str(var_ind) + "\n"

    def open_while(self):
        """Writes code for a while statement"""
        this_ind = self._loop_counts["while"]
        self._vmcode += "label WHILE_EXP" + str(this_ind) + "\n"
        self._loop_counts["while"] += 1
        return this_ind

    def check_while(self, ind):
        """Code to check the while condition"""
        self._vmcode += "not\nif-goto WHILE_END" + str(ind) + "\n"

    def close_while(self, ind):
        """Closes the while statement"""
        self._vmcode += "goto WHILE_EXP" + str(ind) + \
            "\nlabel WHILE_END" + str(ind) + "\n"

    def open_if(self):
        """Opens the if statement"""
        this_ind = self._loop_counts["if"]
        self._loop_counts["if"] += 1
        return this_ind

    def if_flow(self, ind):
        """If statement flow control"""
        self._vmcode += "if-goto IF_TRUE" + str(ind) + "\n" + \
            "goto IF_FALSE" + str(ind) + "\n" + \
            "label IF_TRUE" + str(ind) + "\n"

    def if_close(self, ind, else_present):
        """Closes the if statement"""
        if else_present:
            self._vmcode += "label IF_END" + str(ind) + "\n"
        else:
            self._vmcode += "label IF_FALSE" + str(ind) + "\n"

    def else_clause(self, ind):
        """Writes the else clause"""
        self._vmcode += "goto IF_END" + str(ind) + \
            "\nlabel IF_FALSE" + str(ind) + "\n"

    def operator(self, oper, unary):
        """Writes code appropriate for the operator"""
        if unary:
            self._vmcode += UNARY_OP[oper]
        else:
            self._vmcode += OPER[oper]

    def write_term(self, term, knd):
        """Writes a term"""
        if knd == "string":
            self._vmcode += "push constant " + str(len(term)) + \
            "\ncall String.new 1\n"
            for char in term:
                self._vmcode += "push constant " + str(ord(char)) + \
                    "\ncall String.appendChar 2\n"
        elif knd == "int":
            self._vmcode += "push constant " + term + "\n"
        elif knd == "key":
            self._vmcode += KEYWORD_CONSTANTS[term]

    def array_entry(self):
        """Writes code for array entry"""
        self._vmcode += "add\npop pointer 1\npush that 0\n"

    def push_statement(self, seg, ind):
        """Writes a push statement"""
        self._vmcode += "push " + seg + " " + str(ind) + "\n"

    def call(self, call_name, exp_n):
        """Writes a call"""
        self._vmcode += "call " + call_name + " " + str(exp_n) + "\n"

    def add(self):
        """Writes the add command"""
        self._vmcode += "add\n"


class Xmltranslator():
    """Creates the xml tree"""
    def __init__(self):
        self._xml_tree = ""
        self._tab_char = "  "
        self._tab_level = 0

    @property
    def tab_char(self):
        """Tab character"""
        return self._tab_char

    @tab_char.setter
    def tab_char(self, string):
        if not isinstance(string, str):
            raise TypeError("tab_char should be a string")
        self._tab_char = string

    def get_xml_tree(self):
        """Returns the xml tree"""
        return self._xml_tree

    def open_section(self, secname):
        """Opens a section"""
        self._xml_tree += self._tab_level * self.tab_char + \
            "<" + secname + ">\n"
        self._tab_level += 1

    def close_section(self, secname):
        """Closes a section"""
        self._tab_level -= 1
        self._xml_tree += self._tab_level * self.tab_char + \
            "</" + secname + ">\n"

    def append_terminal(self, tok):
        """Creates a string for xml writing"""
        self._xml_tree += self._tab_level * self.tab_char + build_terminal(tok)

class CompilationEngine():
    """Controls compilation

    Arguments:
        self.tokens -- list of tokens (TokenInfo class).
            Should represent one class.
        out_file_path -- path to the file to write translation to
    """
    def __init__(self):
        self._tokens = None
        self._cur_ind = None
        self._compiled = None
        self._symbol_table = SymbolTable()
        self._xmltranslator = Xmltranslator()
        self._vmtranslator = Vmtranslator()

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
        self._compiled = False
        self._symbol_table.__init__()
        self._xmltranslator.__init__()
        self._vmtranslator.__init__()

    def get_xml_tree(self):
        """Returns the xml tree"""
        if not self._compiled:
            self._compile_class()
        return self._xmltranslator.get_xml_tree()

    def get_vmcode(self):
        """Returns the VM code"""
        if not self._compiled:
            self.compile()
        return self._vmtranslator.get_vmcode()

    def _append_xml_terminal(self):
        """Appends a terminal"""
        self._xmltranslator.append_terminal(self.tokens[self._cur_ind])
        self._cur_ind += 1

    def _process_token(self, check=None, ideal=None):
        """Checks that the token is appropriate and appends it"""
        if (check is not None) and (ideal is not None):
            if not isinstance(ideal, list):
                ideal = [ideal]
            if self.tokens[self._cur_ind][check] not in ideal:
                raise UnexpectedToken(self.tokens[self._cur_ind])
        self._append_xml_terminal()

    def compile(self):
        """Runs the compilations process"""
        self._compile_class()

    def _compile_class(self):
        """Compiles the entire class"""

        self._xmltranslator.open_section("class")

        # The first three tokens
        self._process_token("value", "class")
        self._vmtranslator.class_name = self.tokens[self._cur_ind]["value"]
        self._process_token("type", "identifier")
        self._process_token("value", "{")

        # Class variables
        while self.tokens[self._cur_ind]["value"] in ["static", "field"]:
            self._compile_class_var_dec()

        # Subroutines
        while self.tokens[self._cur_ind]["value"] in \
            ["constructor", "function", "method"]:
            self._compile_subroutine()

        # Closing '}'
        self._process_token("value", "}")

        # Finish up the class
        self._xmltranslator.close_section("class")
        self._compiled = True

    def _compile_class_var_dec(self):
        """Compiles class variable declarations"""
        self._xmltranslator.open_section("classVarDec")

        # All of these should be in the symbol table

        # Variable kind (static or field)
        knd = self.tokens[self._cur_ind]["value"]
        self._process_token("value", ["static", "field"])

        # Variable type
        tpe = self.tokens[self._cur_ind]["value"]
        self._process_token("type", ["keyword", "identifier"])

        # Variable name(s)
        while self.tokens[self._cur_ind]["value"] != ";":
            nme = self.tokens[self._cur_ind]["value"]
            self._process_token("type", "identifier")
            self._symbol_table.define(nme, tpe, knd)
            if self.tokens[self._cur_ind]["value"] == ",":
                self._process_token()

        self._process_token("value", ";")
        self._xmltranslator.close_section("classVarDec")

    def _compile_subroutine(self):
        """Compiles a subroutine"""

        self._xmltranslator.open_section("subroutineDec")

        # Subroutine type
        subroutine_type = self.tokens[self._cur_ind]["value"]
        self._symbol_table.subroutine_type = subroutine_type
        self._process_token("value", ["constructor", "function", "method"])

        # Next is the return type
        self._process_token("type", ["keyword", "identifier"])

        # Then is the name, not placing this in the symbol table.
        subroutine_name = self.tokens[self._cur_ind]["value"]
        self._process_token("type", "identifier")

        # Then is the parameter list.
        # All arguments should be in the symbol table.
        self._compile_parameter_list()

        self._xmltranslator.open_section("subroutineBody")
        self._process_token("value", "{")

        # Then all the variables. All of these will go into the symbol table.
        while self.tokens[self._cur_ind]["value"] == "var":
            self._compile_var_dec()

        # Start VM translation
        self._vmtranslator.start_subroutine(
            subroutine_name, self._symbol_table.var_count("var"),
            subroutine_type, self._symbol_table.var_count("field")
        )

        self._compile_statements()
        self._process_token("value", "}")

        # Finish the subroutine
        self._xmltranslator.close_section("subroutineBody")
        self._xmltranslator.close_section("subroutineDec")

    def _compile_parameter_list(self):
        """Compiles a parameter list (possibly empty)"""

        self._process_token("value", "(")
        self._xmltranslator.open_section("parameterList")

        # Then come the parameters
        while self.tokens[self._cur_ind]["value"] != ")":
            tpe = self.tokens[self._cur_ind]["value"]
            self._process_token("type", ["keyword", "identifier"])
            nme = self.tokens[self._cur_ind]["value"]
            self._process_token("type", "identifier")
            self._symbol_table.define(nme, tpe, "arg")
            if self.tokens[self._cur_ind]["value"] == ",":
                self._process_token()

        self._xmltranslator.close_section("parameterList")
        self._process_token("value", ")")

    def _compile_var_dec(self):
        """Compiles a variable declaration.
        Should look like this: var 'type' 'identifier', 'identifier', ... ;
        """

        self._xmltranslator.open_section("varDec")
        self._process_token("value", "var")

        tpe = self.tokens[self._cur_ind]["value"]
        self._process_token("type", ["keyword", "identifier"])

        # Var name(s)
        while self.tokens[self._cur_ind]["value"] != ";":
            nme = self.tokens[self._cur_ind]["value"]
            self._process_token("type", "identifier")
            self._symbol_table.define(nme, tpe, "var")
            if self.tokens[self._cur_ind]["value"] == ",":
                self._process_token()

        self._process_token("value", ";")

        # Close down
        self._xmltranslator.close_section("varDec")

    def _compile_statements(self):
        """Compiles a series of statements not including the enclosing {}"""

        self._xmltranslator.open_section("statements")

        while True:
            if self.tokens[self._cur_ind]["value"] == "let":
                self._compile_let()
            elif self.tokens[self._cur_ind]["value"] == "if":
                self._compile_if()
            elif self.tokens[self._cur_ind]["value"] == "while":
                self._compile_while()
            elif self.tokens[self._cur_ind]["value"] == "do":
                self._compile_do()
            elif self.tokens[self._cur_ind]["value"] == "return":
                self._compile_return()
            else:
                break

        # Close down
        self._xmltranslator.close_section("statements")

    def _compile_do(self):
        """Compiles a do statement
        do subroutineCall ;
        """
        self._xmltranslator.open_section("doStatement")
        self._process_token("value", "do")
        self._compile_subroutine_call()
        self._process_token("value", ";")
        self._vmtranslator.ignore_void_return()
        self._xmltranslator.close_section("doStatement")

    def _compile_let(self):
        """Compiles a let statement
        let varName[expr] = expr;
        """

        self._xmltranslator.open_section("letStatement")
        self._process_token("value", "let")

        var_name = self.tokens[self._cur_ind]["value"]
        self._process_token("type", ["keyword", "identifier"])

        is_array_entry = False
        if self.tokens[self._cur_ind]["value"] == "[":
            is_array_entry = True
            self._process_token("value", "[")
            while is_term(self.tokens[self._cur_ind]):
                self._compile_expression()
            self._process_token("value", "]")
            self._push_variable(var_name)
            self._vmtranslator.add()

        self._process_token("value", "=")

        while is_term(self.tokens[self._cur_ind]):
            self._compile_expression()

        self._process_token("value", ";")

        seg = SEGMENT[self._symbol_table.kind_of(var_name)]
        var_ind = self._symbol_table.index_of(var_name)

        self._vmtranslator.let_statement(is_array_entry, seg, var_ind)

        self._xmltranslator.close_section("letStatement")

    def _compile_while(self):
        """Compile a while statement
        while (expr) {statements}
        """
        self._xmltranslator.open_section("whileStatement")
        this_ind = self._vmtranslator.open_while()
        self._process_token("value", "while")
        self._process_token("value", "(")
        while is_term(self.tokens[self._cur_ind]):
            self._compile_expression()
        self._process_token("value", ")")
        self._vmtranslator.check_while(this_ind)
        self._process_token("value", "{")
        self._compile_statements()
        self._process_token("value", "}")
        self._vmtranslator.close_while(this_ind)
        self._xmltranslator.close_section("whileStatement")

    def _compile_return(self):
        """Compiles a return statement
        return expression? ;
        """
        self._xmltranslator.open_section("returnStatement")
        self._process_token("value", "return")
        is_void = True
        while is_term(self.tokens[self._cur_ind]):
            is_void = False
            self._compile_expression()
        self._vmtranslator.return_statement(is_void)
        self._process_token("value", ";")
        self._xmltranslator.close_section("returnStatement")

    def _compile_if(self):
        """Compiles an if statement, possibly trailing else
        if (expr) {statements} else {statements}
        """

        this_ind = self._vmtranslator.open_if()

        self._xmltranslator.open_section("ifStatement")
        self._process_token("value", "if")

        self._process_token("value", "(")
        while is_term(self.tokens[self._cur_ind]):
            self._compile_expression()
        self._process_token("value", ")")

        self._vmtranslator.if_flow(this_ind)

        self._process_token("value", "{")
        self._compile_statements()
        self._process_token("value", "}")

        else_present = False
        if self.tokens[self._cur_ind]["value"] == "else":
            else_present = True
            self._vmtranslator.else_clause(this_ind)
            self._process_token("value", "else")
            self._process_token("value", "{")
            self._compile_statements()
            self._process_token("value", "}")
        self._vmtranslator.if_close(this_ind, else_present)
        self._xmltranslator.close_section("ifStatement")

    def _compile_expression(self):
        """Compiles an expression.
        term (op term)*
        """
        self._xmltranslator.open_section("expression")
        self._compile_term()
        while is_op(self.tokens[self._cur_ind]):
            oper = self.tokens[self._cur_ind]["value"]
            self._process_token()
            self._compile_term()
            self._vmtranslator.operator(oper, unary=False)
        self._xmltranslator.close_section("expression")

    def _compile_term(self):
        """Compiles a term"""

        self._xmltranslator.open_section("term")

        toktype = self.tokens[self._cur_ind]["type"]
        tokval = self.tokens[self._cur_ind]["value"]

        # String
        if toktype == "stringConstant":
            self._vmtranslator.write_term(tokval, "string")
            self._process_token()

        # Integer
        elif toktype == "integerConstant":
            self._vmtranslator.write_term(tokval, "int")
            self._process_token()

        # Keyword
        elif tokval in KEYWORD_CONSTANTS.keys():
            self._vmtranslator.write_term(tokval, "key")
            self._process_token()

        # Experssion in brackets
        elif tokval == "(":
            self._process_token()
            while is_term(self.tokens[self._cur_ind]):
                self._compile_expression()
            self._process_token("value", ")")

        # Unary operator
        elif tokval in UNARY_OP.keys():
            self._process_token() # For the unary operator
            self._compile_term()
            self._vmtranslator.operator(tokval, unary=True)

        # This has to be an identifier
        else:
            if toktype != "identifier":
                raise UnexpectedToken(self.tokens[self._cur_ind])

            # Array entry
            if self.tokens[self._cur_ind + 1]["value"] == "[":

                # Array name
                self._process_token()

                self._process_token("value", "[")
                while is_term(self.tokens[self._cur_ind]):
                    self._compile_expression()
                self._process_token("value", "]")

                # Get to the segment's content
                self._push_variable(tokval)
                self._vmtranslator.array_entry()

            # Subroutine call
            elif self.tokens[self._cur_ind + 1]["value"] in ["(", "."]:
                self._compile_subroutine_call()

            # Presumably we found a variable identifier
            else:
                self._push_variable()

        # Close down
        self._xmltranslator.close_section("term")

    def _compile_expression_list(self):
        """Compiles a possibly empty comma-separated list of expressions"""
        self._xmltranslator.open_section("expressionList")
        exp_count = 0
        while is_term(self.tokens[self._cur_ind]):
            exp_count += 1
            self._compile_expression()
            if self.tokens[self._cur_ind]["value"] == ",":
                self._process_token()
        self._xmltranslator.close_section("expressionList")
        return exp_count

    def _compile_subroutine_call(self):
        """"Compiles a call like
        ClassName.subName(exprList) or
        subName(exprList) or
        varname.subname(exprlist)
        """

        nme = self.tokens[self._cur_ind]["value"]
        self._process_token("type", "identifier")

        if self.tokens[self._cur_ind]["value"] == "(":
            self._process_token()
            class_name = self._vmtranslator.class_name
            sub_name = nme
            self._vmtranslator.push_statement("pointer", 0)
            add_arg = 1
        else:
            self._process_token("value", ".")
            sub_name = self.tokens[self._cur_ind]["value"]
            self._process_token("type", "identifier")
            self._process_token("value", "(")
            class_name = self._symbol_table.resolve_symbol(nme)
            if class_name == nme:
                add_arg = 0
            else:
                seg = SEGMENT[self._symbol_table.kind_of(nme)]
                ind = self._symbol_table.index_of(nme)
                self._vmtranslator.push_statement(seg, ind)
                add_arg = 1

        call_name = class_name + "." + sub_name

        exp_n = self._compile_expression_list() + add_arg
        self._process_token("value", ")")

        # Write the VM code
        self._vmtranslator.call(call_name, exp_n)

    def _push_variable(self, var_name=None):
        """Pushes the variable identiefied onto the stack"""
        advance = False
        if var_name is None:
            var_name = self.tokens[self._cur_ind]["value"]
            advance = True
        seg = SEGMENT[self._symbol_table.kind_of(var_name)]
        var_ind = self._symbol_table.index_of(var_name)
        self._vmtranslator.push_statement(seg, var_ind)
        if advance:
            self._process_token()
