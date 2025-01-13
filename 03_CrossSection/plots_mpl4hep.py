import uproot
#import hist
import matplotlib.pyplot as plt
import mplhep as hep 

hep.style.use("CMS")
plt.style.use(hep.style.CMS)


def plot_invariant_mass():
    fig = plt.figure()
    ax = fig.subplots()

    hists = []
    for i,proc in enumerate(procs):
        file = uproot.open(f"output/{proc}.root")
        #print(file.keys())
        h = file["invariant_mass"]
        h = h.to_hist()
        #print(h)
        hists.append(h)


    hep.histplot(
        hists,
        stack=True,
        histtype="fill",
        color=["#7FBF7F", "#7F7FFF", "w"],
        edgecolor=["k", "k", "r"],
        linewidth=1,
        label=labels,
        ax=ax,
    )

    ax.set_ylabel("Events")
    ax.set_xlim([0, 120])
    ax.legend(loc='upper left', fontsize='x-small')
    ax.set_yscale("log")
    ax.set_xlabel("Invariant mass (GeV)")

    hep.label.exp_label(exp="FCC-ee", ax=ax, data=False, rlabel="100 $\mathrm{ab^{-1}}$ (91.2 GeV)")

    fig.savefig(f"{outDir}/invariant_mass_mpl4hep.png", bbox_inches="tight")
    fig.savefig(f"{outDir}/invariant_mass_mpl4hep.pdf", bbox_inches="tight")


def plot_cutflow():
    fig = plt.figure()
    ax = fig.subplots()

    cut_names = ["All events", "$\geq 1 \mu$", "$\geq 2 \mu^\pm$", "$2~\\text{OS}~\mu$", "$\\text{p}_\mu^{\\text{max}} > 0.6~\\text{p}_{\\text{beam}}$"]

    hists = []
    for i,proc in enumerate(procs):
        file = uproot.open(f"output/{proc}.root")
        #print(file.keys())
        h = file["cutFlow"]
        h = h.to_hist()
        #print(h)
        hists.append(h)


    hep.histplot(
        hists,
        stack=True,
        histtype="fill",
        color=["#7FBF7F", "#7F7FFF", "w"],
        edgecolor=["k", "k", "r"],
        linewidth=1,
        label=labels,
        ax=ax,
    )

    ax.set_xticks(range(len(cut_names)))
    ax.set_xticklabels(cut_names, rotation=45, ha="left", fontsize=15)
    ax.set_ylabel("Events")
    ax.set_xlim([0, len(cut_names)])
    ax.legend(loc='upper left', fontsize='x-small')
    ax.set_yscale("log")
    ax.set_xlabel("")
    ax.margins(y=0.25)

    hep.label.exp_label(exp="FCC-ee", ax=ax, data=False, rlabel="100 $\mathrm{ab^{-1}}$ (91.2 GeV)")

    fig.savefig(f"{outDir}/cutFlow_mpl4hep.png", bbox_inches="tight")
    fig.savefig(f"{outDir}/cutFlow_mpl4hep.pdf", bbox_inches="tight")


if __name__ == "__main__":

    outDir = "/home/submit/dipeshb/fcc-ee/tutorials/03_CrossSection/z_mumu_xsec/"
    procs = ["p8_ee_gaga_mumu_ecm91p2", "wzp6_ee_tautau_ecm91p2", "wzp6_ee_mumu_ecm91p2"]
    labels = ["$e^+e^-\\to e^+e^-qq$", "$e^+e^-\\to\\tau^+\\tau^-$", "$e^+e^-\\to\mu^+\mu^-$"]

    plot_invariant_mass()
    plot_cutflow()
