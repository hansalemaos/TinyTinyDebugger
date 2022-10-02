import os
import re as regex
import sys
from random import randrange
from PrettyColorPrinter import pdp
from cprinter import TC
from decorator import decorator
import pandas as pd
import inspect
from time import time as now, strftime
from input_timeout import InputTimeout


detailed_debugger_enabled = True
detailed_debugger_write_log_file = True
detailed_debugger_log_folder = os.path.join(os.getcwd(), "SMALLDEBUGGERLOGS")
detailed_debugger_pause_for_n_seconds_when_exception = 0
detailed_debugger_continue_on_exceptions = True
detailed_debugger_print_write_exceptions_only = False


def c_yellow(text, end="\n"):
    print(TC(str(text)).fg_yellow, end=end)


def c_red(text, end="\n"):
    print(TC(str(text)).fg_red, end=end)


def c_pink(text, end="\n"):
    print(TC(str(text)).fg_pink, end=end)


def c_orange(text, end="\n"):
    print(TC(str(text)).fg_orange, end=end)


def c_lightred(text, end="\n"):
    print(TC(str(text)).fg_lightred, end=end)


def c_lightgreen(text, end="\n"):
    print(TC(str(text)).fg_lightgreen, end=end)


def c_lightcyan(text, end="\n"):
    print(TC(str(text)).fg_lightcyan, end=end)


def c_lightblue(text, end="\n"):
    print(TC(str(text)).fg_lightblue, end=end)


def c_red_bg_black(text, end="\n"):
    print(TC(str(text)).fg_red.bg_black, end=end)


def c_pink_bg_black(text, end="\n"):
    print(TC(str(text)).fg_pink.bg_black, end=end)


def c_orange_bg_black(text, end="\n"):
    print(TC(str(text)).fg_orange.bg_black, end=end)


def c_lightred_bg_black(text, end="\n"):
    print(TC(str(text)).fg_lightred.bg_black, end=end)


def c_lightgreen_bg_black(text, end="\n"):
    print(TC(str(text)).fg_lightgreen.bg_black, end=end)


def c_lightcyan_bg_black(text, end="\n"):
    print(TC(str(text)).fg_lightcyan.bg_black, end=end)


def c_lightblue_bg_black(text, end="\n"):
    print(TC(str(text)).fg_lightblue.bg_black, end=end)


def c_lightgrey(text, end="\n"):
    print(TC(str(text)).bg_black.fg_darkgrey.bold.underline, end=end)


def get_size_of_longest_element_in_list(liste):
    dinges = [(len(str(x)), str(x)) for x in liste]
    dinges.sort()
    return dinges[-1][0]


@decorator
def docs(f, *args, **kwargs):

    print((f"Documentation for {_get_scope(f, args)}"))
    print((inspect.getdoc(f)))

    return f(*args, **kwargs)


@decorator
def time_(f, *args, **kwargs):

    _t0 = now()
    _r = f(*args, **kwargs)
    _t1 = now()

    total_time = _t1 - _t0
    print(c_orange(f"EXECUTION TIME {f.__name__} - {total_time}\n-------------"))

    return _r


@decorator
def trace(f, *args, **kwargs):
    _scope = _get_scope(f, args)
    c_lightblue(f"CALLING FUNCTION: {_scope} / ARGS: {args} / KWARGS: {kwargs}\n")

    return f(*args, **kwargs)


def _get_scope(f, args):

    _scope = inspect.getmodule(f).__name__
    try:
        if f.__name__ in dir(args[0].__class__):
            _scope += "." + args[0].__class__.__name__
            _scope += "." + f.__name__
        else:
            _scope += "." + f.__name__
    except IndexError:
        _scope += "." + f.__name__

    return _scope


