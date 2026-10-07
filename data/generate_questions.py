import csv
import os
import random

QUESTIONS = [
    # ---------------- Variables ----------------
    ("Variables", "Easy", "What is the output of print(2 + 3)?", "5", "23", "6", "Error"),
    ("Variables", "Easy", "Which is a valid variable name in Python?", "my_var", "1var", "my-var", "my var"),
    ("Variables", "Easy", "What is type(3.14)?", "float", "int", "str", "double"),
    ("Variables", "Easy", "Which symbol starts a single-line comment in Python?", "#", "//", "--", "/*"),
    ("Variables", "Easy", "What does the statement x = 5 do?", "Assigns 5 to x", "Compares x with 5", "Declares x as a constant", "Prints 5"),
    ("Variables", "Medium", "What is the output of print(7 // 2)?", "3", "3.5", "4", "3.0"),
    ("Variables", "Medium", "What is the output of print(type(10 / 2))?", "<class 'float'>", "<class 'int'>", "<class 'str'>", "<class 'double'>"),
    ("Variables", "Medium", "a, b = 1, 2\na, b = b, a\nprint(a, b)", "2 1", "1 2", "2 2", "1 1"),
    ("Variables", "Medium", "What is the output of print(2 ** 3 ** 2)?", "512", "64", "36", "128"),
    ("Variables", "Medium", "x = '5'\nprint(x * 2)", "55", "10", "Error", "5 2"),
    ("Variables", "Hard", "a = [1, 2]\nb = a\nb.append(3)\nprint(a)", "[1, 2, 3]", "[1, 2]", "[3]", "Error"),
    ("Variables", "Hard", "What is the output of print(0.1 + 0.2 == 0.3)?", "False", "True", "Error", "None"),
    ("Variables", "Hard", "x = 10\ndef f():\n    print(x)\nx = 20\nf()\nWhat is printed?", "20", "10", "Error", "None"),
    ("Variables", "Hard", "What is the output of print(bool('False'))?", "True", "False", "Error", "None"),
    ("Variables", "Hard", "What is the output of print(-7 // 2)?", "-4", "-3", "-3.5", "3"),

    # ---------------- Loops ----------------
    ("Loops", "Easy", "How many times does for i in range(5) iterate?", "5", "4", "6", "0"),
    ("Loops", "Easy", "Which keyword exits a loop immediately?", "break", "continue", "pass", "exit"),
    ("Loops", "Easy", "What does range(1, 4) produce?", "1, 2, 3", "1, 2, 3, 4", "0, 1, 2, 3", "2, 3, 4"),
    ("Loops", "Easy", "Which loop is best when the number of iterations is not known in advance?", "while", "for with range", "for with a list", "if"),
    ("Loops", "Easy", "What is the first value printed by for i in range(3): print(i)?", "0", "1", "3", "2"),
    ("Loops", "Medium", "s = 0\nfor i in range(1, 5):\n    s += i\nprint(s)", "10", "15", "6", "4"),
    ("Loops", "Medium", "Which keyword skips the rest of the current iteration?", "continue", "break", "pass", "skip"),
    ("Loops", "Medium", "for i in range(10, 0, -3):\n    print(i, end=' ')", "10 7 4 1", "10 7 4", "9 6 3", "10 7 4 1 0"),
    ("Loops", "Medium", "x = 0\nwhile x < 3:\n    x += 1\nprint(x)", "3", "2", "4", "0"),
    ("Loops", "Medium", "When does the else clause of a for loop run?", "When the loop finishes without break", "When the loop is broken", "Before the loop starts", "Only if the loop never runs"),
    ("Loops", "Hard", "for i in range(3):\n    for j in range(i):\n        print('*', end='')\nHow many * are printed in total?", "3", "6", "4", "2"),
    ("Loops", "Hard", "What is the output of print(sum(i for i in range(10) if i % 3 == 0))?", "18", "12", "27", "15"),
    ("Loops", "Hard", "count = 0\nfor i in range(5):\n    if i == 3:\n        break\n    count += 1\nelse:\n    count += 10\nprint(count)", "3", "13", "5", "15"),
    ("Loops", "Hard", "What is the time complexity of two nested loops that each run n times?", "O(n^2)", "O(n)", "O(log n)", "O(2n)"),
    ("Loops", "Hard", "i = 0\nwhile i < 5:\n    i += 2\n    if i == 4:\n        continue\n    print(i, end=' ')", "2 6", "2 4 6", "2 4", "6"),

    # ---------------- Functions ----------------
    ("Functions", "Easy", "Which keyword defines a function in Python?", "def", "func", "function", "define"),
    ("Functions", "Easy", "def f():\n    return 5\nprint(f())", "5", "None", "f", "Error"),
    ("Functions", "Easy", "What does a function without a return statement return?", "None", "0", "An empty string", "Error"),
    ("Functions", "Easy", "How do you call a function named greet?", "greet()", "call greet", "greet", "def greet()"),
    ("Functions", "Easy", "Values passed to a function when it is called are known as:", "Arguments", "Classes", "Modules", "Comments"),
    ("Functions", "Medium", "def f(a, b=2):\n    return a * b\nprint(f(3))", "6", "3", "Error", "5"),
    ("Functions", "Medium", "def f(*args):\n    return len(args)\nprint(f(1, 2, 3))", "3", "1", "Error", "6"),
    ("Functions", "Medium", "f = lambda x: x * 2\nprint(f(4))", "8", "6", "16", "Error"),
    ("Functions", "Medium", "def f(**kw):\n    return kw\nprint(f(a=1))", "{'a': 1}", "(a=1)", "[1]", "Error"),
    ("Functions", "Medium", "Which keyword lets a function modify a global variable?", "global", "nonlocal", "static", "extern"),
    ("Functions", "Hard", "def f(x, lst=[]):\n    lst.append(x)\n    return lst\nf(1)\nprint(f(2))", "[1, 2]", "[2]", "[1]", "Error"),
    ("Functions", "Hard", "def outer():\n    x = 1\n    def inner():\n        nonlocal x\n        x += 1\n    inner()\n    return x\nprint(outer())", "2", "1", "Error", "None"),
    ("Functions", "Hard", "def fact(n):\n    return 1 if n <= 1 else n * fact(n - 1)\nprint(fact(5))", "120", "24", "5", "720"),
    ("Functions", "Hard", "What does a decorator do?", "Wraps a function to extend its behaviour", "Deletes a function", "Declares a variable type", "Compiles the code"),
    ("Functions", "Hard", "def gen():\n    yield 1\n    yield 2\nprint(list(gen()))", "[1, 2]", "[2]", "1", "<generator>"),

    # ---------------- OOP ----------------
    ("OOP", "Easy", "Which keyword creates a class?", "class", "def", "object", "struct"),
    ("OOP", "Easy", "An object is:", "An instance of a class", "A function", "A loop", "A module"),
    ("OOP", "Easy", "What is the constructor method named in Python?", "__init__", "__new_class__", "init", "constructor"),
    ("OOP", "Easy", "What does self refer to inside a method?", "The current instance", "The class name", "The parent class", "A global variable"),
    ("OOP", "Easy", "Which OOP principle hides internal details of an object?", "Encapsulation", "Inheritance", "Polymorphism", "Recursion"),
    ("OOP", "Medium", "class A: pass\nclass B(A): pass\nprint(issubclass(B, A))", "True", "False", "Error", "None"),
    ("OOP", "Medium", "How does a child class call its parent's __init__?", "super().__init__()", "parent.__init__()", "base()", "self.super()"),
    ("OOP", "Medium", "A child method with the same name as a parent method replaces it. This is called:", "Overriding", "Overloading", "Encapsulation", "Slicing"),
    ("OOP", "Medium", "Which decorator defines a method that receives the class (cls) instead of an instance?", "@classmethod", "@staticmethod", "@property", "@abstractmethod"),
    ("OOP", "Medium", "What happens to an attribute named __x inside a class?", "Name mangling", "It is deleted", "Compile error", "It becomes constant"),
    ("OOP", "Hard", "class A:\n    def f(self): return 'A'\nclass B(A): pass\nclass C(A):\n    def f(self): return 'C'\nclass D(B, C): pass\nprint(D().f())", "C", "A", "Error", "None"),
    ("OOP", "Hard", "class A:\n    x = 1\na1 = A(); a2 = A()\nA.x = 5\nprint(a1.x, a2.x)", "5 5", "1 1", "5 1", "Error"),
    ("OOP", "Hard", "Which special method controls what print(obj) shows?", "__str__", "__print__", "__show__", "__disp__"),
    ("OOP", "Hard", "What does the @property decorator do?", "Lets a method be accessed like an attribute", "Makes an attribute private", "Makes a class abstract", "Makes a method static"),
    ("OOP", "Hard", "class A:\n    def __init__(self): self.v = 1\nclass B(A):\n    def __init__(self): self.w = 2\nprint(hasattr(B(), 'v'))", "False", "True", "Error", "None"),

    # ---------------- Data Structures ----------------
    ("Data Structures", "Easy", "Which of these is mutable?", "list", "tuple", "str", "int"),
    ("Data Structures", "Easy", "What is len([1, 2, 3])?", "3", "2", "4", "Error"),
    ("Data Structures", "Easy", "How do you access the first element of list a?", "a[0]", "a[1]", "a(0)", "a.first()"),
    ("Data Structures", "Easy", "Which structure stores key-value pairs?", "dict", "list", "tuple", "set"),
    ("Data Structures", "Easy", "Which built-in structure does not allow duplicate elements?", "set", "list", "tuple", "str"),
    ("Data Structures", "Medium", "a = [1, 2, 3, 4]\nprint(a[1:3])", "[2, 3]", "[1, 2, 3]", "[2, 3, 4]", "[1, 2]"),
    ("Data Structures", "Medium", "What is the output of print(set([1, 2, 2, 3]))?", "{1, 2, 3}", "{1, 2, 2, 3}", "[1, 2, 3]", "Error"),
    ("Data Structures", "Medium", "d = {'a': 1}\nprint(d.get('b', 0))", "0", "None", "KeyError", "1"),
    ("Data Structures", "Medium", "Which list method removes and returns the last item?", "pop()", "remove()", "delete()", "discard()"),
    ("Data Structures", "Medium", "t = (1, 2, 3)\nt[0] = 9\nWhat happens?", "TypeError", "t becomes (9, 2, 3)", "t becomes [9, 2, 3]", "Nothing happens"),
    ("Data Structures", "Hard", "What is the average time complexity of a dict lookup?", "O(1)", "O(n)", "O(log n)", "O(n log n)"),
    ("Data Structures", "Hard", "a = [3, 1, 2]\nb = sorted(a)\nprint(a)", "[3, 1, 2]", "[1, 2, 3]", "None", "Error"),
    ("Data Structures", "Hard", "s = []\ns.append(1)\ns.append(2)\ns.append(3)\ns.pop()\ns.pop()\nprint(s)", "[1]", "[3]", "[1, 2]", "[2, 3]"),
    ("Data Structures", "Hard", "print([x * x for x in range(5) if x % 2 == 0])", "[0, 4, 16]", "[0, 1, 4, 9, 16]", "[4, 16]", "[0, 2, 4]"),
    ("Data Structures", "Hard", "Which structure gives O(1) removal from the front (a queue)?", "collections.deque", "list", "tuple", "set"),
]


def main():
    rng = random.Random(42)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "questions.csv")
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["question_id", "question", "option_a", "option_b", "option_c", "option_d",
                    "correct_answer", "topic", "difficulty"])
        for i, (topic, diff, q, right, *wrong) in enumerate(QUESTIONS, start=1):
            opts = [right] + wrong
            rng.shuffle(opts)
            letter = "ABCD"[opts.index(right)]
            w.writerow([f"Q{i:03d}", q, *opts, letter, topic, diff])
    print(f"Wrote {len(QUESTIONS)} questions to {out}")


if __name__ == "__main__":
    main()
