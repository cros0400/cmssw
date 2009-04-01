import FWCore.ParameterSet.Config as cms

process = cms.Process("PROD")

process.load("SimGeneral.HepPDTESSource.pdt_cfi")

process.load("SimG4CMS.HcalTestBeam.TB2006Geometry77XML_cfi")

process.load("Configuration.EventContent.EventContent_cff")

process.load("SimG4Core.Application.g4SimHits_cfi")

process.TFileService = cms.Service("TFileService",
    fileName = cms.string('hcaltb06_77.root')
)

process.MessageLogger = cms.Service("MessageLogger",
    destinations = cms.untracked.vstring('cout'),
    categories = cms.untracked.vstring('CaloSim', 
        'HCalGeom', 
        'HcalSim', 
        'HcalTBSim', 
        'SimHCalData'),
    cout = cms.untracked.PSet(
        threshold = cms.untracked.string('INFO'),
        INFO = cms.untracked.PSet(
            limit = cms.untracked.int32(-1)
        ),
        DEBUG = cms.untracked.PSet(
            limit = cms.untracked.int32(0)
        ),
        CaloSim = cms.untracked.PSet(
            limit = cms.untracked.int32(0)
        ),
        HCalGeom = cms.untracked.PSet(
            limit = cms.untracked.int32(0)
        ),
        HcalSim = cms.untracked.PSet(
            limit = cms.untracked.int32(0)
        ),
        HcalTBSim = cms.untracked.PSet(
            limit = cms.untracked.int32(0)
        ),
        SimHCalData = cms.untracked.PSet(
            limit = cms.untracked.int32(0)
        )
    )
)

process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
    moduleSeeds = cms.PSet(
        generator = cms.untracked.uint32(456789),
        g4SimHits = cms.untracked.uint32(9876),
        VtxSmeared = cms.untracked.uint32(123456789)
    ),
    sourceSeed = cms.untracked.uint32(135799753)
)

process.common_beam_direction_parameters = cms.PSet(
    MinEta       = cms.double(0.5655),
    MaxEta       = cms.double(0.5655),
    MinPhi       = cms.double(0.15708),
    MaxPhi       = cms.double(0.15708),
    BeamPosition = cms.double(-800.0)
)

process.source = cms.Source("EmptySource")

process.generator = cms.EDProducer("FlatRandomEGunProducer",
    PGunParameters = cms.PSet(
        process.common_beam_direction_parameters,
        MinE   = cms.double(49.99),
        MaxE   = cms.double(50.01),
        PartID = cms.vint32(211)
    ),
    Verbosity       = cms.untracked.int32(0),
    AddAntiParticle = cms.bool(False),
    firstRun        = cms.untracked.uint32(1)
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(100)
)

process.o1 = cms.OutputModule("PoolOutputModule",
    process.FEVTSIMEventContent,
    fileName = cms.untracked.string('sim2006_77.root')
)

process.common_heavy_suppression1 = cms.PSet(
    NeutronThreshold = cms.double(30.0),
    ProtonThreshold = cms.double(30.0),
    IonThreshold = cms.double(30.0)
)

process.Timing = cms.Service("Timing")

from IOMC.EventVertexGenerators.VtxSmearedParameters_cfi import *
process.VtxSmeared = cms.EDFilter("BeamProfileVtxGenerator",
    process.common_beam_direction_parameters,
    VtxSmearedCommon,
    BeamMeanX       = cms.double(0.0),
    BeamMeanY       = cms.double(0.0),
    BeamSigmaX      = cms.double(0.0001),
    BeamSigmaY      = cms.double(0.0001),
    GaussianProfile = cms.bool(False),
    BinX            = cms.int32(50),
    BinY            = cms.int32(50),
    File            = cms.string('beam.profile'),
    UseFile         = cms.bool(False),
    TimeOffset      = cms.double(0.)
)

process.p1 = cms.Path(process.generator*process.VtxSmeared*process.g4SimHits)
process.outpath = cms.EndPath(process.o1)
process.common_maximum_timex = cms.PSet(
    MaxTrackTime  = cms.double(1000.0),
    MaxTimeNames  = cms.vstring(),
    MaxTrackTimes = cms.vdouble()
)
process.g4SimHits.NonBeamEvent = True
process.g4SimHits.UseMagneticField = False
process.g4SimHits.Physics.type = 'SimG4Core/Physics/QGSP_BERT_EMV'
process.g4SimHits.ECalSD.UseBirkLaw = False
process.g4SimHits.ECalSD.BirkC1 = 0.0046
process.g4SimHits.ECalSD.BirkC2 = 0.0
process.g4SimHits.ECalSD.SlopeLightYield = 0.02
process.g4SimHits.HCalSD.UseBirkLaw = False
process.g4SimHits.HCalSD.BirkC1 = 0.013
process.g4SimHits.HCalSD.BirkC2 = '9.6e-6'
process.g4SimHits.HCalSD.UseShowerLibrary = False
process.g4SimHits.HCalSD.TestNumberingScheme = True
process.g4SimHits.HCalSD.UseHF = False
process.g4SimHits.HCalSD.ForTBH2 = True
process.g4SimHits.StackingAction = cms.PSet(
    process.common_heavy_suppression1,
    process.common_maximum_timex,
    TrackNeutrino = cms.bool(False),
    KillHeavy     = cms.bool(False),
    SaveFirstLevelSecondary = cms.untracked.bool(False),
    SavePrimaryDecayProductsAndConversionsInTracker = cms.untracked.bool(True),
    SavePrimaryDecayProductsAndConversionsInCalo = cms.untracked.bool(False),
    SavePrimaryDecayProductsAndConversionsInMuon = cms.untracked.bool(False)
)
process.g4SimHits.SteppingAction = cms.PSet(
    process.common_maximum_timex,
    KillBeamPipe            = cms.bool(True),
    CriticalEnergyForVacuum = cms.double(2.0),
    CriticalDensity         = cms.double(1e-15),
    EkinNames               = cms.vstring(),
    EkinThresholds          = cms.vdouble(),
    EkinParticles           = cms.vstring(),
    Verbosity = cms.untracked.int32(0)
)
process.g4SimHits.CaloSD = cms.PSet(
    process.common_beam_direction_parameters,
    process.common_heavy_suppression1,
    EminTrack      = cms.double(1.0),
    TmaxHit        = cms.double(1000.0),
    EminHits       = cms.vdouble(0.0),
    TmaxHits       = cms.vdouble(1000.0),
    HCNames        = cms.vstring('HcalHits'),
    SuppressHeavy  = cms.bool(False),
    CheckHits      = cms.untracked.int32(25),
    UseMap         = cms.untracked.bool(True),
    Verbosity      = cms.untracked.int32(0),
    DetailedTiming = cms.untracked.bool(False),
    CorrectTOFBeam = cms.bool(False)
)
process.g4SimHits.CaloTrkProcessing.TestBeam = True
process.g4SimHits.Watchers = cms.VPSet(cms.PSet(
    HcalTB06Analysis = cms.PSet(
        process.common_beam_direction_parameters,
        Names    = cms.vstring('HcalHits', 'EcalHitsEB'),
        EHCalMax = cms.untracked.double(2.0),
        ETtotMax = cms.untracked.double(20.0),
        Verbose  = cms.untracked.bool(True)
    ),
    type = cms.string('HcalTB06Analysis')
))


