from pathlib import Path
from cobra.io import save_json_model, load_matlab_model, save_matlab_model, read_sbml_model, write_sbml_model, validate_sbml_model
import logging


print("-----init calc fba------")

data_dir = Path(".") / "uploads"
data_dir = data_dir.resolve()

print("data_dir -> ", data_dir)

mini_fbc2_path = data_dir / "arquivo_sbml3_ccbh4851_argollo.xml"

model = read_sbml_model(str(mini_fbc2_path.resolve()))
report = validate_sbml_model(str(mini_fbc2_path.resolve()))

solution = model.optimize()
print(round(solution, 6))
print(report)

print("-----end calc fba------")

