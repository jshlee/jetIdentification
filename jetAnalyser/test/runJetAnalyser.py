import FWCore.ParameterSet.Config as cms
process = cms.Process("jetAnalyser")

# Settings for local tests
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.source = cms.Source("PoolSource", 
    fileNames = cms.untracked.vstring('file:/pnfs/user/mc/RunIISummer16DR80Premix/QCD_Pt-15to7000_TuneCUETP8M1_FlatP6_13TeV_pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/110000/00D5AF84-33B7-E611-8E07-D067E5F91B8A.root')
)

# Standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.Geometry.GeometryRecoDB_cff") 
process.GlobalTag.globaltag = '80X_mcRun2_asymptotic_2016_TrancheIV_v8'
process.load('JetMETCorrections.Configuration.DefaultJEC_cff')

# Use TFileService to put trees from different analyzers in one file
process.TFileService = cms.Service("TFileService", 
    fileName = cms.string("jet.root"),
    closeFileFast = cms.untracked.bool(True)
)

process.jetAnalyser = cms.EDAnalyzer("jetAnalyser",
    rhoInputTag			= cms.InputTag('fixedGridRhoFastjetAll'),
    vertexInputTag		= cms.InputTag('offlinePrimaryVerticesWithBS'),
    jetsInputTag		= cms.InputTag('ak4PFJetsCHS'),
    pfCandidatesInputTag	= cms.InputTag('particleFlow'),
    genJetsInputTag		= cms.InputTag('ak4GenJets'),
    jec				= cms.string('ak4PFCHSL1FastL2L3'),
    genParticlesInputTag	= cms.InputTag('genParticles'),
    csvInputTag			= cms.InputTag('pfCombinedInclusiveSecondaryVertexV2BJetTags'),
    minJetPt			= cms.untracked.double(20.),
    deltaRcut			= cms.untracked.double(0.3),
)

process.p = cms.Path(process.jetAnalyser)
