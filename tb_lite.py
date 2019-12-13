print("Hello from tb_lite")

def pytorch_structure(model):
  size_tot=0
  for name, param in model.named_parameters():
    dims=list(param.size())
    size=np.prod(dims)
    print(f"{size:10,d} : {name:50s} = {dims}")
    size_tot+=size
  print(f"{size_tot:10,d} : TOTAL")

