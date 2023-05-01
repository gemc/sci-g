from gemc_api_materials import GMaterial

def build_materials(configuration):

    gmaterial = GMaterial("my_scintillator")
    gmaterial.description = "user defined scintillator, 1.032 g/cm3"
    gmaterial.density = 1.032
    gmaterial.addNAtoms("H", 10)
    gmaterial.addNAtoms("C", 9)
    gmaterial.publish(configuration)


