# Blink
Object Oriented Programming (OOP) was originally conceived at least in part as an abstraction of the actor model of distributed functional programming in a serial computing environment.

Blink represents a simple return to that vision. It's a functional paradigm facilitated by an object oriented implementation.

Core to the idea is the `Function` object: a class that defines `inputs`, a `function` and an `output`. It's basically a function that is responsible for gathering it's own inputs and caching it's output (so other function objects can efficiently gather their own inputs).

These `Function` objects, taken together are wired up to require inputs from each other and generally form a directed acyclic graph, though there is no mechanism to enforce a DAG structure.

# Use

```
from blink import Function

class A(Function):
    def function(self):
        print('A running!')
        return 1

class B(Function):
    def function(self):
        print('B running!')
        return 2

class C(Function):
    def function(self):
        print('C running!')
        return self.kwargs['A'] + self.kwargs['B']

class D(Function):
    def function(self):
        return self.transformation(**self.kwargs)
    def transformation(self, **kw):
        print('D running!')
        return kw['C'] + 1

a = A()
b = B()
c = C({'A': a, 'B': b})
d = D({'C': c})

d.run()

>>> A running!
>>> B running!
>>> C running!
>>> D running!
>>> 4

d.visualize()

```
