"""CompilationEngine class"""

from .utilities import UnexpectedToken, build_terminal

class CompilationEngine():
    """Controls compilation

    Arguments:
        self.toks -- list of tokens (TokenInfo class). Should represent one class.
        out_file_path -- path to the file to write translation to
    """
    def __init__(self, toks, out_file_path):
        self.toks = toks
        self.out_file_path = out_file_path
        self.cur_ind = 0
        self.tab_char = "  "
        self.tab_level = 1
        self.result = ""
        self.compile_class()

    def compile_class(self):
        """Compiles the entire class"""

        # First token is 'class'
        if self.toks[self.cur_ind].token != "class":
            raise UnexpectedToken(self.toks[self.cur_ind])
        self.result += "<class>\n"
        self.create_xml_terminal()

        # Second token is the class name
        if self.toks[self.cur_ind].toktype != "identifier":
            raise UnexpectedToken(self.toks[self.cur_ind])
        self.create_xml_terminal()

        # Then is the class body
        self.compile_subroutine()

        # Finish up the class
        self.result += "</class>\n"

        # Write to translation file
        out_file = open(self.out_file_path, "w+")
        out_file.write(self.result)
        out_file.close()

    def compile_subroutine(self):
        """Compiles a subroutine"""

        # First is the opening
        self.create_xml_terminal()

        # Then is the subroutine type
        if self.toks[self.cur_ind].token not in \
            ["constructor", "function", "method"]:
            raise UnexpectedToken(self.toks[self.cur_ind])
        self.result += self.tab_level * self.tab_char + "<subroutineDec>\n"
        self.tab_level += 1
        self.create_xml_terminal()

        # Next is the return type
        self.create_xml_terminal()

        # Then is the name
        self.create_xml_terminal()

        # Then is the parameter list
        self.compile_parameter_list()

        # Then is the subroutine body
        self.result += self.tab_level * self.tab_char + "<subroutineBody>\n"
        self.tab_level += 1

        # First is the opening
        self.create_xml_terminal()

        # Then is the rest of the subroutine body
        while True:
            if self.toks[self.cur_ind].token == "var":
                self.compile_var_dec()
            else:
                break

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
        while True:
            if self.toks[self.cur_ind].token == ")":
                break
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

        while True:
            self.create_xml_terminal()
            if self.toks[self.cur_ind].token != ",":
                break
            self.create_xml_terminal()

        self.create_xml_terminal()

        # Close down
        self.tab_level -= 1
        self.result += self.tab_level * self.tab_char + "</varDec>\n"

    def compile_statements(self):
        """Compiles a series of statements not including the enclosing {}"""

    def compile_do(self):
        """Compiles a do statement"""

    def compile_let(self):
        """Compiles a let statement"""

    def compile_while(self):
        """Compile a while statement"""

    def compile_return(self):
        """Compiles a return statement"""

    def compile_if(self):
        """Compiles an if statement, possibly trailing else"""

    def compile_expression(self):
        """Compiles an expresssion"""

    def compile_term(self):
        """Compiles a term"""

    def compile_expression_list(self):
        """Compiles a possibly empty comma-separated list of expressions"""

    def create_xml_terminal(self, increment=True):
        """Creates a string for xml writing"""
        self.result += self.tab_level * self.tab_char + \
            build_terminal(self.toks[self.cur_ind])
        if increment:
            self.cur_ind += 1
