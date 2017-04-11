#include <memory>
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/JetReco/interface/GenJet.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/JetReco/interface/PFJet.h"
#include "DataFormats/BTauReco/interface/JetTag.h"
#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "JetMETCorrections/Objects/interface/JetCorrector.h"

#include <TTree.h>
#include <TFile.h>
#include <TLorentzVector.h>

#include <fstream>

using namespace std;
using namespace reco;
using namespace edm;


class jetAnalyser : public edm::one::EDAnalyzer<edm::one::SharedResources>  {
public:
  explicit jetAnalyser(const edm::ParameterSet&);
  ~jetAnalyser(){};

private:
  virtual void 	                			beginJob() override;
  virtual void 						endJob() override;
  virtual void 						analyze(const edm::Event&, const edm::EventSetup&) override;
  template <class jetClass> bool 	                jetId(const jetClass *jet, bool tight = false, bool loose = false);
  std::tuple<int, int, int, float, float, float, float> calcVariables(const reco::Jet *jet, edm::Handle<reco::VertexCollection>& vC);

  //
  // <(") HERE
  //
  std::vector< std::vector<float> >                     makeJetMat(const reco::Jet *jet, edm::Handle<reco::VertexCollection>& vC, int jetNum, int ptnId);

  bool 							isPatJetCollection(const edm::Handle<edm::View<reco::Jet>>& jets);
  bool 							isPackedCandidate(const reco::Candidate* candidate);
  template<class a, class b> int 			countInCone(a center, b objectsToCount);
  int 							getPileUp(edm::Handle<std::vector<PileupSummaryInfo>>& pupInfo);
  reco::GenParticleCollection::const_iterator 		getMatchedGenParticle(const reco::Jet *jet, edm::Handle<reco::GenParticleCollection>& genParticles);

  edm::EDGetTokenT<edm::View<reco::Jet>> 		jetsToken;
  edm::EDGetTokenT<edm::View<reco::Candidate>> 		candidatesToken;
  edm::EDGetTokenT<double> 				rhoToken;
  edm::EDGetTokenT<reco::VertexCollection> 		vertexToken;
  edm::EDGetTokenT<reco::GenJetCollection> 		genJetsToken;
  edm::EDGetTokenT<reco::GenParticleCollection> 	genParticlesToken;
  edm::EDGetTokenT<reco::JetTagCollection> 		bTagToken;
  edm::EDGetTokenT<edm::ValueMap<float>> 		qgToken;
  edm::EDGetTokenT<std::vector<PileupSummaryInfo> > 	puToken;
  edm::InputTag						csvInputTag;
  edm::InputTag						qgInputTag;
  std::string 						jecService;
  const double 						minJetPt, deltaRcut;
  const bool 						useQC;

  const JetCorrector 					*JEC;
  edm::Service<TFileService> 				fs;
  TTree 						*tree;

  float rho, pt, eta, axis2, axis1, ptD, bTag, ptDoubleCone, motherMass, pt_dr_log, qgLikelihood_;
  int nEvent, nPileUp, nPriVtxs, mult, nmult, cmult, partonId, jetIdLevel, nGenJetsInCone, nGenJetsForGenParticle, nJetsForGenParticle, motherId;
  bool matchedJet, isPatJet_;
  std::vector<float> *closebyJetdR, *closebyJetPt;
  std::vector<int>   *dau_jetNum_, *dau_ptnId_, *dau_charge_;
  std::vector<float> *dau_deta_, *dau_dphi_, *dau_pt_;

  
  bool weStillNeedToCheckJets, weAreUsingPatJets;
  bool weStillNeedToCheckJetCandidates, weAreUsingPackedCandidates;
};

