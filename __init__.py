import os
import sys
from collections import defaultdict
from functools import wraps
from files_folders_with_timestamp import get_timestamp
from tolerant_isinstance import isinstance_tolerant
from copy_functions_and_more import copy_func
from cprinter import TC
from sleepchunk import sleep_with_statusbar, sleep
from windows_filepath import make_filepath_windows_comp
import time

copiedfu = copy_func(sys.settrace)


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


nested_dict = lambda: defaultdict(nested_dict)
get_stdfolder = lambda: os.path.normpath(
    os.path.join(os.getcwd(), "_tinytinydebugger_log")
)

detailed_debugger = sys.modules[__name__]
detailed_debugger.local_function_vars = nested_dict()
detailed_debugger.write_log_file = True
detailed_debugger.log_folder = get_stdfolder()
detailed_debugger.pause_for_n_seconds_when_except = 1
detailed_debugger.continue_on_exceptions = True
detailed_debugger.capture_local_vars = True
detailed_debugger.color_print = True
detailed_debugger.print_local_vars = True
detailed_debugger.print_line = True
detailed_debugger.print_return = True
detailed_debugger.print_exception = True
detailed_debugger.sleep_between_each_line = 0


def _print_results(counter, event, v1, v2, v3, v4, v5, v6):

    pru = lambda: f"---------------------------\nCounter:     {counter}"

    wholeprintline = f"{v1}\n{v2}\n{v3}\n{v4}\n{v5}\n"
    if event == "line":
        if detailed_debugger.print_line:
            print(pru())
            if not detailed_debugger.color_print:
                print(wholeprintline)
            else:
                c_lightgreen_bg_black(wholeprintline)

    elif event == "return":
        if detailed_debugger.print_return:
            print(pru())
            if not detailed_debugger.color_print:
                print(wholeprintline)
            else:
                c_orange_bg_black(wholeprintline)
    elif event == "exception":
        if detailed_debugger.print_exception:
            print(pru())
            if not detailed_debugger.color_print:
                print(f"{v6}\n")
                print(wholeprintline)
            else:
                c_lightred_bg_black(f"{v6}\n")
                c_red_bg_black(wholeprintline)
    else:
        pass


class debug_context:
    # based on https://stackoverflow.com/a/32261446/15096247

    def __init__(self, name, fname):
        self.name = name
        self.filename = os.path.normpath(fname)
        self.all_code_lines = self.read_py_file(self.filename)
        self.counter = 0

    def read_py_file(self, filename):
        allezeilen = []
        try:
            with open(filename, mode="r", encoding="utf-8") as f:
                allezeilen = [_.rstrip() for _ in f.read().splitlines()]

        except Exception:
            pass
        return allezeilen

    def __enter__(self):
        sys.settrace(self.trace_calls)

    def __exit__(self, *args, **kwargs):
        sys.settrace = copy_func(copiedfu)

    def trace_calls(self, frame, event, arg):
        if event != "call":
            return
        elif frame.f_code.co_name != self.name:
            return
        return self.trace_lines

    def trace_lines(self, frame, event, arg):
        co = frame.f_code
        func_name = co.co_name
        line_no = frame.f_lineno
        filename = co.co_filename
        local_vars = frame.f_locals
        if filename != self.filename:
            self.filename = filename
            self.all_code_lines = self.read_py_file(self.filename)
        one_line_of_code = self.all_code_lines[line_no - 1].strip()

        detailed_debugger.local_function_vars[self.counter]["function"] = func_name
        detailed_debugger.local_function_vars[self.counter]["event"] = event
        detailed_debugger.local_function_vars[self.counter]["line_number"] = line_no
        detailed_debugger.local_function_vars[self.counter]["code"] = one_line_of_code
        detailed_debugger.local_function_vars[self.counter]["local_vars"] = None
        detailed_debugger.local_function_vars[self.counter]["log_file"] = None

        if isinstance_tolerant(arg, tuple):
            detailed_debugger.local_function_vars[self.counter]["extra"] = arg[1]
        else:
            detailed_debugger.local_function_vars[self.counter]["extra"] = arg
        if detailed_debugger.capture_local_vars is True:
            detailed_debugger.local_function_vars[self.counter][
                "local_vars"
            ] = local_vars
        exception_infos = detailed_debugger.local_function_vars[self.counter]
        v1 = f"Function:    {exception_infos['function']}"
        v2 = f"Event:       {exception_infos['event']}"
        v3 = f"Line Number: {exception_infos['line_number']}"
        v4 = "Local Vars:  "
        if detailed_debugger.print_local_vars:
            v4 = f"Local Vars:  {exception_infos['local_vars']}"
        v5 = f"Code:        {exception_infos['code']}"
        v6 = f"{exception_infos['extra']}"

        _print_results(self.counter, exception_infos["event"], v1, v2, v3, v4, v5, v6)
        if detailed_debugger.write_log_file:
            tsa = get_timestamp(sep="-")
            fp = make_filepath_windows_comp(
                filepath=f"""{tsa}__{str(self.counter).zfill(6)}_{exception_infos['event']}_{exception_infos['line_number']}___{exception_infos['code']}.txt""",
                fillvalue="-",  # replacement of any illegal char
                reduce_fillvalue=True,  # */<> (illegal chars) -> ____ (replacement) -> _ (reduced replacement)
                remove_backslash_and_col=True,  # important for multiple folders
                spaceforbidden=False,  # '\s' -> _
                other_to_replace=(),  # other chars you don't want in the file path
                slash_to_backslash=False,  # replaces / with \\ before doing all the other replacements
            )
            fp = os.path.normpath(os.path.join(detailed_debugger.log_folder, fp))
            if not os.path.exists(detailed_debugger.log_folder):
                os.makedirs(detailed_debugger.log_folder)
            ba = repr(detailed_debugger.local_function_vars[self.counter])
            ba = ba[ba.find("{") : -1]
            try:
                with open(fp, mode="w", encoding="utf-8") as f:
                    f.write(ba)
                detailed_debugger.local_function_vars[self.counter]["log_file"] = fp
            except Exception as fa:
                print(f"Problems writing the log file: {fp}")
                print(fa)
        self.counter += 1
        if detailed_debugger.sleep_between_each_line > 0:
            sleep(detailed_debugger.sleep_between_each_line)


