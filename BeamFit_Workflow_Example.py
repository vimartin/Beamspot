import FWCore.ParameterSet.Config as cms

process = cms.Process("BSworkflow")
# initialize MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.load("RecoVertex.BeamSpotProducer.d0_phi_analyzer_cff")

#FNAL location /pnfs/cms/WAX/11
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        'root://xrootd.unl.edu//store/relval/CMSSW_7_0_0/RelValMinBias_13/ALCARECO/TkAlMinBias-START70_V6_BS-v1/00000/92B54648-6FA2-E311-B987-02163E00E5B0.root'
        )
    )

#process.MessageLogger = cms.Service("MessageLogger",
#    threshold = cms.untracked.string('INFO')
#)

process.MessageLogger.cerr.FwkReport  = cms.untracked.PSet(
    reportEvery = cms.untracked.int32(1000000),
)

#process.source = cms.Source('PoolSource',
#                            debugVerbosity = cms.untracked.uint32(0),
#                            debugFlag = cms.untracked.bool(False)
#                            )

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(10000) #1500
)

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)
    )

# this is for filtering on L1 technical trigger bit
process.load('L1TriggerConfig.L1GtConfigProducers.L1GtTriggerMaskTechTrigConfig_cff')
process.load('HLTrigger/HLTfilters/hltLevel1GTSeed_cfi')
process.hltLevel1GTSeed.L1TechTriggerSeeding = cms.bool(True)
process.hltLevel1GTSeed.L1SeedsLogicalExpression = cms.string('0 AND ( 40 OR 41 ) AND NOT (36 OR 37 OR 38 OR 39)')
##

## reco PV
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = 'PRE_CSA14_V1::All'
#process.load("Configuration.StandardSequences.Geometry_cff")

process.load("Configuration.StandardSequences.Reconstruction_cff")
process.load("RecoVertex.BeamSpotProducer.BeamSpot_cfi")
process.load("RecoVertex.PrimaryVertexProducer.OfflinePrimaryVertices_cfi")
process.offlinePrimaryVertices.TrackLabel = cms.InputTag("ALCARECOTkAlMinBias")
#process.offlinePrimaryVertices.TrackLabel = cms.InputTag("generalTracks") 

#### remove beam scraping events
process.noScraping= cms.EDFilter("FilterOutScraping",
                                 applyfilter = cms.untracked.bool(True),
                                 debugOn = cms.untracked.bool(False), ## Or 'True' to get some per-event info
                                 numtrack = cms.untracked.uint32(10),
                                 thresh = cms.untracked.double(0.20)
    )

process.p = cms.Path(
#                     process.hltLevel1GTSeed +
#                     process.offlineBeamSpot +
#                     process.offlinePrimaryVertices+
#                     process.noScraping +
                     process.d0_phi_analyzer)

process.MessageLogger.debugModules = ['BeamSpotAnalyzer']

################### Primary Vertex
#process.offlinePrimaryVertices.PVSelParameters.maxDistanceToBeam = 2
#process.offlinePrimaryVertices.TkFilterParameters.maxNormalizedChi2 = 20
#process.offlinePrimaryVertices.TkFilterParameters.minSiliconLayersWithHits = 5
#process.offlinePrimaryVertices.TkFilterParameters.maxD0Significance = 100
#process.offlinePrimaryVertices.TkFilterParameters.minPixelLayersWithHits = 1
#process.offlinePrimaryVertices.TkClusParameters.TkGapClusParameters.zSeparation = 1

#######################
#process.d0_phi_analyzer.BeamFitter.TrackCollection = 'generalTracks'
process.d0_phi_analyzer.BeamFitter.TrackCollection = 'ALCARECOTkAlMinBias'
process.d0_phi_analyzer.BeamFitter.MinimumTotalLayers = 6
process.d0_phi_analyzer.BeamFitter.MinimumPixelLayers = 2
process.d0_phi_analyzer.BeamFitter.MaximumNormChi2 = 10
process.d0_phi_analyzer.BeamFitter.MinimumInputTracks = 50
process.d0_phi_analyzer.BeamFitter.MinimumPt = 0.7
process.d0_phi_analyzer.BeamFitter.MaximumImpactParameter = 1.0
process.d0_phi_analyzer.BeamFitter.TrackAlgorithm =  cms.untracked.vstring()
process.d0_phi_analyzer.BeamFitter.Debug = True

process.d0_phi_analyzer.PVFitter.Apply3DFit = True
process.d0_phi_analyzer.PVFitter.minNrVerticesForFit = 10 
#########################

process.d0_phi_analyzer.BeamFitter.AsciiFileName = 'BeamFit_RunBased_Workflow_CSA14.txt'
process.d0_phi_analyzer.BeamFitter.AppendRunToFileName = False
process.d0_phi_analyzer.BeamFitter.OutputFileName = '/uscms/home/vimartin/nobackup/beamspot_START50_V13_Realistic8TeVCollision/BeamFit_RunBased_Workflow_PVrefit.root' 
process.d0_phi_analyzer.BeamFitter.SaveNtuple = False
process.d0_phi_analyzer.BeamFitter.SavePVVertices = False
process.d0_phi_analyzer.BeamFitter.SaveFitResults = False

# fit as function of lumi sections
process.d0_phi_analyzer.BSAnalyzerParameters.fitEveryNLumi = -1
process.d0_phi_analyzer.BSAnalyzerParameters.resetEveryNLumi = -1