jetAnalyser::jetAnalyser(const edm::ParameterSet& iConfig) :
  jetsToken( consumes<edm::View<reco::Jet>>( iConfig.getParameter<edm::InputTag>("jetsInputTag"))),
  candidatesToken( consumes<edm::View<reco::Candidate>>( iConfig.getParameter<edm::InputTag>("pfCandidatesInputTag"))),
  rhoToken( consumes<double>( iConfig.getParameter<edm::InputTag>("rhoInputTag"))),
  vertexToken(    	consumes<reco::VertexCollection>( iConfig.getParameter<edm::InputTag>("vertexInputTag"))),
  genJetsToken(    	consumes<reco::GenJetCollection>( iConfig.getParameter<edm::InputTag>("genJetsInputTag"))),
  genParticlesToken(    consumes<reco::GenParticleCollection>( iConfig.getParameter<edm::InputTag>("genParticlesInputTag"))),
  puToken ( 		consumes<std::vector<PileupSummaryInfo> > (edm::InputTag("slimmedAddPileupInfo")) ),
  csvInputTag( iConfig.getParameter<edm::InputTag>("csvInputTag")),
  qgInputTag( iConfig.getParameter<edm::InputTag>("qgInputTag")),
  jecService( iConfig.getParameter<std::string>("jec")),
  minJetPt( iConfig.getUntrackedParameter<double>("minJetPt", 20.)),
  deltaRcut( iConfig.getUntrackedParameter<double>("deltaRcut", 0.3)),
  useQC( iConfig.getUntrackedParameter<bool>("useQualityCuts", false))
{
  weStillNeedToCheckJets	  = true;
  weStillNeedToCheckJetCandidates = true;
  bTagToken = consumes<reco::JetTagCollection>( edm::InputTag(csvInputTag));
  qgToken = consumes<edm::ValueMap<float> >( edm::InputTag(qgInputTag));
}

  void jetAnalyser::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup){

    //
    // <(") HERE
    //
    std::ofstream     outJets;
    outJets.open("yangJet.csv");
    outJets << "# jetNumbering, pdgid, deta, dphi, pt, charge" << endl;

    for(auto v : {closebyJetdR, closebyJetPt})
      v->clear();

    nEvent = (int) iEvent.id().event();

    edm::Handle< edm::View<reco::Jet> > jets;
    iEvent.getByToken(jetsToken, jets);

    edm::Handle< edm::View<reco::Candidate> > candidates;
    iEvent.getByToken(candidatesToken, candidates);

    edm::Handle< std::vector<PileupSummaryInfo> > pupInfo;
    iEvent.getByToken(puToken, 	pupInfo);

    edm::Handle< reco::VertexCollection > vertexCollection;
    iEvent.getByToken(vertexToken, vertexCollection);

    edm::Handle<double> rhoHandle;
    iEvent.getByToken(rhoToken, rhoHandle);

    edm::Handle<reco::GenJetCollection> genJets;
    iEvent.getByToken(genJetsToken, genJets);

    edm::Handle< reco::GenParticleCollection > genParticles;
    iEvent.getByToken(genParticlesToken, genParticles);

    edm::Handle< reco::JetTagCollection > bTagHandle;  
    isPatJet_ = isPatJetCollection(jets);
    if( !isPatJet_ )
      if(!csvInputTag.label().empty())
	iEvent.getByToken(bTagToken, bTagHandle);

    if( !isPatJet_ )
      JEC = JetCorrector::getJetCorrector(jecService, iSetup);

    edm::Handle<edm::ValueMap<float>> qgHandle;
    if(!qgInputTag.label().empty())
      iEvent.getByToken(qgToken, qgHandle);
  
    // Get number of primary vertices, pile-up and rho
    nPriVtxs = vertexCollection->size();
    rho      = (float) *rhoHandle;
    nPileUp  = getPileUp(pupInfo);

    //
    //  <(") HERE
    //  just jet numbering
    //
    int jetNum = 0;

    // Start jet loop (the tree is filled for each jet separately)
    for(auto jet = jets->begin();  jet != jets->end(); ++jet){
      // If miniAOD, jets are already corrected
      // If RECO, we correct them on the fly
      if(isPatJet_)
	pt = jet->pt();
      else
	pt = jet->pt()*JEC->correction(*jet, iEvent, iSetup);

      if(pt < minJetPt)
	continue;
    
      bool overLappingJet = false;
      // Remove Closeby jets for now. do late - Closeby jet study variables
      for(auto otherJet = jets->begin(); otherJet != jets->end(); ++otherJet){
	if(otherJet == jet)
	  continue;
	float dR = reco::deltaR(*jet, *otherJet);
	if(dR > deltaRcut)
	  continue;
	overLappingJet = true;
	// closebyJetdR->push_back(dR);
	// if( isPatJet_ )
	// 	closebyJetPt->push_back(otherJet->pt());
	// else
	// 	closebyJetPt->push_back(otherJet->pt()*JEC->correction(*otherJet, iEvent, iSetup));
      }
      if (overLappingJet) continue;

      // Parton Id matching
      auto matchedGenParticle = getMatchedGenParticle(&*jet, genParticles);
      matchedJet = (matchedGenParticle != genParticles->end());
      if(matchedJet){
	partonId 			= matchedGenParticle->pdgId();
	nJetsForGenParticle 	= countInCone(matchedGenParticle, jets);
	nGenJetsForGenParticle 	= countInCone(matchedGenParticle, genJets);
	if(matchedGenParticle->numberOfMothers() == 1){
	  // Very experimental, but first tests shows it's good at finding W's and t's
	  // A bit more difficult for QCD, where it's sometimes a quark, decaying into
	  // quark+gluon, and sometimes just a proton with a lot of other QCD mess and
	  // sometimes 2 mothers (mostly two quarks recoiling each other, but sometimes
	  // also two quarks going into two gluons etc...)
	  motherId		= matchedGenParticle->mother()->pdgId();
	  motherMass		= matchedGenParticle->mother()->mass();
	}
	else {
	  motherId		= 0;
	  motherMass		= 0;
	}
      }
      else {
	partonId 			= 0;
	nJetsForGenParticle 	= 0;
	nGenJetsForGenParticle 	= 0;
	motherId			= 0;
	motherMass		= 0;
	continue;
	// To keep the tuples small, we only save matched jets
      }
      nGenJetsInCone 		= countInCone(jet, genJets);

      if(isPatJet_){
	auto patJet 	= static_cast<const pat::Jet*> (&*jet);
	jetIdLevel	= jetId(patJet) + jetId(patJet, false, true) + jetId(patJet, true); 
	bTag		= patJet->bDiscriminator(csvInputTag.label());
      }
      else {
	edm::RefToBase<reco::Jet> jetRef(edm::Ref<edm::View<reco::Jet>>(jets, (jet - jets->begin())));
	auto recoJet 	= static_cast<const reco::PFJet*>(&*jet);
	jetIdLevel	= jetId(recoJet) + jetId(recoJet, false, true) + jetId(recoJet, true); 
	bTag		= csvInputTag.label().empty() ? 0 : (*bTagHandle)[jetRef];
	// cms qgLikelihood
	qgLikelihood_ = qgInputTag.label().empty() ? 0 : (*qgHandle)[jetRef];      
	/*    axis2		= (*axis2Handle)[jetRef];
	      mult		= (*multHandle)[jetRef];
	      ptD		= (*ptDHandle)[jetRef];*/
      }

      /////////////////////////////////////////////////////////////////////////////////////////////////////
      // 
      // <(") HERE
      // //
    
      dau_jetNum_ = new std::vector<int>();
      dau_ptnId_ = new std::vector<int>();
      dau_charge_ = new std::vector<int>();
      dau_deta_ = new std::vector<float>();
      dau_dphi_ = new std::vector<float>();
      dau_pt_ = new std::vector<float>();
    
      std::vector< std::vector<float> > jetMat = makeJetMat(&*jet, vertexCollection, jetNum, partonId);
      for(auto row = jetMat.begin(); row != jetMat.end(); ++row){
	for(auto col = row->begin(); col != row->end(); ++col){
	  if( col != --(row->end()) )
	    outJets << *col << ',';
	  else
	    outJets << *col << endl; 
	}
      }

      jetNum++;
      /////////////////////////////////////////////////////////////////////////////////////////////////////////

      std::tie(mult, nmult, cmult, ptD, axis2, axis1, pt_dr_log) = calcVariables(&*jet, vertexCollection);
      axis2 			= -std::log(axis2);
      axis1                   = -std::log(axis1);
      eta			= jet->eta();
      //  qg = qglcalc->computeQGLikelihood(pt, eta, rho, {(float) mult, ptD, axis2});
      if(mult < 2) continue;  
    
      ptDoubleCone = 0;
      for(auto candidate = candidates->begin(); candidate != candidates->end(); ++candidate){
	if(reco::deltaR(*candidate, *jet) < deltaRcut*2) ptDoubleCone += candidate->pt();
      }
 
      tree->Fill();
      delete dau_jetNum_;
      delete dau_ptnId_;
      delete dau_charge_;
      delete dau_deta_;
      delete dau_dphi_;
      delete dau_pt_;
    }


    outJets.close();
  }