def function_debug(
    f=None,  # reserved for the decorated function, don't use
    active=True,  # used to disable the debugger
    write_log_file=False,  # if True, data will be saved to hdd. Import allow_long_path_windows from windows_filepath and execute before! function_debug won't check for path length, so it is better to allow long file names
    log_folder=get_stdfolder(),  # default value is the folder "_tinytinydebugger_log" in cwd
    pause_for_n_seconds_when_except=10,  # Only important if continue_on_exceptions is True. The execution will be paused and you can read the Exception. When you are done, press ctrl+c to continue
    continue_on_exceptions=True,  # if True, the execution will go on
    capture_local_vars=True,  # If True, all local variables in the function will be saved after each line in: detailed_debugger.local_function_vars
    color_print=True,  # black/white or colored
    print_line=True,  # If False, the event "line" won't be printed
    print_return=True,  # If False, the event "return" won't be printed
    print_exception=True,  # If False, the event "exception" won't be printed
    print_execution_time=True,  # enable/disable printing of execution time
    print_local_vars=True,  # if True: prints all local variables in the function each line
    sleep_between_each_line=0,  # sleep after each line of code
):
    detailed_debugger.local_function_vars = nested_dict()

    detailed_debugger.write_log_file = write_log_file
    detailed_debugger.log_folder = log_folder
    detailed_debugger.pause_for_n_seconds_when_except = pause_for_n_seconds_when_except
    detailed_debugger.continue_on_exceptions = continue_on_exceptions
    detailed_debugger.capture_local_vars = capture_local_vars
    detailed_debugger.color_print = color_print
    detailed_debugger.print_line = print_line
    detailed_debugger.print_return = print_return
    detailed_debugger.print_exception = print_exception
    detailed_debugger.print_local_vars = print_local_vars
    detailed_debugger.sleep_between_each_line = sleep_between_each_line

    def dec(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if active:
                xa = None
                try:
                    exestart = 0
                    if print_execution_time:
                        exestart = time.perf_counter()
                    with debug_context(func.__name__, fname=__file__):
                        xa = func(*args, **kwargs)
                    if print_execution_time:
                        exeend = time.perf_counter()
                        if color_print:
                            print(
                                TC(
                                    f"Execution time: {exeend - exestart}"
                                ).bg_black.fg_pink
                            )
                        else:
                            print(f"Execution time: {exeend - exestart}")
                except Exception as fe:
                    if not continue_on_exceptions:

                        raise fe
                    else:
                        if pause_for_n_seconds_when_except > 0:
                            print(
                                TC(
                                    "Exception! Press ctrl+c to continue"
                                ).bg_black.fg_red
                            )

                            sleep_with_statusbar(
                                detailed_debugger.pause_for_n_seconds_when_except
                            )
                finally:
                    sys.settrace = copy_func(copiedfu)
                return xa
            else:
                return func(*args, **kwargs)

        return wrapper

    return dec(f) if callable(f) else dec
