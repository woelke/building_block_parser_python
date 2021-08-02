#!/usr/bin/python
from pathlib import Path

class ParseError(Exception):
    pass

class NoMoreArgs:
    def __call__(self, argv):
        if len(argv) > 0:
            raise ParseError(f"Expected no more arguments but received: {' '.join(argv)}")

        return [], dict()

class ParserBase:
    def __init__(self):
        self._next = None

    def __call__(self, argv):
        argv_new, parsed_args = self._parse(argv)
        if self._next is None:
            return argv_new, parsed_args
        argv_new, parsed_args_new = self._next(argv_new)
        return argv_new, parsed_args | parsed_args_new

    def _parse(self, arg):
        raise ParseError("_parse() not implemented")

    def __add__(self, next):
        last = self
        while last._next is not None:
            last = last._next
        last._next = next
        return self

class  Optional(ParserBase):
    def __init__(self, parser):
        super().__init__()
        self._parser = parser

    def _parse(self, argv):
        if len(argv) == 0:
            return [], dict()

        return self._parser(argv)

class OneOf(ParserBase):
    def __init__(self, *parsers):
        super().__init__()
        self._parsers = parsers

    def _parse(self, argv):
        for parser in self._parsers:
            try:
                return parser(argv)
            except ParseError:
                pass
        raise ParseError("None of the parsers were suitable")

class Exact(ParserBase):
    def __init__(self, key, value):
        super().__init__()
        self._key = key
        self._value = value

    def _parse(self, argv):
        if len(argv) == 0:
            if self._value == "":
                return [], {self._key : self._value}
            raise ParseError("Missing argument")
        if self._value != argv[0]:
            raise ParseError(f"cmd {self._value} expected but got {argv[0]}")
        return argv[1:], {self._key : self._value}

class Converter(ParserBase):
    def __init__(self, key, convert_to=(lambda x: x)):
        super().__init__()
        self._key = key
        self._convert_to = convert_to

    def _parse(self, argv):
        if len(argv) == 0:
            raise ParseError("Missing argument")
        return argv[1:], {self._key : self._convert_to(argv[0])}

class String(Converter):
    def __init__(self, key):
        super().__init__(key)  

class Integer(Converter):
    def __init__(self, key):
        super().__init__(key, (lambda x: int(x))) 

class ExistingPath(Converter):
    def __init__(self, key):
        def to_path(x):
            path = Path(x)
            if not path.exists():
                raise ParseError(f"path {path} does not exist")
            return path.absolute()
        super().__init__(key, to_path) 

class Flag(ParserBase):
    def __init__(self, key, value, parser):
        super().__init__()
        self._arg = {key : value}
        self._parser = parser

    def _parse(self, argv):
        argv_new, res = self._parser(argv)
        return argv_new, self._arg

Help = OneOf(Exact("help", "-h"), Exact("help", "--help"))

def show_result(parser, argv):
    try:
        print(parser(argv)[1])
    except ParseError as err:
        print(err)

def test1():
    # p1 = Exact("b") + Exact("c")
    # p2 = Exact("a") + p1
    # show_result(p1, ["b", "c"])
    # show_result(p2, ["a", "b", "c"])

    # p1 = Exact("cmd1", "p1") # + Exact("p11")
    # p2 = Exact("cmd2", "p2") + Exact("cmd22", "p22") + Optional(String("string"))
    # p = OneOf(p1,p2)
    # show_result(p, ["p1"])
    # show_result(p, ["p1", "p22"])

    install_p = OneOf(String("action")) + String("index")
    show_result(install_p, ["action", "index"])

if __name__ == "__main__":
    test1()