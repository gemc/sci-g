from gemc_api_geometry import GVolume

def build_geometry(configuration):
    build_mother_volume(configuration)
    build_target(configuration)
    build_lead_shield(configuration)


def build_mother_volume(configuration):
    gvolume = GVolume('cloud-chamber')
    gvolume.description = 'cloud chamber - for simplicity made of water vapor'
    gvolume.make_box(100.0, 100.0, 100.0)
    gvolume.material = 'G4_WATER_VAPOR'
    gvolume.color = '3399FF'
    gvolume.style = 0
    gvolume.digitization = 'flux'
    gvolume.set_identifier('cloud', 1)  # flux identifier for the cloud chamber
    gvolume.publish(configuration)

def build_target(configuration):
    gvolume = GVolume('target')
    gvolume.description = 'epoxy target'
    gvolume.mother = 'cloud-chamber'
    gvolume.make_tube(0, 20, 40, 0, 360)
    gvolume.material = 'G4_WATER_VAPOR'
    gvolume.color = 'ff0000'
    gvolume.publish(configuration)

def build_lead_shield(configuration):
    gvolume = GVolume('shield')
    gvolume.mother = 'cloud-chamber'
    gvolume.description = 'target shield'
    gvolume.make_tube(50, 50.1, 50, 0, 360)
    gvolume.material = 'G4_Pb'
    gvolume.color = '00ff00'
    gvolume.publish(configuration)
