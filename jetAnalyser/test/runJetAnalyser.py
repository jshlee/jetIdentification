import FWCore.ParameterSet.Config as cms

# The top level of a configuration program is a Process object.

process = cms.Process("jetAnalyser")

# Settings for local tests
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))

from utils import get_vstring

num_root_file = 100 
fnames = get_vstring(num_files=num_root_file)

process.source = cms.Source("PoolSource", 
    fileNames = cms.untracked.vstring(*fnames)
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

outfname = 'jet_pythia_%d.root' % num_root_file

process.TFileService = cms.Service("TFileService", 
    fileName = cms.string(outfname),
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
