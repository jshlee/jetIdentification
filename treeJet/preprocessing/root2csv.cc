{ // START

// Load data
TFile *file = new TFile("../data/root/jet.root");
TTree *tree = (TTree *)file->Get("jetAnalyser/jetAnalyser");

int                      partonId;
std::vector<float>       *dau_jetNum, *dau_ptnId, *dau_charge, *dau_deta,*dau_dphi,*dau_pt;

tree->SetBranchAddress("partonId",&partonId);
tree->SetBranchAddress("dau_ptnId",&dau_ptnId);
tree->SetBranchAddress("dau_charge",&dau_charge);
tree->SetBranchAddress("dau_deta",&dau_deta);
tree->SetBranchAddress("dau_dphi",&dau_dphi);
tree->SetBranchAddress("dau_pt",&dau_pt);

// ready to write csv file
ofstream              outJ;
outJ.open("../data/csv/jet.csv");
outJ << "# pdgid, charged pt image (33*33), neutral pt image (33*33), charged multiplicity image (33*33)" << endl;

// using the histogram

TH2F *h_cpt, *h_npt, *h_cmul;

static const int   bin = 33;
static const float up  = 0.4;
static const float low = -up;

// write csv file
for(auto iev = 0; iev < tree->GetEntries(); ++iev) {
    tree->GetEntry(iev);
    outJ << partonId << ",";

    h_cpt  = new TH2F("h_cpt", "h_cpt", bin, low, up, bin, low, up);
    h_npt  = new TH2F("h_npt", "h_npt", bin, low, up, bin, low, up);
    h_cmul = new TH2F("h_cmul", "h_mul", bin, low, up, bin, low, up);

    // make histogram
    for(auto i = 0; i < dau_deta->size(); ++i) {
        // charged particle
        if( ( *dau_charge)[i] != 0 ) {
            h_cpt->Fill( (*dau_deta)[i], (*dau_dphi)[i], (*dau_pt)[i]);
            h_cmul->Fill( ( *dau_deta)[i], (*dau_dphi)[i] );
        }
        // neutral particle
        else {
            h_npt->Fill( (*dau_deta)[i], (*dau_dphi)[i], (*dau_pt)[i]);
        }
    }
    // charged pT
    for(Int_t j = 1; j <= h_cpt->GetNbinsX(); ++j) {
        for(Int_t k = 1; k <= h_cpt->GetNbinsY(); ++k)
                outJ << h_cpt->GetBinContent(j, k) << ",";
    }

    // neutral pT
    for(Int_t j = 1; j <= h_npt->GetNbinsX(); ++j) {
        for(Int_t k = 1; k <= h_npt->GetNbinsY(); ++k)
                outJ << h_npt->GetBinContent(j, k) << ",";
    }

    for(Int_t j = 1; j <= h_cmul->GetNbinsX(); ++j) {
        for(Int_t k = 1; k <= h_cmul->GetNbinsY(); ++k)
            if( j != h_cmul->GetNbinsX() or k != h_cmul->GetNbinsY() )
                outJ << h_cmul->GetBinContent(j, k) << ",";
            else
                outJ << h_cmul->GetBinContent(j, k) << endl;
    }
    delete h_cpt;
    delete h_npt;
    delete h_cmul;

} // FOR LOOP END

outJ.close();

} // END
