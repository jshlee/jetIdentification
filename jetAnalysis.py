# import ROOT in batch mode
import sys
oldargv = sys.argv[:]
sys.argv = [ '-b-' ]
import ROOT
ROOT.gROOT.SetBatch(True)
sys.argv = oldargv

# load FWLite C++ libraries
ROOT.gSystem.Load("libFWCoreFWLite.so");
ROOT.gSystem.Load("libDataFormatsFWLite.so");
ROOT.FWLiteEnabler.enable()

# load FWlite python libraries
from DataFormats.FWLite import Handle, Events

jets, jetLabel = Handle("std::vector<pat::Jet>"), "slimmedJets"

# open file
events = Events("/cms/scratch/jlee/TT_TuneCUETP8M1_13TeV-powheg-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14_ext3-v1/0064B539-803A-E611-BDEA-002590D0B060.root")

for iev,event in enumerate(events):
    event.getByLabel(jetLabel, jets)
    print "\nEvent %d: run %6d, lumi %4d, event %12d" % (iev,event.eventAuxiliary().run(), event.eventAuxiliary().luminosityBlock(),event.eventAuxiliary().event())
    #https://github.com/cms-sw/cmssw/blob/CMSSW_8_0_X/DataFormats/PatCandidates/interface/Jet.h
    for i,jet in enumerate(jets.product()):
        print "jet %3d: pt %5.1f, eta %+4.2f, mass %5.1f, partonFlavour %3d" % (
            i, jet.pt(), jet.eta(), jet.mass(), jet.partonFlavour())

#        print "jet.bDiscriminator()", jet.bDiscriminator()
        print "jet.chargedHadronEnergyFraction()", jet.chargedHadronEnergyFraction(),
        print "jet.neutralHadronEnergyFraction()", jet.neutralHadronEnergyFraction(),
        print "jet.chargedEmEnergyFraction()", jet.chargedEmEnergyFraction(),
        print "jet.neutralEmEnergyFraction()", jet.neutralEmEnergyFraction()
        
        print "jet.photonEnergyFraction()", jet.photonEnergyFraction(),
        print "jet.electronEnergyFraction()", jet.electronEnergyFraction(),
        print "jet.muonEnergyFraction()", jet.muonEnergyFraction(),
        print "jet.HFHadronEnergyFraction()", jet.HFHadronEnergyFraction()

        for d in range(jet.numberOfDaughters()):
            # https://github.com/cms-sw/cmssw/blob/CMSSW_8_0_X/DataFormats/PatCandidates/interface/PackedCandidate.h
            dau = jet.daughter(d)
            print "daughter: pt %5.1f, eta %+4.2f, phi %+4.2f, pdgId %3d" % (dau.pt(), dau.eta(), dau.phi(), dau.pdgId())
            

