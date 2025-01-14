#include "FCCAnalyses/MCParticle.h"
ROOT::VecOps::RVec<float> get_energy(const ROOT::VecOps::RVec<edm4hep::MCParticleData>& particles) {
    ROOT::VecOps::RVec<float> invariant_masses;

    // Vectors to store all muons and anti-muons
    std::vector<TLorentzVector> muons;
    std::vector<TLorentzVector> anti_muons;

    for (const auto& particle : particles) {
        // Check for muon or anti-muon
        if (std::abs(particle.PDG) == 13) {
            TLorentzVector tlv;
            tlv.SetXYZM(particle.momentum.x, particle.momentum.y, particle.momentum.z, particle.mass);

            if (particle.PDG == 13) {
                muons.push_back(tlv);  // Muon
            } else if (particle.PDG == -13) {
                anti_muons.push_back(tlv);  // Anti-muon
            }
        }
    }

    // Check if we have valid muons and anti-muons
    if (muons.empty() || anti_muons.empty()) {
        std::cerr << "No muon or anti-muon found in the event." << std::endl;
        return invariant_masses;
    }

    // Loop over all muon-anti-muon pairs
    for (const auto& muon : muons) {
        for (const auto& anti_muon : anti_muons) {
            // Combine the TLorentzVectors
            TLorentzVector combined = muon + anti_muon;

            // Ensure combined mass is physical (non-negative and plausible)
            float mass = combined.M();
            if (mass > 0 && mass < 200) {  // Use a reasonable upper bound (e.g., 200 GeV for Z boson mass region)
                invariant_masses.push_back(mass);
            } else {
                std::cerr << "Unphysical mass detected: " << mass << " GeV" << std::endl;
            }
        }
    }

    return invariant_masses;
}
