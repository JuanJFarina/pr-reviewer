### Scope
- Apply this rule when creating or editing Python code (.py, .pyi).
- Use these standards across all Python modules, packages, and tests.
- Provide examples in PRs when deviating for justified reasons (e.g., complex package layouts).

### Imports

- Put imports at the top of the file, after the module docstring and dunders, before globals/constants.
- Group imports in order with a blank line between groups:
  1) Standard library
  2) Third-party
  3) Local application/library
- Use absolute imports by default; explicit relative imports are acceptable for complex package layouts.
- Avoid wildcard imports (from module import *), except for republishing internal interfaces as a public API.
- When importing classes, import by name; if local names clash, import the module and qualify.

#### Examples:

```python
# Correct: separate lines
import os
import sys
```

```python
# Wrong:
import sys, os
```

```python
# Correct: grouped
import os
import sys

from typing import TypeVar

import requests

from . import sibling
from .sibling import example
```

```python
# Clash handling
import myclass
myclass.MyClass
```

```python
# Acceptable class import
from foo.bar.yourclass import YourClass
```

### Module Level Dunder Names

- Place dunders (e.g., __all__, __author__, __version__) after the docstring and after any from __future__ imports, but before other imports.

#### Example:

```python
"""This is the example module.

This module does stuff.
"""

from __future__ import barry_as_FLUFL

__all__ = ['a', 'b', 'c']
__version__ = '0.1'
__author__ = 'Cardinal Biggles'

import os
import sys
```

### Comments

- Avoid writing comments in general
- Do not write comments that explain the code, code should be self-explanatory and may also change over time
- Do write comments that explain decisions when it is not obvious

### Naming Conventions

- Avoid single-character names ‘l’, ‘O’, ‘I’ due to ambiguity.
- Identifiers in the standard library must be ASCII compatible (PEP 3131 policy).
- Modules/packages: short, all-lowercase; underscores allowed for modules, discouraged for packages. C/C++ extension modules use a leading underscore (e.g., _socket).
- Classes: CapWords (CamelCase). Use CapWords for exceptions; suffix “Error” for error exceptions.
- Functions/variables: lower_case_with_underscores. mixedCase only if required by existing prevailing style.
- Type variables (PEP 484): CapWords and short (e.g., T, AnyStr, Num). Use _co and _contra suffixes for variance.

#### Example:

```python
# Type variables
from typing import TypeVar
VT_co = TypeVar('VT_co', covariant=True)
KT_contra = TypeVar('KT_contra', contravariant=True)
```

- Function/method arguments: first arg of instance methods is self; first arg of class methods is cls.
- If a name clashes with a keyword, append a trailing underscore (class_ rather than clss).
- Methods/instance variables: lower_case_with_underscores.
- Use one leading underscore for non-public methods/attributes.
- Use two leading underscores for name mangling only to avoid subclass clashes (__attr -> _ClassName__attr).
- Constants: module-level, UPPER_CASE_WITH_UNDERSCORES (e.g., MAX_OVERFLOW).

### Designing for Inheritance

- Decide and document which attributes are public vs non-public. Prefer non-public by default.
- Public attributes: no leading underscores; append trailing underscore if keyword collision (e.g., class_).
- Use properties to evolve simple public data attributes when needed; avoid heavy computation in properties.
- Consider double leading underscores for attributes you explicitly don’t want subclasses to use; balance with debugging and advanced usage costs.

### Public and Internal Interfaces

- Backwards compatibility applies only to public interfaces. Undocumented interfaces are internal.
- Explicitly declare public API via __all__. An empty list means no public API.
- Internal names should still be prefixed with a single leading underscore.
- Imported names are implementation details unless explicitly documented as part of the API.

### Programming Recommendations

- Compare to None with is / is not. Prefer is not over not ... is.
- Implement all six rich comparisons (__eq__, __ne__, __lt__, __le__, __gt__, __ge__) or use functools.total_ordering.
- Use def instead of binding a lambda to a name.

#### Examples:

```python
# Correct:
def f(x): return 2 * x
```

```python
# Wrong:
f = lambda x: 2 * x
```

- Derive custom exceptions from Exception (not BaseException). Use “Error” suffix for error exceptions.
- Use exception chaining: raise X from Y; when suppressing original (raise X from None), preserve relevant details.
- Catch specific exceptions. Avoid bare except:; use except Exception: if catching all program errors.

#### Example:

```python
try:
    import platform_specific_module
except ImportError:
    platform_specific_module = None
```

- Keep try blocks minimal to avoid masking bugs.

#### Examples:
```python
# Correct:
try:
    value = collection[key]
except KeyError:
    return key_not_found(key)
else:
    return handle_value(value)
```

```python
# Wrong:
try:
    return handle_value(collection[key])  # Too broad; KeyError in handle_value() is also caught
except KeyError:
    return key_not_found(key)
```

- Use with statements for resource management; make context manager usage explicit when it does more than acquire/release.

#### Examples:

```python
# Correct:
with conn.begin_transaction():
    do_stuff_in_transaction(conn)
```

```python
# Wrong:
with conn:
    do_stuff_in_transaction(conn)
```

- Be consistent in return statements: either all return expressions or explicitly return None where appropriate.

#### Examples:

```python
# Correct:
def foo(x):
    if x >= 0:
        return math.sqrt(x)
    else:
        return None

def bar(x):
    if x < 0:
        return None
    return math.sqrt(x)
```

```python
# Wrong:
def foo(x):
    if x >= 0:
        return math.sqrt(x)

def bar(x):
    if x < 0:
        return
    return math.sqrt(x)
```

- Use .startswith() / .endswith() instead of slicing for prefix/suffix checks.
- Use isinstance() for type checks; avoid direct type comparisons.
- Use truthiness of sequences for emptiness checks; avoid len(seq) == 0 patterns.
- Don’t rely on significant trailing whitespace in string literals.
- Don’t compare booleans with == or is; use their truthiness.
- Avoid return/break/continue in finally blocks if it would jump outside finally, as it cancels active exceptions.

#### Examples:

```python
# Wrong:
def foo():
    try:
        1 / 0
    finally:
        return 42  # Cancels the ZeroDivisionError
```

### Function Annotations (PEP 484)

- Use PEP 484 syntax for function annotations. Third-party code may experiment within PEP 484 rules; stdlib code should be conservative.
- To ignore annotations in a file, add a top-level comment:

```python
# type: ignore
```

- Type checkers are optional tools; they do not affect runtime behavior. Use stub files (.pyi) where appropriate.

### Variable Annotations (PEP 526)

- Use a single space after the colon, none before it.
- If an assignment has a right hand side, put exactly one space around the equals.

#### Examples:

```python
# Correct:
code: int

class Point:
    coords: tuple[int, int]
    label: str = '<unknown>'
```

```python
# Wrong:
code:int          # No space after colon
code : int        # Space before colon

class Test:
    result: int=0  # No spaces around equality sign
```

### When generating code or reviewing PRs:

- Enforce these import, naming, interface, and annotation rules.
- Provide small code examples in comments when flagging violations.
- Avoid introducing new “magic” dunder names; only use documented ones.
- Prefer explicitness and consistency to cleverness.
