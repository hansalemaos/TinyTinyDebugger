# TinyTinyDebugger

Simple debugger for small scripts - shows the line being executed, local vars, log files as xlsx
It only can be used if your script is in a .py file. It doesn't work directly from the console.
```python
pip install TinyTinyDebugger
```

```python
#Examples
from TinyTinyDebugger import get_detailed_debugger

#Configurations for all debugged functions with
detailed_debugger = get_detailed_debugger()
detailed_debugger.enabled = True
detailed_debugger.write_log_file = True
detailed_debugger.log_folder = "f:\\mylogstest2"
detailed_debugger.pause_for_n_seconds_when_exception = 1
detailed_debugger.continue_on_exceptions = True
detailed_debugger.print_write_exceptions_only = False


@detailed_debugger
def test1(x, y):
    vara = x * y * 1000


@detailed_debugger
def test2(x, y):
    test2 = x * y * 6
    test3 = x * y * 16
    return x * y


@detailed_debugger
def test3(*args, **kwargs):
    hal = "hallo" in kwargs
    return args


@detailed_debugger
def test4_exception(x, t):
    tt = t * t
    j = 0
    p = x / j
    return p


test1(44, 44)
test2(44, 122)
test3(3, 4, 4, hallo="baba")
test4_exception(199, 34)
```

<div>
<img title="" src="https://raw.githubusercontent.com/hansalemaos/TinyTinyDebugger/main/screen2.png" alt="">
</div>

```python
from TinyTinyDebugger import get_detailed_debugger
##Let's use some other configurations
detailed_debugger = get_detailed_debugger()
detailed_debugger.enabled = True
detailed_debugger.write_log_file = False
detailed_debugger.log_folder = "f:\\mylogstest2"
detailed_debugger.pause_for_n_seconds_when_exception = 1
detailed_debugger.continue_on_exceptions = True
detailed_debugger.print_write_exceptions_only = True


@detailed_debugger
def test1(x, y):
    vara = x * y * 1000


@detailed_debugger
def test2(x, y):
    test2 = x * y * 6
    test3 = x * y * 16
    return x * y


@detailed_debugger
def test3(*args, **kwargs):
    hal = "hallo" in kwargs
    return args


@detailed_debugger
def test4_exception(x, t):
    tt = t * t
    j = 0
    p = x / j
    return p


test1(44, 44)
test2(44, 122)
test3(3, 4, 4, hallo="baba")
test4_exception(199, 34)
```

<div>
<img title="" src="https://raw.githubusercontent.com/hansalemaos/TinyTinyDebugger/main/screen1.png" alt="">
</div>
