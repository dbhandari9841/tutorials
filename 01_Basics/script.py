
import ROOT
import numpy as np 

# Open the file
file = ROOT.TFile("/ceph/submit/data/group/cms/store/fccee/samples/winter2023/CLD_FullSim/wzp6_ee_mumuH_ecm240/mumuH_rec_16610_191.root")

# Get the tree of events
tree = file.Get("events")

# Create a histogram to store the energies
h = ROOT.TH1D("h", "Energy [GeV]", 150, 0, 180)

# for loop over the first 10 events, and print information about the MC particles
for i in range(10000):
    
    print("Processing event", i)
    tree.GetEntry(i)

    # get the MC particles for this event
    MCParticles = tree.MCParticles
    print("Number of MC particles:", len(MCParticles))

    menergetic_muon = None
    menergetic_antimuon = None  #this being outside the loop was very important, to prevent resetting...
    max_energy_mu = -2
    max_energy_antimu = -2

    # loop over all particles in the event
    for j in range(len(MCParticles)):

        # print their information
        #print("MC Particle", j)
        #print("Momentum (px, py, pz):", MCParticles[j].momentum.x, MCParticles[j].momentum.y, MCParticles[j].momentum.z)
        #print("Charge:", MCParticles[j].charge)
        #print("PDG ID:", MCParticles[j].PDG)

        

        if np.abs(MCParticles[j].PDG) == 13:
            momentum = MCParticles[j].momentum
            energy = (MCParticles[j].momentum.x**2 + MCParticles[j].momentum.y**2 + MCParticles[j].momentum.z**2 + MCParticles[j].mass**2)**0.5
            #print("Energy:", energy)

            if MCParticles[j].PDG == 13:  #for muon
                if energy > max_energy_mu:
                    max_energy_mu = energy
                    menergetic_muon = MCParticles[j]
            elif MCParticles[j].PDG == -13:  #for antimuon
                if energy > max_energy_antimu:
                    max_energy_antimu = energy
                    menergetic_antimuon = MCParticles[j]
#now, need to calculate the invariant mass for muon and antimuon,
#can each event have both muon and anti-muon...? perhaps not, so need to check if both are present

    if menergetic_muon and menergetic_antimuon:
        p1 = menergetic_muon.momentum
        p2 = menergetic_antimuon.momentum

        #M^2 = (E1 + E2)^2 - ||p1 + p2||^2  #this should be the invariant mass formula
        total_energy = max_energy_mu + max_energy_antimu
        total_px = p1.x + p2.x
        total_py = p1.y + p2.y
        total_pz = p1.z + p2.z
        invariant_mass = np.sqrt(total_energy**2 - (total_px**2 + total_py**2 + total_pz**2))

        #filling the histogram with the invariant mass
        h.Fill(invariant_mass)

        # if the particle has more than 10 GeV of energy, fill the histogram
        #if energy > 10:
            #h.Fill(energy)

# draw the histogram, this is done using a Canvas
c = ROOT.TCanvas()
c.SetLogy()
#h.GetXaxis().SetRangeUser(0, 180)
h.Draw()

# label the axes
h.GetXaxis().SetTitle("Invariant Mass (maybe in GeV/c*c)") #c^2 important for unit
h.GetYaxis().SetTitle("Number of particles")

# draw the canvas
c.Draw()

# save the plot to a file
c.SaveAs("Invariant Mass.png")

# save the histogram to a .root file
file_out = ROOT.TFile("output.root", "RECREATE")
h.Write()
file_out.Close()

print("All done!")
