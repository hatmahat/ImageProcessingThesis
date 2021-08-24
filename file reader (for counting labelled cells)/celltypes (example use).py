import celltypes as ct

count = ct.countTypes(r"D:\White Blood Cells  RSUP Sardjito - Copy", "sampel 1 (checked1) - Copy")
count.read_file_names()
count.count_cells()

cells = count.get_uniq_dict()
binary = count.get_blast_vs_nonblast()
print(cells)
print(binary)