// root
#include <TTree.h>
#include <TFile.h>
#include <TH1F.h>

void test()
{
	TFile* f = new TFile("events.root");
	TTree* tree = (TTree *) f -> Get("digitized_flux");
	
	vector<int>   *pids  = new vector<int>;
	vector<float> *kines = new vector<float>;
	
	tree->SetBranchAddress("pid",  &pids);
	tree->SetBranchAddress("kine", &kines);
	
	// Create histos
	
	// nu_mu pdg encoding: 14
	// anti_nu_mu pdg encoding: -14
	// nu_e pdg encoding: 12
	// anti_nu_e pdg encoding: -12
		
	TH1F *nu_mu      = new TH1F("#nu_{#mu}",       "", 300, 0., 300.);
	TH1F *anti_nu_mu = new TH1F("#bar{#nu}_{#mu}", "", 300, 0., 300.);
	TH1F *nu_e       = new TH1F("#nu_{e}",         "", 300, 0., 300.);
	TH1F *anti_nu_e  = new TH1F("#bar{#nu}_{e}",   "", 300, 0., 300.);
	
	Int_t nentries = (Int_t)tree -> GetEntries();
	cout << "n : "    <<  nentries  <<  endl;
	
	for(int i=0; i<nentries; i++){
		
		pids->clear();
		kines->clear();

		tree -> GetEntry(i);
		
		int nhits = pids->size();
		
		for (int h=0; h<nhits; h++) {
			
			int pid  = (*pids)[h];
			int kine = (*kines)[h];

//			if(pid ==  12 && kine > 5 )  { nu_e-> Fill(kine);      }
//			if(pid == -12 && kine > 6 )  { anti_nu_e->Fill(kine);  }
			if(pid ==  12)  { nu_e-> Fill(kine);      }
			if(pid == -12)  { anti_nu_e->Fill(kine);  }
			if(pid ==  14)  { nu_mu->Fill(kine);      }
			if(pid == -14)  { anti_nu_mu->Fill(kine); }

		}
				
		
	}
	
	TCanvas *c1  =  new TCanvas("c1", "neutrino energy");
	c1-> SetLogy();
	c1-> SetLineWidth(5);
	nu_mu -> GetXaxis()->SetTitle("Energy(MeV)");
	nu_mu -> SetLineColor(2);
	nu_mu -> Draw("hist");
	anti_nu_mu -> SetLineColor(4);
	anti_nu_mu -> Draw("histsame");
	nu_e -> SetLineColor(6);
	nu_e -> Draw("histsame");
	anti_nu_e -> SetLineColor(8);
	anti_nu_e -> Draw("histsame");
	
	c1->BuildLegend();
	
	
	int m1 = nu_mu->GetEntries();
	int m2 = anti_nu_mu->GetEntries();
	int e1 = nu_e->GetEntries();
	int e2 = anti_nu_e->GetEntries();
	
	int i1 = nu_mu->Integral(26,55);
	int i2 = anti_nu_mu->Integral(26,55);
	int i3 = nu_e->Integral(26,55);
	int i4 = anti_nu_e->Integral(26,55);

	cout << "nu_mu : "    <<  m1  <<  ",   nu_mu* : "   <<  m2 <<  ",   nu_e : " << e1  <<  ",   nu_e* : " << e2 <<  endl;
	cout << "nu_mu(25~55MeV) : "  <<  i1 <<  ",   nu_mu*(25~55MeV) : " << i2  << ",   nu_e(25~55MeV) : "  << i3 <<",   nu_e(25~55MeV) : "   << i4 << endl;
	
}
