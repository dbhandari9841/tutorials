import uproot

# open a .root file containing histograms
file = uproot.open("output.root")

# print the contents of the file
print(file.keys())

# read in the histogram
h = file["h"]

# this shold be a TH1D object, since we created it with ROOT
print(h)


import hist

# let's convert the uproot obeject it to hist histogram
h = h.to_hist()

# print the hist object
print(h)