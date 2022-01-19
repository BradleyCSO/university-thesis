def singleton(class_):
    """
    Decorator for defining an object which acts as a singleton, the solution
    is provided by this author:
    https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
    """
    instances = {}

    def get_instance(*args, **kwargs):
        """
        Create, or acquire existing singleton
        :param args: Args
        :param kwargs: Kwargs
        :return: Instance
        """
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return get_instance
