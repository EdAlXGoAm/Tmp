import os
from TC_Common.SelectorCmd import create_path

def write_texto_in_tmp(texto):
  with open(os.path.join(create_path(f"{os.path.dirname(__file__)}/tmp/UnitScripts"), "paragraphs.txt"), "w") as f:
      for line in texto.split("\n"):
          f.write(f"{line}\n")

string = ""
write_texto_in_tmp(string)