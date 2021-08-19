#ifndef CHPLUGIN
#define CHPLUGIN 1

// glibrary
#include "gdynamicdigitization.h"
#include "gutsConventions.h"

class chPlugin : public GDynamicDigitization {

public:

	// mandatory readout specs definitions
	bool defineReadoutSpecs();

	// loads digitization constants
	bool loadConstants(int runno, string variation);

	// loads the translation table
	bool loadTT(int runno, string variation);

	// digitized the hit
	GDigitizedData* digitizeHit(GHit *ghit, int hitn);

private:

	// noise
	double pedestal[484];
	double pedestal_rms[484];
	double noise[484];
	double noise_rms[484];
	double threshold[484];

	// energy
	double mips_charge[484];
	double mips_energy[484];
	double fadc_to_charge[484];
	double preamp_gain[484];
	double apd_gain[484];

	// time
	double time_offset[484];
	double time_rms[484];

	// fadc parameters
	double ns_per_sample;
	double fadc_input_impedence;
	double time_to_tdc;
	double tdc_max;

	// preamp parameter
	double preamp_input_noise;
	double apd_noise ;

	// crystal paramters
	double light_speed;

	//	voltage signal parameters, using double gaussian + delay (function DGauss, need documentation for it)
	double vpar[4];

};

#endif