class SwitchedDecorator:
    def __init__(self, enabled_func):
        self._enabled = False
        self._enabled_func = enabled_func
        self._write_log_file = False
        self._log_folder = os.path.join(os.getcwd(), "SMALLDEBUGGERLOGS")

        self._pause_for_n_seconds_when_exception = 5
        self._continue_on_exceptions = True
        self._print_write_exceptions_only = False

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, new_value):
        if not isinstance(new_value, bool):
            raise ValueError("enabled can only be set to a boolean value")
        self._enabled = new_value

    def __call__(self, target):
        if self._enabled:
            return self._enabled_func(target)
        return target

    @property
    def write_log_file(self):
        return self._write_log_file

    @write_log_file.setter
    def write_log_file(self, new_value):
        global detailed_debugger_write_log_file
        if not isinstance(new_value, bool):
            raise ValueError("enabled can only be set to a boolean value")
        self._write_log_file = new_value
        detailed_debugger_write_log_file = self._write_log_file

    @property
    def log_folder(self):
        if not os.path.exists(self._log_folder):
            os.makedirs(self._log_folder)
        return self._log_folder

    @log_folder.setter
    def log_folder(self, new_value):
        global detailed_debugger_log_folder
        if not isinstance(new_value, str):
            raise ValueError("log_folder can only be set to a str value")
        self._log_folder = new_value
        detailed_debugger_log_folder = self._log_folder
        if not os.path.exists(self._log_folder):
            os.makedirs(self._log_folder)

    @property
    def pause_for_n_seconds_when_exception(self):
        return self._pause_for_n_seconds_when_exception

    @pause_for_n_seconds_when_exception.setter
    def pause_for_n_seconds_when_exception(self, new_value):
        global detailed_debugger_pause_for_n_seconds_when_exception
        if not isinstance(new_value, (int, float)):
            raise ValueError(
                "pause_for_n_seconds_when_exception can only be set to int/float value"
            )
        self._pause_for_n_seconds_when_exception = new_value
        detailed_debugger_pause_for_n_seconds_when_exception = (
            self._pause_for_n_seconds_when_exception
        )

    @property
    def continue_on_exceptions(self):
        return self._continue_on_exceptions

    @continue_on_exceptions.setter
    def continue_on_exceptions(self, new_value):
        global detailed_debugger_continue_on_exceptions
        if not isinstance(new_value, bool):
            raise ValueError(
                "continue_on_exceptions can only be set to a boolean value"
            )
        self._continue_on_exceptions = new_value
        detailed_debugger_continue_on_exceptions = self._continue_on_exceptions

    @property
    def print_write_exceptions_only(self):
        return self._print_write_exceptions_only

    @print_write_exceptions_only.setter
    def print_write_exceptions_only(self, new_value):
        global detailed_debugger_print_write_exceptions_only
        if not isinstance(new_value, bool):
            raise ValueError("print_exceptions only can only be set to a boolean value")
        self._print_write_exceptions_only = new_value
        detailed_debugger_print_write_exceptions_only = (
            self._print_write_exceptions_only
        )


def regex_substitute_os_sep(path):
    ossep = regex.escape(os.sep)
    return regex.sub(f"[\\/{ossep}]+", ossep, path)


