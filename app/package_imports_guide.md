# Python Package Imports Guide

This file explains why `app/models/__init__.py` exists and how it changes imports.

## 1. Without `__init__.py`

If the folder is just a plain folder, Python does not treat it as a clean package unless it has an `__init__.py` file.

You would have to import from the exact files:

```python
from app.models.user import User
from app.models.product import Product
from app.models.order import Order
```

This works, but it is repetitive and less clean.

## 2. With `__init__.py`

Once `app/models/__init__.py` exists, the folder becomes a package.

Then you can write:

```python
from app.models import User, Product, Order
```

This works because the package file re-exports those model classes.

Example content of `__init__.py`:

```python
from app.models.user import User
from app.models.product import Product
from app.models.order import Order

__all__ = ["User", "Product", "Order"]
```

## 3. What `__all__` does

`__all__` is a list of names that should be imported when someone uses wildcard import syntax:

```python
from app.models import *
```

If `__all__` is set to:

```python
__all__ = ["User", "Product", "Order"]
```

then only those names are brought into the current namespace.

## 4. Why this matters

A package file makes imports cleaner and easier to maintain.

It helps when:
- you have many model files
- you want fewer repeated import paths
- you want one place to expose the public parts of a package

## 5. Plain English Summary

- `__init__.py` = package organizer
- `__all__` = public names exported by the package
- without it, imports are longer and less organized
- with it, code reads more cleanly