//Begin job: create vectors and set up tree
void jetAnalyser::beginJob(){
  for(auto v : {&closebyJetdR, &closebyJetPt}) *v = new std::vector<float>();
  tree = fs->make<TTree>("jetAnalyser","jetAnalyser");
  tree->Branch("nEvent" ,			&nEvent, 			"nEvent/I");
  tree->Branch("nPileUp",			&nPileUp, 			"nPileUp/I");
  tree->Branch("nPriVtxs",			&nPriVtxs, 			"nPriVtxs/I");
  tree->Branch("rho" ,		        	&rho, 				"rho/F");
  tree->Branch("pt" ,				&pt,				"pt/F");
  tree->Branch("eta",				&eta,				"eta/F");
  tree->Branch("qgLikelihood",                  &qgLikelihood_,                   "qgLikelihood_/F");
  tree->Branch("axis2",		        	&axis2,				"axis2/F");
  tree->Branch("axis1",                         &axis1,                         "axis1/F");
  tree->Branch("ptD",				&ptD,				"ptD/F");
  tree->Branch("mult",			      &mult,				"mult/I");
  tree->Branch("nmult",                       &nmult,                         "nmult/I");
  tree->Branch("cmult",                       &cmult,                         "cmult/I");
  tree->Branch("pt_dr_log",                   &pt_dr_log,                     "pt_dr_log/F");
  tree->Branch("bTag",			      &bTag,				"bTag/F");
  tree->Branch("partonId",			&partonId,			"partonId/I");
  tree->Branch("motherId",			&motherId,			"motherId/I");
  tree->Branch("motherMass",			&motherMass,			"motherMass/F");
  tree->Branch("jetIdLevel",			&jetIdLevel,			"jetIdLevel/I");
  tree->Branch("nGenJetsInCone",		&nGenJetsInCone,		"nGenJetsInCone/I");
  tree->Branch("matchedJet",			&matchedJet,			"matchedJet/O");
  tree->Branch("ptDoubleCone",		        &ptDoubleCone,			"ptDoubleCone/F");
  tree->Branch("nGenJetsForGenParticle",	&nGenJetsForGenParticle,	"nGenJetsForGenParticle/I");
  tree->Branch("nJetsForGenParticle",   	&nJetsForGenParticle,   	"nJetsForGenParticle/I");
  tree->Branch("closebyJetdR",		"vector<float>",		&closebyJetdR);
  tree->Branch("closebyJetPt",		"vector<float>",		&closebyJetPt);

  tree->Branch("dau_jetNum",		"vector<int>",		&dau_jetNum_);
  tree->Branch("dau_ptnId",		"vector<int>",		&dau_ptnId_);
  tree->Branch("dau_charge",		"vector<int>",		&dau_charge_);
  tree->Branch("dau_deta",		"vector<float>",        &dau_deta_);
  tree->Branch("dau_dphi",		"vector<float>",        &dau_dphi_);
  tree->Branch("dau_pt",		"vector<float>",        &dau_pt_);
}

