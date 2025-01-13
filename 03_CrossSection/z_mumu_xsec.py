
import ROOT
ROOT.TH1.SetDefaultSumw2(ROOT.kTRUE)

import numpy as np
frac = np.linspace(0.1, 1.0, 10)
for f in frac:
    # list of all guns
    processList = {
        'wzp6_ee_mumu_ecm91p2': {'fraction':f},
        'wzp6_ee_tautau_ecm91p2': {'fraction':f},
        'p8_ee_gaga_mumu_ecm91p2': {'fraction':f},
    }



    inputDir = "/ceph/submit/data/group/fcc/ee/generation/DelphesEvents/winter2023/IDEA/"
    procDict = "/ceph/submit/data/group/fcc/ee/generation/DelphesEvents/winter2023/IDEA/samplesDict.json"

    # additional/custom C++ functions
    includePaths = ["../functions/functions.h", "../functions/functions_gen.h"]


    # output directory
    outputDir   = "output/"


    # optional: ncpus, default is 4, -1 uses all cores available
    nCPUS       = 128

    # scale the histograms with the cross-section and integrated luminosity
    doScale = True
    intLumi = 100e6 # 44.84 pb-1 = LEP, 100e6=100 ab-1 = FCCee

# define histograms
    bins_p_mu = (200, 0, 200) # 1 GeV bins
    bins_m_ll = (200, 0, 200) # 1 GeV bins
    bins_p_ll = (200, 0, 200) # 1 GeV bins

    bins_theta = (500, -5, 5)
    bins_phi = (500, -5, 5)

    bins_count = (50, 0, 50)
    bins_pdgid = (60, -30, 30)
    bins_charge = (10, -5, 5)

    bins_cos = (100, -1, 1)
    bins_norm = (200, 0, 2)
    bins_nparticles = (200, 0, 200)
    bins_aco = (800,-4,4)

    def build_graph(df, dataset):

        hists = []

        df = df.Define("weight", "1.0")
        weightsum = df.Sum("weight")

        df = df.Alias("Particle0", "Particle#0.index")
        df = df.Alias("Particle1", "Particle#1.index")
        df = df.Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
        df = df.Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
        df = df.Alias("Muons", "Muon#0.index")

        # reco muons
        df = df.Define("muons_all", "FCCAnalyses::ReconstructedParticle::get(Muons, ReconstructedParticles)")
        df = df.Define("muons_all_p", "FCCAnalyses::ReconstructedParticle::get_p(muons_all)")
        df = df.Define("muons_all_theta", "FCCAnalyses::ReconstructedParticle::get_theta(muons_all)")
        df = df.Define("muons_all_costheta", "FCCAnalyses::get_costheta(muons_all)")
        df = df.Define("muons_all_phi", "FCCAnalyses::ReconstructedParticle::get_phi(muons_all)")
        df = df.Define("muons_all_q", "FCCAnalyses::ReconstructedParticle::get_charge(muons_all)")
        df = df.Define("muons_all_no", "FCCAnalyses::ReconstructedParticle::get_n(muons_all)")

        # define cos(theta) of the muons
        hists.append(df.Histo1D(("muons_all_costheta", "", *bins_cos), "muons_all_costheta"))
        df = df.Define("muons", "FCCAnalyses::sel_range(0, 0.97, true)(muons_all, muons_all_costheta)")
        df = df.Define("muons_p", "FCCAnalyses::ReconstructedParticle::get_p(muons)")
        df = df.Define("muons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(muons)")
        df = df.Define("muons_no", "FCCAnalyses::ReconstructedParticle::get_n(muons)")
        df = df.Define("muons_q", "FCCAnalyses::ReconstructedParticle::get_charge(muons)")


        #########
        ### CUT 0: all events
        #########
        df = df.Define("cut0", "0")
        hists.append(df.Histo1D(("cutFlow", "", *bins_count), "cut0"))

        #########
        ### CUT 1: select at least 1 muon
        #########
        df = df.Filter("muons_no >= 1")

        df = df.Define("cut1", "1")
        hists.append(df.Histo1D(("cutFlow", "", *bins_count), "cut1"))

        #########
        ### CUT 2: select at least 2 muons
        #########
        df = df.Filter("muons_no >= 2")

        df = df.Define("cut2", "2")
        hists.append(df.Histo1D(("cutFlow", "", *bins_count), "cut2"))


        #########
        ### CUT 3: require exactly 2 opposite-sign muons
        #########
        df = df.Filter("muons_no == 2 && (muons_q[0] + muons_q[1]) == 0")

        df = df.Define("cut3", "3")
        hists.append(df.Histo1D(("cutFlow", "", *bins_count), "cut3"))

        ######### so the cuts are sequentially applied, after the third cut, we have 2 muons
        ###We first define the momentum of the two muons separately
        #########
        df = df.Define("muon1_p", "muons_p[0]")  
        df = df.Define("muon2_p", "muons_p[1]") 

        ##hstograms for muon1_p and muon2_p
    
        hists.append(df.Histo1D(("muon1_p", "Muon 1 Momentum; Momentum [GeV]; Events", *bins_count), "muon1_p"))
        hists.append(df.Histo1D(("muon2_p", "Muon 2 Momentum; Momentum [GeV]; Events", *bins_count), "muon2_p"))


        #########
        ### CUT 4: max normalized muon momentum > 0.6
        #########
        df = df.Define("muon_max_p", "(muons_p[0] > muons_p[1]) ? muons_p[0] : muons_p[1]")
        df = df.Define("muon_max_p_norm", "muon_max_p/45.6")
        hists.append(df.Histo1D(("muon_max_p_norm", "", *bins_norm), "muon_max_p_norm"))
        df = df.Filter("muon_max_p_norm > 0.6")

        df = df.Define("cut4", "4")
        hists.append(df.Histo1D(("cutFlow", "", *bins_count), "cut4"))


        ############################################################################
        # acolinearity between 2 muons
        df = df.Define("acolinearity", "FCCAnalyses::acolinearity(muons)")
        hists.append(df.Histo1D(("acolinearity", "", *bins_aco), "acolinearity"))

        # plot invariant mass of both muons
        df = df.Define("leps_tlv", "FCCAnalyses::makeLorentzVectors(muons)")
        df = df.Define("invariant_mass", "(leps_tlv[0]+leps_tlv[1]).M()")
        hists.append(df.Histo1D(("invariant_mass", "", *bins_m_ll), "invariant_mass"))



        return hists, weightsum
