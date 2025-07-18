from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit, QPushButton, QScrollArea, QMainWindow, QTabWidget
)
class StartHereTab(QWidget):
    def __init__(self, state_manager):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        instructions = QTextEdit()
        instructions.setReadOnly(True)
        instructions.setPlainText(self.get_plain_content())
        layout.addWidget(instructions)

    def get_plain_content(self):
        return (
            "Welcome to DotArray2 XML Editor\n\n"
            "Purpose: This editor helps configure DotArray2.xml input files used in quantum device simulation workflows.\n\n"
            "What Each Tab Does:\n"
                        "- Main: Displays the raw XML file as plain text for read-only viewing.\n"
            "- 1.Run Parameters: Controls simulation settings like threading, self-consistency flags, and output parameters.\n"
            "  Includes: RunParameters, PoissonSolver_NumericalParameters, SP_Parameters, SingleParticleEigensystemParameters\n"
            "- 2.Auto Tuning: Configure automatic tuning parameters for simulation optimization.\n"
            "  Includes: AutoTuningData, AutoTuningInput, AutoTuningOutput, ImportExportSPiterate, CreateInitialSPiterate\n"
            "- 3.Boundary Conditions: Set interface and lower surface boundary conditions.\n"
            "  Includes: InterfaceBCparameters, EffectiveBC_Parameters, LowerSurfaceBoundaryConditions\n"
            "- 4.Transverse Meshing and Gate Smoothing: Sets mesh density and smoothing for transverse geometry regions.\n"
            "  Includes: TransverseParameters, GateSmoothingParameters\n"
            "- 5.Import/Export Initial Solution: Configure import/export settings for initial solutions.\n"
            "  Includes: ImportExportSPiterate, CreateInitialSPiterate\n"
            "- 6.Computational Subdomains and Settings: Adjust computational subdomains and interpolation/smoothing settings.\n"
            "  Includes: MultiDomainParameters, ComputationalSubdomains\n"
            "- 7.Tunneling and Excluded Potential Calculation: Configure tunneling rate calculations and excluded potential setups.\n"
            "  Includes: TunnelingRateCalculation, ExcludedPotentialCalculation\n"
            "- 8.Layered Structure: Define the stack of material layers used in the device.\n"
            "- 9.MultiDomain Settings: Adjust computational subdomains and interpolation/smoothing settings.\n"
            "- 10.Material List: Browse material properties in a quick lookup window.\n\nView and edit the list of materials and their physical properties.\n"
            "- Layers: Add, remove, or modify layers within the Layered Structure interactively.\n"
'''
                ✅ Included in Description and Present in XML:

                RunParameters

                PoissonSolver_NumericalParameters

                SP_Parameters

                SingleParticleEigensystemParameters

                AutoTuningData

                AutoTuningInput

                AutoTuningOutput

                ImportExportSPiterate

                CreateInitialSPiterate

                InterfaceBCparameters

                EffectiveBC_Parameters

                LowerSurfaceBoundaryConditions

                TransverseParameters

                GateSmoothingParameters

                MultiDomainParameters

                ComputationalSubdomains

                TunnelingRateCalculation

                ExcludedPotentialCalculation

                LayeredStructure

                MaterialList

                ⚠️ Present in XML But Not Explicitly Listed in Description:

                GateBias

                EffectiveBC

                NoiseSources

                MaterialDataSource"
'''
            "Basic Workflow:\n"
            "1. Load an XML File using the Initial Window.\n"
            "2. Edit Parameters via the section tabs.\n"
            "3. Save Your Work by clicking 'Save Edited XML'.\n"
            "4. Use Tooltips by focusing on a field (if enabled).\n"
        )
