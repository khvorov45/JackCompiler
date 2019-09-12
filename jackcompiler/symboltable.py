"""SymbolTable class"""

def identifier(iden_name, iden_type, iden_kind, iden_index):
    """Entry in a symbol table"""
    entry = {
        "name": iden_name, "type": iden_type, "kind": iden_kind,
        "index": iden_index
    }
    return entry

class SymbolTable:
    """Symbol table"""
    def __init__(self):
        self._class_scope = []
        self._class_static_ind = 0
        self._class_field_ind = 0
        self._subroutine_scope = []
        self._subroutine_arg_ind = 0
        self._subroutine_var_ind = 0

    def start_subroutine(self):
        """Starts a new subroutine (resets subroutine scope)"""
        self._subroutine_scope = []
        self._subroutine_arg_ind = 0
        self._subroutine_var_ind = 0

    def define(self, iden_name, iden_type, iden_kind):
        """Defines a new identifier of a given name, type and kind.
        Assigns it a running index.
        """
        if iden_kind == "static":
            iden = identifier(
                iden_name, iden_type, iden_kind, self._class_static_ind
            )
            self._class_scope.append(iden)
            self._class_static_ind += 1
        elif iden_kind == "field":
            iden = identifier(
                iden_name, iden_type, iden_kind, self._class_field_ind
            )
            self._class_scope.append(iden)
            self._class_field_ind += 1
        elif iden_kind == "arg":
            iden = identifier(
                iden_name, iden_type, iden_kind, self._subroutine_arg_ind
            )
            self._subroutine_scope.append(iden)
            self._subroutine_arg_ind += 1
        elif iden_kind == "var":
            iden = identifier(
                iden_name, iden_type, iden_kind, self._subroutine_var_ind
            )
            self._subroutine_scope.append(iden)
            self._subroutine_var_ind += 1
        else:
            raise Exception("unexpected identifier kind: " + iden.kind)

    def var_count(self, iden_kind):
        """Returns the number of variables of the given kind
        already defined in the current scope.
        """
        if iden_kind in ["static", "field"]:
            dic = self._class_scope
        elif iden_kind in ["arg", "var"]:
            dic = self._subroutine_scope
        else:
            raise Exception("unexpected identifier kind: " + iden_kind)
        cnt = 0
        for ent in dic:
            if ent["kind"] == iden_kind:
                cnt += 1
        return cnt

    def kind_of(self, iden_name):
        """Returns the kind of the named identifier in the current scope"""
        return self._prop_of(iden_name, "kind")

    def type_of(self, iden_name):
        """Returns the type of the named identifier in the current scope"""
        return self._prop_of(iden_name, "type")

    def index_of(self, iden_name):
        """Returns the index of the named identifier in the current scope"""
        return self._prop_of(iden_name, "index")

    def _prop_of(self, iden_name, prop):
        """Generic function for *_of"""
        for iden in self._subroutine_scope:
            if iden["name"] == iden_name:
                return iden[prop]
        for iden in self._class_scope:
            if iden["name"] == iden_name:
                return iden[prop]
        return "NONE"

    def print(self, cla=True, sub=True):
        """Prints the table"""
        template = "{:10} | {:10} | {:10} | {:3}"
        top_row = template.format("Name", "Type", "Kind", "#")
        print(top_row)
        if cla:
            self._print_scope("class", template)
        if sub:
            self._print_scope("subroutine", template)

    def _print_scope(self, scope, template):
        """Prints a scope"""
        if scope == "class":
            dic = self._class_scope
        elif scope == "subroutine":
            dic = self._subroutine_scope
        else:
            raise ValueError("scope should be 'class' or 'subroutine'")
        for iden in dic:
            row = template.format(
                iden["name"], iden["type"], iden["kind"], iden["index"]
            )
            print(row)
