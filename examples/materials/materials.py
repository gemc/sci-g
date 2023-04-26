from gemc_api_materials import GMaterial


def build_materials(configuration):

    gmaterial = GMaterial("my_peek")
    gmaterial.description = "peek plastic 1.31 g/cm3"
    gmaterial.density = 1.31
    gmaterial.addMaterialWithFractionalMass("G4_C", 0.76)
    gmaterial.addMaterialWithFractionalMass("G4_H", 0.08)
    gmaterial.addMaterialWithFractionalMass("G4_O", 0.16)
    gmaterial.publish(configuration)

    gmaterial = GMaterial("my_epoxy")
    gmaterial.description = "epoxy glue 1.16 g/cm3"
    gmaterial.density = 1.16
    gmaterial.addNAtoms("H", 32)
    gmaterial.addNAtoms("N", 2)
    gmaterial.addNAtoms("O", 4)
    gmaterial.addNAtoms("C", 15)
    gmaterial.publish(configuration)

    gmaterial = GMaterial("my_carbonFiber")
    gmaterial.description = "ft carbon fiber material is epoxy and carbon - 1.75g/cm3"
    gmaterial.density = 1.75
    gmaterial.addMaterialWithFractionalMass("G4_C", 0.745)
    gmaterial.addMaterialWithFractionalMass("my_epoxy", 0.255)
    gmaterial.publish(configuration)

    # resistive strips
    # 81% filling fraction, 1.33 density
    resistPasteTransparency_Density = 0.81 * 1.33
    gmaterial = GMaterial("my_resistPaste")
    gmaterial.description = "resistive strips paste"
    gmaterial.density = resistPasteTransparency_Density
    gmaterial.addMaterialWithFractionalMass("G4_C", 1)
    gmaterial.publish(configuration)
