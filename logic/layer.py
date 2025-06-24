# layer.py

class Layer:
    """
    Represents a single layer in the XML structure.
    """
    def __init__(self, name, materialType, height, panelDensity, localWaveCalcType):
        self.name = name
        self.materialType = materialType
        self.height = height
        self.panelDensity = panelDensity
        self.localWaveCalcType = localWaveCalcType

    def __repr__(self):
        return f"Layer(name={self.name}, materialType={self.materialType}, height={self.height}, panelDensity={self.panelDensity}, localWaveCalcType={self.localWaveCalcType})"
