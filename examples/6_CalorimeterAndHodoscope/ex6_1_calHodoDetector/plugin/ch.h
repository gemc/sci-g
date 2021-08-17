#ifndef CHPLUGIN
#define CHPLUGIN 1

// gdynamicdigitization
#include "gdynamicdigitization.h"

class chPlugin : public GDynamicDigitization {

public:

	// mandatory readout specs definitions
	bool defineReadoutSpecs();

	// loads digitization constants
	bool loadConstants(int runno, string variation);

	// digitized the hit
	GDigitizedData* digitizeHit(GHit *ghit);

private:

	 // constants definitions

};

#endif

