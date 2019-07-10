"""CompilationEngine class.
Does not have a huge amount of errer checking, will likely only work with
correctly written .jack classes.
"""

from .utilities import UnexpectedToken, build_terminal
from .glossary import is_term, is_op, KEYWORD_CONSTANTS, UNARY_OP
from .symboltable import SymbolTable

class CompilationEngine():
    """Controls compilation

    Arguments:
        self.toks -- list of tokens (TokenInfo class).
            Should represent one class.
        out_file_path -- path to the file to write translation to
    """
    def __init__(self, toks, out_file_path):
        self.toks = toks
        self.out_file_path = out_file_path
        self.cur_ind = 0
        self.tab_char = "  "
        self.tab_level = 1
        self.result = ""
        self.symbol_table = SymbolTable()
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
        self.create_xml_terminal()

        # Opening '{'
        self.create_xml_terminal()

        # Class variables
        while self.toks[self.cur_ind].token in ["static", "field"]:
            self.compile_class_var_dec()

        # Print the symbol table
        self.symbol_table.print(sub=False)

        # Subroutines
        while self.toks[self.cur_ind].token in \
            ["constructor", "function", "method"]:
            self.compile_subroutine()

        # Closing '}'
        self.create_xml_terminal()

        # Finish up the class
        self.result += "</class>\n"

        # Write to translation file
        out_file = open(self.out_file_path, "w+")
        out_file.write(self.result)
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

        # Identifier
        self.create_xml_terminal(increment=False)
        nme = self.toks[self.cur_ind].token
        self.cur_ind += 1

        self.symbol_table.define(nme, tpe, knd)

        while self.toks[self.cur_ind].token == ",":
            self.create_xml_terminal() # ,

            # Add another variable to the symbol table
            self.create_xml_terminal(increment=False)
            nme = self.toks[self.cur_ind].token
            self.cur_ind += 1
            self.symbol_table.define(nme, tpe, knd)

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

        # Subroutine type
        if self.toks[self.cur_ind].token not in \
            ["constructor", "function", "method"]:
            raise UnexpectedToken(self.toks[self.cur_ind])
        self.create_xml_terminal()

        # Next is the return type
        self.create_xml_terminal()

        # Then is the name, not placing this in the symbol table.
        self.create_xml_terminal()

        # Then is the parameter list. 
        # All arguments should be in the symbol table.
        self.compile_parameter_list()

        # Then is the subroutine body
        self.result += self.tab_level * self.tab_char + "<subroutineBody>\n"
        self.tab_level += 1

        # First is the opening
        self.create_xml_terminal()

        # Then all the variables. All of these will go into the symbol table.
        while self.toks[self.cur_ind].token == "var":
            self.compile_var_dec()

        # Then all the statements
        self.compile_statements()

        # Closing '}'
        self.create_xml_terminal()

        # Print the symbol table
        self.symbol_table.print(cla=False)

        # Finish the subroutine
        self.tab_level -= 1
        self.result += self.tab_level * self.tab_char + "</subroutineBody>\n"
        self.tab_level -= 1
        self.result += self.tab_level * self.tab_char + "</subroutineDec>\n"

    def compile_parameter_list(self):
        """Compiles a parameter list (possibly empty)"""

        # First is the opening
        self.create_xml_terminal()

        # Then come the parameters
        self.result += self.tab_level * self.tab_char + "<parameterList>\n"
        self.tab_level += 1
        while self.toks[self.cur_ind].token != ")":
            self.create_xml_terminal()
        self.tab_level -= 1
        self.result += self.tab_level * self.tab_char + "</parameterList>\n"

        # Finishes with closing the list
        self.create_xml_terminal()

    def compile_var_dec(self):
        """Compiles a variable declaration.
        Should look like this: var 'type' 'identifier', 'identifier', ... ;
        """

        # Open up
        self.result += self.tab_level * self.tab_char + "<varDec>\n"
        self.tab_level += 1

        self.create_xml_terminal()
        self.create_xml_terminal()
        self.create_xml_terminal()

        while self.toks[self.cur_ind].token == ",":
            self.create_xml_terminal()
            self.create_xml_terminal()

        self.create_xml_terminal()

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

        while self.toks[self.cur_ind].token != "(":
            self.create_xml_terminal()
        self.create_xml_terminal()
        self.compile_expression_list()
        self.create_xml_terminal()
        self.create_xml_terminal()

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

        self.create_xml_terminal()
        self.create_xml_terminal()

        if self.toks[self.cur_ind].token == "[":
            self.create_xml_terminal()
            while is_term(self.toks[self.cur_ind]):
                self.compile_expression()
            self.create_xml_terminal()

        self.create_xml_terminal()

        while is_term(self.toks[self.cur_ind]):
            self.compile_expression()

        self.create_xml_terminal()

        # Close down
        self.tab_level -= 1
        self.result += self.tab_level * self.tab_char + "</letStatement>\n"


    def compile_while(self):
        """Compile a while statement
        while (expr) {statements}
        """

        # Open up
        self.result += self.tab_level * self.tab_char + "<whileStatement>\n"
        self.tab_level += 1

        self.create_xml_terminal()
        self.create_xml_terminal()

        while is_term(self.toks[self.cur_ind]):
            self.compile_expression()

        self.create_xml_terminal()
        self.create_xml_terminal()

        self.compile_statements()

        self.create_xml_terminal()

        # Close down
        self.tab_level -= 1
        self.result += self.tab_level * self.tab_char + "</whileStatement>\n"

    def compile_return(self):
        """Compiles a return statement
        return expression? ;
        """

        # Open up
        self.result += self.tab_level * self.tab_char + "<returnStatement>\n"
        self.tab_level += 1

        self.create_xml_terminal()

        while is_term(self.toks[self.cur_ind]):
            self.compile_expression()

        self.create_xml_terminal()

        # Close down
        self.tab_level -= 1
        self.result += self.tab_level * self.tab_char + "</returnStatement>\n"

    def compile_if(self):
        """Compiles an if statement, possibly trailing else
        if (expr) {statements} else {statements}
        """

        # Open up
        self.result += self.tab_level * self.tab_char + "<ifStatement>\n"
        self.tab_level += 1

        self.create_xml_terminal()
        self.create_xml_terminal()

        while is_term(self.toks[self.cur_ind]):
            self.compile_expression()

        self.create_xml_terminal()
        self.create_xml_terminal()

        self.compile_statements()

        self.create_xml_terminal()

        if self.toks[self.cur_ind].token == "else":
            self.create_xml_terminal()
            self.create_xml_terminal()

            self.compile_statements()

            self.create_xml_terminal()

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
            self.create_xml_terminal()
            self.compile_term()

        # Close down
        self.tab_level -= 1
        self.result += self.tab_level * self.tab_char + "</expression>\n"

    def compile_term(self):
        """Compiles a term"""

        # Open up
        self.result += self.tab_level * self.tab_char + "<term>\n"
        self.tab_level += 1

        if self.toks[self.cur_ind].toktype in \
            ["integerConstant", "stringConstant"]:
            self.create_xml_terminal()
        elif self.toks[self.cur_ind].token in KEYWORD_CONSTANTS:
            self.create_xml_terminal()
        elif self.toks[self.cur_ind].token == "(":
            self.create_xml_terminal()
            while is_term(self.toks[self.cur_ind]):
                self.compile_expression()
            self.create_xml_terminal()
        elif self.toks[self.cur_ind].token in UNARY_OP:
            self.create_xml_terminal()
            self.compile_term()
        else:
            if self.toks[self.cur_ind].toktype != "identifier":
                raise UnexpectedToken(self.toks[self.cur_ind])
            if self.toks[self.cur_ind + 1].token == "[":
                self.create_xml_terminal()
                self.create_xml_terminal()
                while is_term(self.toks[self.cur_ind]):
                    self.compile_expression()
                self.create_xml_terminal()
            elif self.toks[self.cur_ind + 1].token == "(":
                self.create_xml_terminal()
                self.create_xml_terminal()
                self.compile_expression_list()
                self.create_xml_terminal()
            elif self.toks[self.cur_ind + 1].token == ".":
                self.create_xml_terminal()
                self.create_xml_terminal()
                self.create_xml_terminal()
                self.create_xml_terminal()
                self.compile_expression_list()
                self.create_xml_terminal()
            else:
                self.create_xml_terminal()

        # Close down
        self.tab_level -= 1
        self.result += self.tab_level * self.tab_char + "</term>\n"


    def compile_expression_list(self):
        """Compiles a possibly empty comma-separated list of expressions"""

        # Open up
        self.result += self.tab_level * self.tab_char + "<expressionList>\n"
        self.tab_level += 1

        while is_term(self.toks[self.cur_ind]):
            self.compile_expression()
            if self.toks[self.cur_ind].token == ",":
                self.create_xml_terminal()

        # Close down
        self.tab_level -= 1
        self.result += self.tab_level * self.tab_char + "</expressionList>\n"

    def create_xml_terminal(self, increment=True):
        """Creates a string for xml writing"""
        self.result += self.tab_level * self.tab_char + \
            build_terminal(self.toks[self.cur_ind])
        if increment:
            self.cur_ind += 1
