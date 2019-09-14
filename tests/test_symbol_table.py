#pylint: disable=missing-docstring

from jackcompiler.symboltable import SymbolTable

def test_symbol_table():
    """Tests symbol table"""
    symt = SymbolTable()
    symt.subroutine_type = "function"
    symt.define("var1stat", "int", "static")
    symt.define("var2stat", "int", "static")
    symt.define("var3stat", "int", "static")
    symt.define("var4stat", "int", "static")
    symt.define("var1f", "int", "field")
    symt.define("var2f", "int", "field")
    symt.define("var3f", "int", "field")
    symt.define("var1arg", "int", "arg")
    symt.define("var2arg", "int", "arg")
    symt.define("var1v", "int", "var")
    symt.print()
    assert symt.var_count("static") == 4
    assert symt.var_count("field") == 3
    assert symt.var_count("arg") == 2
    assert symt.var_count("var") == 1
    assert symt.kind_of("var1stat") == "static"
    assert symt.kind_of("var1f") == "field"
    assert symt.kind_of("var1arg") == "arg"
    assert symt.kind_of("var1v") == "var"
    assert symt.type_of("var1v") == "int"
    assert symt.index_of("var1v") == 0
