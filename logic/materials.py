#material.py

class Material:
    """
    Represents a material with its electronic properties.
    """
    def __init__(self, name, dielectricConstant, effectiveMass_x, effectiveMass_y, effectiveMass_z, bandShift, backgroundDopingDensity):
        self.name = name
        self.dielectricConstant = dielectricConstant
        self.effectiveMass_x = effectiveMass_x
        self.effectiveMass_y = effectiveMass_y
        self.effectiveMass_z = effectiveMass_z
        self.bandShift = bandShift
        self.backgroundDopingDensity = backgroundDopingDensity

   