
import uproot
import numpy as np
import argparse
import matplotlib.pyplot as plt

def get_hist(proc, hName, processList, norm=False, lumi=150e6):
    fraction = processList[proc]["fraction"]
    with uproot.open(f"output/{proc}.root") as f:
        hist = f[hName].to_numpy() # tuple (hist vals, hist edges)
        xsec = f["crossSection"].value
        nevents = f["eventsProcessed"].value
        if norm:
            scale_factor = fraction*lumi * xsec / nevents
            hist = (hist[0] * scale_factor, hist[1])
    return hist, xsec, nevents

def yields():
    procs = ["wzp6_ee_mumu_ecm91p2", "wzp6_ee_tautau_ecm91p2", "p8_ee_gaga_mumu_ecm91p2"]
    luminosity = 100e6 # LEP=44.84, FCC=100e6

    print(f"Integrated luminosity used: {luminosity} pb-1\n")
    for proc in procs:
        hist, xsec, nevents = get_hist(proc, "cutFlow")
        hist_scaled, xsec, nevents = get_hist(proc, "cutFlow", norm=True, lumi=luminosity)
        yields = hist[0][4]
        yields_scaled = hist_scaled[0][4]
        print(f"Process {proc} xsec={xsec:.2f} pb, nevents={nevents}")
        print(f"   Bare yields: {yields:.2f}")
        print(f"   Normalized yields: {yields_scaled:.2f}")


def acceptance():
    acceptances = []
    proc = "wzp6_ee_mumu_ecm91p2"
    frac = np.linspace(0.1, 1.0, 100)
    for f in frac:
        processList = {
            'wzp6_ee_mumu_ecm91p2': {'fraction': f},
            'wzp6_ee_tautau_ecm91p2': {'fraction': f},
            'p8_ee_gaga_mumu_ecm91p2': {'fraction': f},
        }
        hist, xsec, nevents = get_hist(proc, "cutFlow", processList, norm=True)
        n_tot = hist[0][0] # events before any cut
        n_sel = hist[0][4] # events after all cuts
        acc = n_sel / n_tot
        acceptances.append(acc)
        print(f"Acceptance for {proc} = {acc:.03f}")

    # Plot acceptance as a function of fraction
    plt.figure()
    plt.plot(frac, acceptances, marker="o", linestyle="-", color="blue", label="Acceptance")
    plt.xlabel("Fraction")
    plt.ylabel("Acceptance")
    plt.title(f"Acceptance vs. Fraction for {proc}")
    plt.grid()
    plt.legend()
    output_file = f"acceptance_vs_fraction_{proc}.png"
    plt.savefig(output_file, dpi=300, bbox_inches="tight")




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--yields", action="store_true", help="Calculate event yields")
    parser.add_argument("--acceptance", action="store_true", help="Calculate acceptance")
    args = parser.parse_args()

    if args.yields:
        yields()
    elif args.acceptance:
        acceptance()
