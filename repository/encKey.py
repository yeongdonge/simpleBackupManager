from cryptography.fernet import Fernet


class EncKey:
    __instance = None

    def __init__(self):
        if EncKey.__instance is not None:
            raise Exception("Singleton clss, use instance() method instead")
        else:
            EncKey.__instance = self
            self.key = Fernet.generate_key()

    @staticmethod
    def instance():
        if EncKey.__instance is None:
            EncKey()
        return EncKey.__instance
