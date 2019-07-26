"""Parsing command line input"""

class CmdParser:
    """Parses command line input. Expects it unmodified.

    Arguments:
        system_arguments: a list of strings. Expected to be unmodified
            command line input
        opt_dic: a dictionary of options.
            indicator : option information returned by build_option_entry
    """
    def __init__(self, system_arguments, opt_dic):
        self._unprocessed = system_arguments[1:] # Ignore the first
        self._opt_dic = opt_dic
        self._opts = {}
        self._read_opts()

    def get_opts(self):
        """Returns the parsed options"""
        return self._opts

    def get_nonopts(self):
        """Returns what's left after parsing options"""
        return self._unprocessed

    def _read_opts(self):
        """Returns a dictionary with all the optional arguments"""

        opt_inds = self._opt_dic
        opts = {}

        # See what arguments have been provided
        new_unprocessed = []
        skip_next = False
        for i, arg in enumerate(self._unprocessed):
            if skip_next:
                skip_next = False
                continue
            if arg in opt_inds.keys():
                if not opt_inds[arg]["fun"]: # Assume a boolean option
                    opts[opt_inds[arg]["name"]] = True
                    continue
                skip_next = True
                candidate = opt_inds[arg]["fun"](self._unprocessed[i + 1])
                if candidate is not None:
                    opts[opt_inds[arg]["name"]] = candidate
            else:
                new_unprocessed.append(arg)

        # Update the values
        self._unprocessed = new_unprocessed
        self._opts = opts

def build_option_entry(name, fun=False):
    """Builds a dictionary entry for the options indicator.
    Each indicator will correspond to a proper option name and a funciton that
    will recieve the next item in the command line argument list.
    If fun=False (the default), the option will be assumed to be boolean and
    if present, the value of the option in the parsed option dicitonary will
    be set to True.
    """
    return {"name": name, "fun": fun}
