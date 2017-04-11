import FWCore.ParameterSet.Config as cms
process = cms.Process("jetAnalyser")

# Settings for local tests
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.source = cms.Source("PoolSource", 
    fileNames = cms.untracked.vstring('file:/pnfs/user/mc/RunIISummer16DR80Premix/QCD_Pt-15to7000_TuneCUETP8M1_FlatP6_13TeV_pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/110000/00D5AF84-33B7-E611-8E07-D067E5F91B8A.root','file:/pnfs/user/mc/RunIISummer16DR80Premix/QCD_Pt-15to7000_TuneCUETP8M1_FlatP6_13TeV_pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/110000/020A1BBC-DCB6-E611-B1DB-B083FECFC6ED.root','file:/pnfs/user/mc/RunIISummer16DR80Premix/QCD_Pt-15to7000_TuneCUETP8M1_FlatP6_13TeV_pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/110000/02BFF584-C5B6-E611-ABAB-0025905B85B2.root','file:/pnfs/user/mc/RunIISummer16DR80Premix/QCD_Pt-15to7000_TuneCUETP8M1_FlatP6_13TeV_pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/110000/02FD5FEA-94B6-E611-9625-0242AC130002.root','file:/pnfs/user/mc/RunIISummer16DR80Premix/QCD_Pt-15to7000_TuneCUETP8M1_FlatP6_13TeV_pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/110000/043DCA80-C0B6-E611-A570-001E67E95A8A.root','file:/pnfs/user/mc/RunIISummer16DR80Premix/QCD_Pt-15to7000_TuneCUETP8M1_FlatP6_13TeV_pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/110000/06D2E19A-8EB6-E611-9ABE-5065F3820351.root','file:/pnfs/user/mc/RunIISummer16DR80Premix/QCD_Pt-15to7000_TuneCUETP8M1_FlatP6_13TeV_pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/110000/08E920C2-78B6-E611-BEE1-02163E012F5F.root','file:/pnfs/user/mc/RunIISummer16DR80Premix/QCD_Pt-15to7000_TuneCUETP8M1_FlatP6_13TeV_pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/110000/0A780905-DFB6-E611-8732-0242AC130003.root','file:/pnfs/user/mc/RunIISummer16DR80Premix/QCD_Pt-15to7000_TuneCUETP8M1_FlatP6_13TeV_pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/110000/0A899D02-7EB6-E611-89C7-14187763B750.root','file:/pnfs/user/mc/RunIISummer16DR80Premix/QCD_Pt-15to7000_TuneCUETP8M1_FlatP6_13TeV_pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/110000/0AD916AB-7FB6-E611-99D6-20CF307C9944.root','file:/pnfs/user/mc/RunIISummer16DR80Premix/QCD_Pt-15to7000_TuneCUETP8M1_FlatP6_13TeV_pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/110000/0E6DB0AB-7AB6-E611-86AD-B083FED03632.root','file:/pnfs/user/mc/RunIISummer16DR80Premix/QCD_Pt-15to7000_TuneCUETP8M1_FlatP6_13TeV_pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/110000/127D7979-98B6-E611-AEFE-00259048B754.root','file:/pnfs/user/mc/RunIISummer16DR80Premix/QCD_Pt-15to7000_TuneCUETP8M1_FlatP6_13TeV_pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/110000/182396EA-DBB6-E611-822B-0CC47A78A2F6.root','file:/pnfs/user/mc/RunIISummer16DR80Premix/QCD_Pt-15to7000_TuneCUETP8M1_FlatP6_13TeV_pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/110000/182D6200-C8B6-E611-B62E-0025905B8580.root','file:/pnfs/user/mc/RunIISummer16DR80Premix/QCD_Pt-15to7000_TuneCUETP8M1_FlatP6_13TeV_pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/110000/186DF439-DFB6-E611-9922-02163E013ADF.root')
)

# Standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.Geometry.GeometryRecoDB_cff") 
process.GlobalTag.globaltag = '80X_mcRun2_asymptotic_2016_TrancheIV_v8'
process.load('JetMETCorrections.Configuration.DefaultJEC_cff')

process.load('RecoJets.JetProducers.QGTagger_cfi')
process.QGTagger.srcJets          = cms.InputTag('ak4PFJetsCHS')      # Could be reco::PFJetCollection or pat::JetCollection (both AOD and miniAOD)
process.QGTagger.jetsLabel        = cms.string('QGL_AK4PFchs')        # Other options: see https://twiki.cern.ch/twiki/bin/viewauth/CMS/QGDataBaseVersion
#process.QGTagger.jec              = cms.string('ak4PFCHSL1FastL2L3')  # Provide the jet correction service if your jets are uncorrected, otherwise keep empty

# Use TFileService to put trees from different analyzers in one file
process.TFileService = cms.Service("TFileService", 
    fileName = cms.string("jetall.root"),
    closeFileFast = cms.untracked.bool(True)
)

process.jetAnalyser = cms.EDAnalyzer("jetAnalyser",
    rhoInputTag			= cms.InputTag('fixedGridRhoFastjetAll'),
    vertexInputTag		= cms.InputTag('offlinePrimaryVerticesWithBS'),
    jetsInputTag		= cms.InputTag('ak4PFJetsCHS'),
    pfCandidatesInputTag= cms.InputTag('particleFlow'),
    genJetsInputTag		= cms.InputTag('ak4GenJets'),
    jec			    	= cms.string('ak4PFCHSL1FastL2L3'),
    genParticlesInputTag= cms.InputTag('genParticles'),
    csvInputTag			= cms.InputTag('pfCombinedInclusiveSecondaryVertexV2BJetTags'),
    minJetPt			= cms.untracked.double(20.),
    deltaRcut			= cms.untracked.double(0.4),
    qgInputTag			= cms.InputTag('QGTagger','qgLikelihood'),
)

process.ak8PFCHSL1FastL2L3 = process.ak8PFL2L3.clone()
process.ak8PFCHSL1FastL2L3.correctors.insert(0,'ak8PFCHSL1Fastjet')

process.fatJetAnalyser = process.jetAnalyser.clone()
process.fatJetAnalyser.jetsInputTag    = cms.InputTag('ak8PFJetsCHS')
process.fatJetAnalyser.genJetsInputTag = cms.InputTag('ak8GenJets')
process.fatJetAnalyser.jec             = cms.string('ak8PFCHSL1FastL2L3')
process.fatJetAnalyser.deltaRcut	   = cms.untracked.double(0.8)
process.fatJetAnalyser.csvInputTag	   = cms.InputTag('')
process.fatJetAnalyser.qgInputTag 	   = cms.InputTag('')

process.p = cms.Path(process.QGTagger+process.jetAnalyser+process.fatJetAnalyser)
