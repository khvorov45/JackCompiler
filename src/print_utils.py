#--------------------------------------------------------------------------------
# Printing utility functions
#--------------------------------------------------------------------------------

def print_dotted_line(width = 115):
    """ Prints a dotted line of the specified width """
    print("-"*width)

def print_padded(string):
    """ Prints start message """
    print_dotted_line()
    print(string)
    print_dotted_line()