void jetAnalyser::endJob(){
  for(auto v : {closebyJetdR, closebyJetPt}) delete v;
}

//Function to tell us if we are using pat::Jet or reco::PFJet
bool jetAnalyser::isPatJetCollection(const edm::Handle<edm::View<reco::Jet>>& jets){

  if(weStillNeedToCheckJets){
    if(typeid(pat::Jet)==typeid(*(jets->begin())))
      weAreUsingPatJets = true;
    else if( typeid(reco::PFJet)==typeid(*(jets->begin())) )
      weAreUsingPatJets = false;
    else
      throw cms::Exception("WrongJetCollection", "Expecting pat::Jet or reco::PFJet");
    weStillNeedToCheckJets = false;
  }
  return weAreUsingPatJets;
}

//Function to tell us if we are using packedCandidates, only test for first candidate
bool jetAnalyser::isPackedCandidate(const reco::Candidate* candidate){

  if(weStillNeedToCheckJetCandidates){
    if( typeid(pat::PackedCandidate) == typeid(*candidate) )
      weAreUsingPackedCandidates = true;
    else if( typeid(reco::PFCandidate) == typeid(*candidate) )
      weAreUsingPackedCandidates = false;
    else
      throw cms::Exception("WrongJetCollection", "Jet constituents are not particle flow candidates");
    weStillNeedToCheckJetCandidates = false;
  }
  return weAreUsingPackedCandidates;
}

