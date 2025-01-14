h1D = hist.Hist.new.Reg(100, 0, 200, name="momentum", label="$p$ [GeV]").Weight()
h2D = hist.Hist.new.Reg(100, 0, 200, name="momentum", label="$p$ [GeV]").Reg(100, 0, 6.28, name="phi", label="$\phi$").Weight()
