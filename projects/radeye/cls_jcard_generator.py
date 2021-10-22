import numpy as np
import random
import json

class jcard_ops():
    def __init__(self):
        pass


    def generateBase(self, g_system = "./radeye", g_factory="text", g_n=100):
        
        jcard_entries = {
        # sets the number of threads
        "nthreads": 4,

        # sets number of particles
        "n" : g_n, 

        # verbosity
        "verbosity": 2,
        "gsystemv": 0,
        "g4systemv": 0,

        # the ex1_1 system
        "+gsystem": [
            {
                "system":   g_system,
                "factory": g_factory,
                "variation": "default"
            }
        ]}

        return jcard_entries

    def generateOutput(self, jcard_entries):

        jcard_entries["+goutput"] = [
            {
                "format": "ROOT",
                "name": "events.root",
                "type": "event"
            },
            {
                "format": "TEXT",
                "name": "events.txt",
                "type": "event"
            }
        ]
        return jcard_entries

    def generateVolumePoints(self,
                            jcard_entries,
                            vol_x=(0,1), 
							vol_y=(0,1), 
							vol_z=(0,1), 
							points=2,
							pname="gamma",
							p=1, #Energy in MeV
							multiplicity=1,
							theta=-90,
							phi=0):
        # we assume the point will be specified in world region so we don't have to worry about coordinates
        
        # create a list to store the point variables
        uniform_vol_source = []

        for point in range(0,points):
            
            vx = random.uniform(vol_x[0], vol_x[1])
            vy = random.uniform(vol_y[0], vol_y[1])
            vz = random.uniform(vol_z[0], vol_z[1])

            # add this to the +gparticle array entry
            uniform_vol_source.append( {"pname":pname, "p":p, "multiplicity":multiplicity, 
                                        "theta":theta, "phi":phi, "vx":vx, "vy":vy, "vz":vz, "vunit":"mm"})

        jcard_entries["+gparticle"] =  uniform_vol_source

        return jcard_entries

    def save(self, jcard_entries, fle = "radeye1.jcard" ):
        # save the jcard in the current directory
        f = open(fle, 'w')
        json.dump(jcard_entries, f, indent=6)
        f.close()
        