// 
// <(") HERE
// jetNum, partonFlavour, deta, dphi, pt, charge
//
std::vector< std::vector<float> > jetAnalyser::makeJetMat(const reco::Jet *jet, edm::Handle<reco::VertexCollection>& vC, int jetNum, int ptnId){

  std::vector< std::vector<float> >                       jetMat;
    
  //Loop over the jet constituents
  std::vector<float>                                      dauRow;
  for(auto daughter : jet->getJetConstituentsQuick()){

    float deta   = daughter->eta() - jet->eta();
    float dphi   = reco::deltaPhi(daughter->phi(), jet->phi());
    float pt     = daughter->pt();
    float charge = daughter->charge();

    dauRow.push_back(jetNum);
    dauRow.push_back(ptnId);
    dauRow.push_back(deta);
    dauRow.push_back(dphi);
    dauRow.push_back(pt);
    dauRow.push_back(charge);

    dau_jetNum_->push_back(jetNum);
    dau_ptnId_->push_back(ptnId);
    dau_deta_->push_back(deta);
    dau_dphi_->push_back(dphi);
    dau_pt_->push_back(pt);
    dau_charge_->push_back(charge);
    
    jetMat.push_back(dauRow);        
    dauRow.clear();
  }
  return jetMat;
}



//Calculation of axis2, mult and ptD
std::tuple<int, int, int, float, float, float, float> jetAnalyser::calcVariables(const reco::Jet *jet, edm::Handle<reco::VertexCollection>& vC){
  float sum_weight = 0., sum_deta = 0., sum_dphi = 0., sum_deta2 = 0., sum_dphi2 = 0., sum_detadphi = 0., sum_pt = 0.;
  int mult = 0, nmult = 0, cmult = 0;
  float pt_dr_log = 0;

  //Loop over the jet constituents
  for(auto daughter : jet->getJetConstituentsQuick()){
    if(isPackedCandidate(daughter)){
      //packed candidate situation
      auto part = static_cast<const pat::PackedCandidate*>(daughter);

      if(part->charge()){
	if(!(part->fromPV() > 1 && part->trackHighPurity()))
	  continue;
	if(useQC){
	  if((part->dz()*part->dz())/(part->dzError()*part->dzError()) > 25.)
	    continue;
	  if((part->dxy()*part->dxy())/(part->dxyError()*part->dxyError()) < 25.){
	    ++mult;
	    ++cmult;
	  }
	}
	else {
	  ++mult;
	  ++cmult;
	}
      }
      else {
	if(part->pt() < 1.0)
	  continue;
	++mult;
	++nmult;
      }

      //Calculate pt_dr_log                                                                                                                                 
      float dr = reco::deltaR(*jet, *part);
      pt_dr_log += std::log(part->pt()/dr);

    }
    else {
      auto part = static_cast<const reco::PFCandidate*>(daughter);

      reco::TrackRef itrk = part->trackRef();
      //Track exists --> charged particle
      if(itrk.isNonnull()){
	auto vtxLead  = vC->begin();
	auto vtxClose = vC->begin();
	//Search for closest vertex to track
	for(auto vtx = vC->begin(); vtx != vC->end(); ++vtx){
	  if(fabs(itrk->dz(vtx->position())) < fabs(itrk->dz(vtxClose->position())))
	    vtxClose = vtx;
	}
	if(!(vtxClose == vtxLead && itrk->quality(reco::TrackBase::qualityByName("highPurity"))))
	  continue;

	if(useQC){
	  //If useQC, require dz and d0 cuts
	  float dz = itrk->dz(vtxClose->position());
	  float d0 = itrk->dxy(vtxClose->position());
	  float dz_sigma_square = pow(itrk->dzError(),2) + pow(vtxClose->zError(),2);
	  float d0_sigma_square = pow(itrk->d0Error(),2) + pow(vtxClose->xError(),2) + pow(vtxClose->yError(),2);
	  if(dz*dz/dz_sigma_square > 25.)
	    continue;
	  if(d0*d0/d0_sigma_square < 25.) {
	    ++mult;
	    ++cmult;
	  }
	}
	else{
	  ++mult;
	  ++cmult;
	}
      }
      else {
	//No track --> neutral particle
	if(part->pt() < 1.0) continue;
	//Only use neutrals with pt > 1 GeV
	++mult;
	++nmult;
      }

      //Calculate pt_dr_log                                                                                                                                 
      float dr = reco::deltaR(*jet, *part);
      pt_dr_log += std::log(part->pt()/dr);
    }

    float deta   = daughter->eta() - jet->eta();
    float dphi   = reco::deltaPhi(daughter->phi(), jet->phi());
    float partPt = daughter->pt();
    float weight = partPt*partPt;

    sum_weight   += weight;
    sum_pt       += partPt;
    sum_deta     += deta*weight;
    sum_dphi     += dphi*weight;
    sum_deta2    += deta*deta*weight;
    sum_detadphi += deta*dphi*weight;
    sum_dphi2    += dphi*dphi*weight;
  }

  //Calculate axis2 and ptD
  float a = 0., b = 0., c = 0.;
  float ave_deta = 0., ave_dphi = 0., ave_deta2 = 0., ave_dphi2 = 0.;
  if(sum_weight > 0){
    ave_deta  = sum_deta/sum_weight;
    ave_dphi  = sum_dphi/sum_weight;
    ave_deta2 = sum_deta2/sum_weight;
    ave_dphi2 = sum_dphi2/sum_weight;
    a         = ave_deta2 - ave_deta*ave_deta;                          
    b         = ave_dphi2 - ave_dphi*ave_dphi;                          
    c         = -(sum_detadphi/sum_weight - ave_deta*ave_dphi);                
  }
  float delta = sqrt(fabs((a-b)*(a-b)+4*c*c));
  float axis2 = (a+b-delta > 0 ?  sqrt(0.5*(a+b-delta)) : 0);
  float axis1 = (a+b+delta > 0 ?  sqrt(0.5*(a+b+delta)) : 0);
  float ptD   = (sum_weight > 0 ? sqrt(sum_weight)/sum_pt : 0);
  return std::make_tuple(mult, nmult, cmult,  ptD, axis2, axis1, pt_dr_log);
}

