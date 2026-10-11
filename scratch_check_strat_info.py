import json
with open("user_data/config.json") as f:
    config = json.load(f)

from NostalgiaForInfinityX8_Combined import NostalgiaForInfinityX8_Combined
strat = NostalgiaForInfinityX8_Combined(config=config)
print("Informative pairs:", strat.informative_pairs())
