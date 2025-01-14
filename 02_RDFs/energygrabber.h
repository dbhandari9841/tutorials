#include "FCCAnalyses/MCParticle.h"

ROOT::VecOps::RVec<float> get_energy(const ROOT::VecOps::RVec<edm4hep::MCParticleData>& particles) {
    ROOT::VecOps::RVec<float> invariant_masses;

    //to track the most energetic muon and anti-muon
    TLorentzVector mostEnergeticMuon, mostEnergeticAntiMuon;
    float maxEnergyMuon = -1.0, maxEnergyAntiMuon = -1.0;

    for (const auto& particle : particles) {
        //see if the particle is a muon or anti-muon
        if (std::abs(particle.PDG) == 13) {
            //TLorentzVector for the particle
            TLorentzVector tlv;
            tlv.SetXYZM(particle.momentum.x, particle.momentum.y, particle.momentum.z, particle.mass);

            //energy
            float energy = tlv.E();

            //upate the most energetic muon or anti-muon
            if (particle.PDG == 13 && energy > maxEnergyMuon) {
                maxEnergyMuon = energy;
                mostEnergeticMuon = tlv;
            } else if (particle.PDG == -13 && energy > maxEnergyAntiMuon) {
                maxEnergyAntiMuon = energy;
                mostEnergeticAntiMuon = tlv;
            }
        }
    }

    //invariant mass if both muon and anti-muon are present
    if (maxEnergyMuon > 0 && maxEnergyAntiMuon > 0) {
        TLorentzVector combined = mostEnergeticMuon + mostEnergeticAntiMuon;
        invariant_masses.push_back(combined.M());
    }
//we did energy energy energy, but in reality the final entry of the 4lorentz vector is mass
    return invariant_masses;
}
