class Testable:
    def __init__(self) -> None:
        pass

    def test(self):
        return False

class TestLauncher:
    def __init__(self) -> None:
        pass

    @staticmethod
    def test_object(object_testable:Testable):
        return object_testable.test()
    
    @staticmethod
    def test_objects(objects_testable):
        for object_testable in objects_testable:
            if not TestLauncher.test_object(object_testable):
                return False
        return True