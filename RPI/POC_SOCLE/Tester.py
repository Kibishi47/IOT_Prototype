class Testable:
    def __init__(self) -> None:
        pass

    def test(self):
        return False

class TestLauncher:
    def __init__(self, isDebug = False) -> None:
        self.isDebug = isDebug
        self.object_in_error = None

    def test_object(self, object_testable:Testable):
        if self.isDebug:
            print(f"Testing of {object_testable.__class__.__name__}")
            if object_testable.test():
                print(f"No error found for {object_testable.__class__.__name__}")
                return True
            else:
                self.object_in_error = object_testable
                print(f"There is an issue for {object_testable.__class__.__name__}")
                return False
        else:
            return object_testable.test()
    
    def test_objects(self, objects_testable):
        for object_testable in objects_testable:
            if not self.test_object(object_testable):
                return False
        return True


    def get_class_name(self):
        if self.object_in_error is not None:
            return self.object_in_error.__class__.__name__
        else:
            return False

    @staticmethod
    def debug_mode():
        return TestLauncher(True)
