from AbstractErogakiMaskError import AbstractErogakiMaskError

class NoCensoredRegionsFoundError(AbstractErogakiMaskError):
    def __init__(self, description):
        super().__init__(description)
