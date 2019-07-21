"""SymbolTable class"""

from .utilities import count_kind

class Identifier:
    """Identifier, entry in a symbol table"""
    # pylint: disable=too-few-public-methods
    def __init__(self, iden_name, iden_type, iden_kind, iden_index):
        self.name = iden_name
        self.type = iden_type
        self.kind = iden_kind
        self.index = iden_index

class SymbolTable:
    """Symbol table"""
    def __init__(self):
        self.class_scope = []
        self.class_static_ind = 0
        self.class_field_ind = 0
        self.subroutine_scope = []
        self.subroutine_arg_ind = 0
        self.subroutine_var_ind = 0

    def start_subroutine(self):
        """Starts a new subroutine (resets subroutine scope)"""
        self.subroutine_scope = []
        self.subroutine_arg_ind = 0
        self.subroutine_var_ind = 0

    def define(self, iden_name, iden_type, iden_kind):
        """Defines a new identifier of a given name, type and kind.
        Assigns it a running index.
        """

        if iden_kind == "static":
            iden = Identifier(
                iden_name, iden_type, iden_kind, self.class_static_ind
            )
            self.class_scope.append(iden)
            self.class_static_ind += 1
        elif iden_kind == "field":
            iden = Identifier(
                iden_name, iden_type, iden_kind, self.class_field_ind
            )
            self.class_scope.append(iden)
            self.class_field_ind += 1
        elif iden_kind == "arg":
            iden = Identifier(
                iden_name, iden_type, iden_kind, self.subroutine_arg_ind
            )
            self.subroutine_scope.append(iden)
            self.subroutine_arg_ind += 1
        elif iden_kind == "var":
            iden = Identifier(
                iden_name, iden_type, iden_kind, self.subroutine_var_ind
            )
            self.subroutine_scope.append(iden)
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
        for iden in self.subroutine_scope:
            if iden.name == iden_name:
                return iden.kind
        for iden in self.class_scope:
            if iden.name == iden_name:
                return iden.kind
        return "NONE"

    def type_of(self, iden_name):
        """Returns the type of the named identifier in the current scope"""
        for iden in self.subroutine_scope:
            if iden.name == iden_name:
                return iden.type
        for iden in self.class_scope:
            if iden.name == iden_name:
                return iden.type
        return "NONE"

    def index_of(self, iden_name):
        """Returns the index of the named identifier in the current scope"""
        for iden in self.subroutine_scope:
            if iden.name == iden_name:
                return iden.index
        for iden in self.class_scope:
            if iden.name == iden_name:
                return iden.index
        return "NONE"

    def print(self, cla=True, sub=True):
        """Prints the table"""
        template = "{:10} | {:10} | {:10} | {:3}"
        top_row = template.format("Name", "Type", "Kind", "#")
        print(top_row)
        if cla:
            for iden in self.class_scope:
                row = template.format(
                    iden.name, iden.type, iden.kind, iden.index
                )
                print(row)
        if sub:
            for iden in self.subroutine_scope:
                row = template.format(
                    iden.name, iden.type, iden.kind, iden.index
                )
                print(row)
