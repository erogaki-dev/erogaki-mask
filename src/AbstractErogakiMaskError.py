from erogaki_wrapper_shared_python.AbstractErogakiWrapperError import AbstractErogakiWrapperError

class AbstractErogakiMaskError(AbstractErogakiWrapperError):
    def __init__(self, description):
        self.component = "erogaki-mask"
        super().__init__(description)
