from gemc_api_geometry import GVolume


def build_pim_absorption(configuration):
    build_mother_volume(configuration)
    build_target(configuration)


def build_mother_volume(configuration):
    gvolume = GVolume("vacuumDetector")
    gvolume.make_tube(0, 60, 210, 0, 360, 'cm')
    gvolume.material = 'G4_Galactic'
    gvolume.color = 'FFAAAA4'
    gvolume.digitization = 'flux'
    gvolume.set_identifier('det', 1)
    gvolume.publish(configuration)


def build_target(configuration):
    gvolume = GVolume("beamDump")
    gvolume.mother = 'vacuumDetector'
    gvolume.make_tube(0, 50, 200, 0, 360, 'cm')
    gvolume.color = 'AAAAFF'
    gvolume.material = 'G4_Al'
    gvolume.publish(configuration)
