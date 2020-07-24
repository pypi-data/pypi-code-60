# Ref: https://stackoverflow.com/a/16700993/9878098
# delattr() is what you want. Loop through vars() of the class and test for attribute names starting with "test_". E.g.,


class Dummy:
    @classmethod
    def __vars(cls):
        return list(vars(cls))

    @classmethod
    def remove_prefixed_methods(cls, prefix: str = "test_"):
        for name in cls.__vars():
            if name.startswith(prefix) and callable(getattr(cls, name)):
                print(name)
                # delattr(cls, name)


d = Dummy()
d.remove_prefixed_methods(prefix="")
print("*" * 40)


# I'd advise against using dir(), as this will show you names from your parent classes as well, so not all the names you get from dir() may defined on the class you're targeting.