class SmallDebugger:
    def __init__(self, name):
        self.name = name
        self.filename = __file__
        self.filename = regex_substitute_os_sep(self.filename)
        self.allezeilen = self.read_py_file(self.filename)

    def read_py_file(self, filename):

        try:
            with open(filename, mode="r", encoding="utf-8") as f:
                allezeilen = [_.rstrip() for _ in f.read().splitlines()]

        except Exception:
            pass
        return allezeilen

    def __enter__(self):
        (c_yellow(f"STARTING: {self.name}\n"))
        sys.settrace(self.trace_calls)

    def __exit__(self, *args, **kwargs):
        sys.settrace(None)

    def trace_calls(self, frame, event, arg):
        if event != "call":
            return
        elif frame.f_code.co_name != self.name:
            return
        return self.trace_lines

    def trace_lines(self, frame, event, arg):
        global detailed_debugger_print_write_exceptions_only
        global detailed_debugger_write_log_file
        global detailed_debugger_log_folder
        co = frame.f_code
        func_name = co.co_name
        line_no = frame.f_lineno
        filename = co.co_filename
        local_vars = frame.f_locals
        if event == "exception" or (detailed_debugger_print_write_exceptions_only is False):
            if filename != self.filename:
                self.filename = filename
                self.allezeilen = self.read_py_file(self.filename)
            localv = pd.DataFrame(pd.Series(local_vars))
            localv.columns = ["local_vars_value"]
            allezeilen = [str(_).strip() for _ in self.allezeilen]
            ganzezeilen = allezeilen[line_no - 1]
            c_lightgrey(f"LOCAL VARIABLES BEFORE THE EXECUTION OF:\t", end="\n")

            c_lightcyan_bg_black(f"{ganzezeilen}")
            pdp(localv)
            allefunkdru = ["FUNCTION", "EVENT", "LINE", "FILE"]
            allefunkdru = [str(f"{x}: ").ljust(12) for x in allefunkdru]
            allinfos = [func_name, event, f"{line_no}\t>>>\t\t{ganzezeilen}", filename]
            allinfosfordebug = allinfos.copy()
            laengste = get_size_of_longest_element_in_list(allinfos) + 3
            allinfos = [str(f"{x}").ljust(laengste) for x in allinfos]
            for b1, b2 in zip(allefunkdru, allinfos):
                if event == "line":
                    if b1.startswith("LINE"):
                        c_lightgreen_bg_black(f"{b1} {b2}")
                    else:
                        c_lightgreen(f"{b1} {b2}")
                elif event == "return":
                    if b1.startswith("LINE"):
                        c_orange_bg_black(f"{b1} {b2}")
                    else:
                        (c_yellow(f"{b1} {b2}"))
                elif event == "exception":
                    if b1.startswith("LINE"):
                        c_red_bg_black(f"{b1} {b2}")
                    else:
                        (c_lightred(f"{b1} {b2}"))
                else:
                    pass

            if detailed_debugger_write_log_file:
                no1 = pd.DataFrame(
                    allinfosfordebug,
                    index=["FUNCTION", "EVENT", "LINE", "FILE"],
                    columns=["log"],
                )
                dfz = pd.concat([no1, localv])
                filename_ = ""
                forbiddenfilepath = ["\\", "/", ":", "?", "*", "<", '"', ">", "|"]
                for debuginfo in allinfosfordebug[:3]:
                    for symbol in forbiddenfilepath:
                        debuginfo = (
                            str(debuginfo)
                            .strip()
                            .replace("\n", "_")
                            .replace("\r", "_")
                            .replace(symbol, "_")
                            + "---"
                        )
                    filename_ = filename_ + "---" + debuginfo
                filename_ = regex.sub(r"[\s.=]+", "_", filename_)
                filename_ = regex.sub("_+", "_", filename_)
                filename_ = filename_.strip().strip("_ ")
                filename_ = regex.sub("-+", "---", filename_)
                detailed_debugger_log_folder_file = os.path.join(
                    detailed_debugger_log_folder,
                    f'{get_timestamp()}log---{filename_.strip(" _-")}{str(randrange(1,1000000000)).zfill(10)}',
                )[:250]
                detailed_debugger_log_folder_file = (
                    detailed_debugger_log_folder_file + ".xlsx"
                )

                dfz.to_excel(detailed_debugger_log_folder_file)
                c_lightgreen(f"Log written: {str(detailed_debugger_log_folder_file)}")


def get_timestamp():
    return strftime("%Y_%m_%d_%H_%M_%S")


@decorator
def debug_decorator(func, *args, **kwargs):
    with SmallDebugger(func.__name__):
        return_value = func(*args, **kwargs)
    return return_value


@decorator
def ignore_exceptions(func, *args, **kwargs):
    return_value = None
    if detailed_debugger_continue_on_exceptions is False:
        return func(*args, **kwargs)

    try:
        return_value = func(*args, **kwargs)
    except Exception as Fehler:
        print(Fehler)
        if detailed_debugger_pause_for_n_seconds_when_exception > 0:
            i = InputTimeout(
                timeout=detailed_debugger_pause_for_n_seconds_when_exception,
                input_message=" THERE WAS AN EXCEPTION - PLEASE PRESS ENTER OR ESC TO CONTINUE ",
                timeout_message="Let's go on!",
                defaultvalue="",
                cancelbutton="esc",
                show_special_characters_warning=None,
            ).finalvalue

    return return_value


#########################################################################################################################################


def composed(*decs):
    def deco(f):
        for dec in reversed(decs):
            f = dec(f)
        return f

    return deco


def get_detailed_debugger():

    allezusammen = composed(ignore_exceptions, trace, time_, debug_decorator)
    detailed_debugger = SwitchedDecorator(allezusammen)
    return detailed_debugger
