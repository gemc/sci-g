#include "ch.h"

bool chPlugin::defineReadoutSpecs()
{
	float     timeWindow = 10;                  // electronic readout time-window of the detector
	float     gridStartTime = 0;                // defines the windows grid
	HitBitSet hitBitSet = HitBitSet("101011");  // defines what information to be stored in the hit
	bool      verbosity = true;

	readoutSpecs = new GReadoutSpecs(timeWindow, gridStartTime, hitBitSet, verbosity);

	cout << " defineReadoutSpecs " << endl;

	return true;
}


// DO NOT EDIT BELOW THIS LINE: defines how to create the <chPlugin>
extern "C" GDynamicDigitization* GDynamicFactory(void) {
	return static_cast<GDynamicDigitization*>(new chPlugin);
}

