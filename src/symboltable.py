"""SymbolTable class"""

from .utilities import count_kind

class Identifier:
    """Identifier, entry in a symbol table"""
    # pylint: disable=too-few-public-methods
    def __init__(self, iden_name, iden_type, iden_kind):
        self.name = iden_name
        self.type = iden_type
        self.kind = iden_kind

class SymbolTable:
    """Symbol table"""
    def __init__(self):
        self.class_scope = {}
        self.class_static_ind = 0
        self.class_field_ind = 0
        self.subroutine_scope = {}
        self.subroutine_arg_ind = 0
        self.subroutine_var_ind = 0

    def start_subroutine(self):
        """Starts a new subroutine (resets subroutine scope)"""
        self.subroutine_scope = {}
        self.subroutine_arg_ind = 0
        self.subroutine_var_ind = 0

    def define(self, iden_name, iden_type, iden_kind):
        """Defines a new identifier of a given name, type and kind.
        Assigns it a running index.
        """
        iden = Identifier(iden_name, iden_type, iden_kind)
        if iden.kind == "static":
            self.class_scope.update({self.class_static_ind: iden})
            self.class_static_ind += 1
        elif iden.kind == "field":
            self.class_scope.update({self.class_field_ind: iden})
            self.class_field_ind += 1
        elif iden.kind == "arg":
            self.subroutine_scope.update({self.subroutine_arg_ind: iden})
            self.subroutine_arg_ind += 1
        elif iden.kind == "var":
            self.subroutine_scope.update({self.subroutine_var_ind: iden})
            self.subroutine_var_ind += 1
        else:
            raise Exception("unexpected identifier kind: " + iden.kind)

    def var_count(self, iden_kind):
        """Returns the number of variables of the given kind
        already defined in the current scope.
        """
        if iden_kind in ["static", "field"]:
            return count_kind(self.class_scope, iden_kind)
        if iden_kind in ["arg", "var"]:
            return count_kind(self.subroutine_scope, iden_kind)
        raise Exception("unexpected identifier kind: " + iden_kind)

    def kind_of(self, iden_name):
        """Returns the kind of the named identifier in the current scope"""
        for iden in self.subroutine_scope.values():
            if iden.name == iden_name:
                return iden.kind
        for iden in self.class_scope.values():
            if iden.name == iden_name:
                return iden.kind
        return "NONE"

    def type_of(self, iden_name):
        """Returns the type of the named identifier in the current scope"""
        for iden in self.subroutine_scope.values():
            if iden.name == iden_name:
                return iden.type
        for iden in self.class_scope.values():
            if iden.name == iden_name:
                return iden.type
        return "NONE"

    def index_of(self, iden_name):
        """Returns the index of the named identifier in the current scope"""
        for ind, iden in self.subroutine_scope.items():
            if iden.name == iden_name:
                return ind
        for ind, iden in self.class_scope.items():
            if iden.name == iden_name:
                return ind
        return "NONE"

    def print(self, cla=True, sub=True):
        """Prints the table"""
        template = "{:10} | {:10} | {:10} | {:3}"
        top_row = template.format("Name", "Type", "Kind", "#")
        print(top_row)
        if cla:
            for ind, iden in self.class_scope.items():
                row = template.format(iden.name, iden.type, iden.kind, ind)
                print(row)
        if sub:
            for ind, iden in self.subroutine_scope.items():
                row = template.format(iden.name, iden.type, iden.kind, ind)
                print(row)
