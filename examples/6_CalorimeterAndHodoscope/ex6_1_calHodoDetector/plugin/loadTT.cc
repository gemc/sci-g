#include "ch.h"

// ccdb
#include <CCDB/Calibration.h>
#include <CCDB/Model/Assignment.h>
#include <CCDB/CalibrationGenerator.h>
using namespace ccdb;

string connection = "mysql://clas12reader@clasdb.jlab.org/clas12";
unique_ptr<Calibration> calib(CalibrationGenerator::CreateCalibration(connection));

int icomponent;
vector<vector<double> > data;

bool chPlugin::loadTT(int runno, string variation)
{
	translationTable = new GTranslationTable();

	vector<vector<double> > data;

	string database   = "/daq/tt/ftcal:1";
	gLogMessage("FT-CAL: Loading Translation Table " + database);
	data.clear(); calib->GetCalib(data, database);

	// filling translation table
	for(unsigned row = 0; row < data.size(); row++) {
		int crate   = data[row][0];
		int slot    = data[row][1];
		int channel = data[row][2];

		int sector  = data[row][3];
		int layer   = data[row][4];
		int crystal = data[row][5];
		int order   = data[row][6];

		// order is important as we could have duplicate entries w/o it
		int mode = 1;
		translationTable->addGElectronicWithIdentity({sector, layer, crystal, order}, GElectronic(crate, slot, channel, mode));
	}

	return true;
}
