import pickle
from collections import Counter

filename = "animals_used.pkl"
skipped = 0
total_counter = {}
tot = 0
watch_terms = ["egg","python","rodent","pupa","larva","primate","insect","bug"]
watchlist = ["rodent","pupa"]


with open(filename, "rb") as f:
  loaded_object = pickle.load(f)

for paper_title in loaded_object.keys():
  aanimals = loaded_object[paper_title]
  animals = [a for a in aanimals if a not in watch_terms]
  top_keyword = ""
  if len(animals) > 1:
    _animals = Counter(animals)
    top_keyword = sorted(_animals, key=lambda x: (-_animals[x], x))[0]
  elif len(animals) == 1:
    top_keyword = animals[0]
  else:
    skipped+=1
    continue

  if top_keyword not in total_counter.keys():
    total_counter[top_keyword] = 1
    tot+=1
  else:
    total_counter[top_keyword] += 1
    tot+=1

  if top_keyword in watchlist:
    print(top_keyword, animals, paper_title)


print(total_counter)
print("Counted papers", tot)
print("Skipped papers", skipped)