//Calculate jetId for levels loose, medium and tight
template <class jetClass> bool jetAnalyser::jetId(const jetClass *jet, bool tight, bool medium){
  bool jetid = false;
  const auto& j = *jet;
  float NHF    = j.neutralHadronEnergyFraction();
  float NEMF   = j.neutralEmEnergyFraction();
  float CHF    = j.chargedHadronEnergyFraction();
  //float MUF    = j.muonEnergyFraction();
  float CEMF   = j.chargedEmEnergyFraction();
  int NumConst = j.chargedMultiplicity()+j.neutralMultiplicity();
  int CHM      = j.chargedMultiplicity();
  int NumNeutralParticle =j.neutralMultiplicity(); 
  float eta = j.eta();

  // POG JetID loose, tight, tightLepVeto
  if (not tight and not medium) { // loose -- default
    jetid=(NHF<0.99 && NEMF<0.99 && NumConst>1) && ((abs(eta)<=2.4 && CHF>0 && CHM>0 && CEMF<0.99) || abs(eta)>2.4) && abs(eta)<=2.7 ;
    jetid = jetid or (NEMF<0.90 && NumNeutralParticle>2 && abs(eta)>2.7 && abs(eta)<=3.0 ) ;
    jetid = jetid or (NEMF<0.90 && NumNeutralParticle>10 && abs(eta)>3.0 ) ;
    return jetid;
  }

  if (medium) {// no medium recommendation at the moment. https://twiki.cern.ch/twiki/bin/viewauth/CMS/JetID this is LOOSE
    jetid=(NHF<0.99 && NEMF<0.99 && NumConst>1) && ((abs(eta)<=2.4 && CHF>0 && CHM>0 && CEMF<0.99) || abs(eta)>2.4) && abs(eta)<=2.7 ;
    jetid = jetid or (NEMF<0.90 && NumNeutralParticle>2 && abs(eta)>2.7 && abs(eta)<=3.0 ) ;
    jetid = jetid or (NEMF<0.90 && NumNeutralParticle>10 && abs(eta)>3.0 ) ;
    return jetid;
  }

  if(tight) {	
    jetid = (NHF<0.90 && NEMF<0.90 && NumConst>1) && ((abs(eta)<=2.4 && CHF>0 && CHM>0 && CEMF<0.99) || abs(eta)>2.4) && abs(eta)<=2.7 ;
    jetid = jetid or (NEMF<0.90 && NumNeutralParticle>2 && abs(eta)>2.7 && abs(eta)<=3.0 ) ;
    jetid = jetid or (NEMF<0.90 && NumNeutralParticle>10 && abs(eta)>3.0 ) ;
    return jetid;
  }

  return true;
}

