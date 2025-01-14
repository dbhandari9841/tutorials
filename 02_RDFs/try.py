import ROOT
ROOT.EnableImplicitMT(1)
ROOT.gInterpreter.ProcessLine("""#include "energygrabber.h" """)  #cheating a bit here...


# Open the file
f = ROOT.TFile.Open("/ceph/submit/data/group/cms/store/fccee/samples/winter2023/CLD_FullSim/wzp6_ee_mumuH_ecm240/mumuH_rec_16610_191.root")

# Get the tree
tree = f.Get("events")

# Create the RDF
df = ROOT.RDataFrame(tree)

# Define the energy of the particles, and save if above 10 GeV
df = df.Define("Energy", "get_energy(MCParticles)")

# Fill the histogram with the calculated energies
# We defined 100 bins between 0 and 1000 GeV
h = df.Histo1D(("Invariant Mass", "", *(180, 0, 180)), "Energy")

# Draw the histogram
c = ROOT.TCanvas()
h.Draw()
c.Draw()
c.SetLogy()
h.GetXaxis().SetTitle("Energy")
h.GetYaxis().SetTitle("no. of events")

# save the histogram
c.SaveAs("Invariant Mass.png")
