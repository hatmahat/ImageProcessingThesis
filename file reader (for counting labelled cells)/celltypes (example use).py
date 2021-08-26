import celltypes as ct

count = ct.countTypes(r"D:\White Blood Cells  RSUP Sardjito - Copy", "sampel 1 (clean)")
count.read_file_names()
count.count_cells()

cells = count.get_uniq_dict()
binary = count.get_blast_vs_nonblast()
print("Cell types:", cells)
print("Binary type:", binary)
print("Total cells:", binary['Limfoblas']+binary['Non-Limfoblas'])
print("Labelled img:", len(count.get_preprocessed()))