//Count objects around another object within dR < deltaRcut
template<class a, class b> int jetAnalyser::countInCone(a center, b objectsToCount){

  int counter = 0;
  for(auto object = objectsToCount->begin(); object != objectsToCount->end(); ++object){
    if(reco::deltaR(*center, *object) < deltaRcut)
      ++counter;
  }

  return counter;
}

int jetAnalyser::getPileUp(edm::Handle<std::vector<PileupSummaryInfo>>& pupInfo){

  if(!pupInfo.isValid())
    return -1;

  auto PVI = pupInfo->begin();
  while(PVI->getBunchCrossing() != 0 && PVI != pupInfo->end())
    ++PVI;

  if(PVI != pupInfo->end())
    return PVI->getPU_NumInteractions();
  else
    return -1;
}

reco::GenParticleCollection::const_iterator jetAnalyser::getMatchedGenParticle(const reco::Jet *jet, edm::Handle<reco::GenParticleCollection>& genParticles){
  float deltaRmin = 999;
  auto matchedGenParticle = genParticles->end();
  for(auto genParticle = genParticles->begin(); genParticle != genParticles->end(); ++genParticle){
    if(!genParticle->isHardProcess())
      continue;
    // This status flag is exactly the pythia8 status-23 we need (i.e. the same as genParticles->status() == 23), probably also ok to use for other generators
    // Only consider udscb quarks and gluons
    if(abs(genParticle->pdgId()) > 5 && abs(genParticle->pdgId() != 21))
      continue;
    float thisDeltaR = reco::deltaR(*genParticle, *jet);
    if(thisDeltaR < deltaRmin && thisDeltaR < deltaRcut){
      deltaRmin = thisDeltaR;
      matchedGenParticle = genParticle;
    }
  }
  return matchedGenParticle;
}

DEFINE_FWK_MODULE(jetAnalyser);
