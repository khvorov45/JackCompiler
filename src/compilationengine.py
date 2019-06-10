#--------------------------------------------------------------------------------
# CompilationEngine class
#--------------------------------------------------------------------------------

class CompilationEngine():
    def __init__(self, tokens, out_path):
        self.out_file = open(out_path, "w")
        self.tokens = tokens
        self.current_index = -1
    
    def compile_class(self):
        self.out_file.write("<class>\n")
        self._go_to_next()
        self.out_file.write("<keyword> "+ self.tokens[self.current_index].keyword +" </keyword>\n")
        self.out_file.write("something here i guess\n")
        
        self.out_file.write("</class>")
    
    def _go_to_next(self):
        self.current_index += 1
    
    def _go_back(self):
        self.current_index -= 1