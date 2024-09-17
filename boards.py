# The boards to be displayed

class Inkplate6MOTION:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Inkplate6MOTION, cls).__new__(cls)
        return cls._instance
    def __init__(self, parent=None):
        if not hasattr(self, '_initialized'):
            self._initialized = True  # Avoids re-initialization
            self.name = "Inkplate 6MOTION"
            self.conversion_modes = ["Black and white (1-bit mode)", "Grayscale (4-bit mode)"]

class Inkplate10:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Inkplate10, cls).__new__(cls)
        return cls._instance
    def __init__(self, parent=None):
        if not hasattr(self, '_initialized'):
            self._initialized = True  # Avoids re-initialization
            self.name = "Inkplate 10"
            self.conversion_modes = ["Black and white (1-bit mode)", "Grayscale (3-bit mode)"]

class Inkplate6:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Inkplate6, cls).__new__(cls)
        return cls._instance
    def __init__(self, parent=None):
        if not hasattr(self, '_initialized'):
            self._initialized = True  # Avoids re-initialization
            self.name = "Inkplate 6"
            self.conversion_modes = ["Black and white (1-bit mode)", "Grayscale (3-bit mode)"]

class Inkplate6PLUS:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Inkplate6PLUS, cls).__new__(cls)
        return cls._instance
    def __init__(self, parent=None):
        if not hasattr(self, '_initialized'):
            self._initialized = True  # Avoids re-initialization
            self.name = "Inkplate 6PLUS"
            self.conversion_modes = ["Black and white (1-bit mode)", "Grayscale (3-bit mode)"]
