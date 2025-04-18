# basic-capella-update

---

## install requirements
pip install requirements.txt

---

## update main.py
add your variables into main.py

---

## run
python ./main.py

---

## output
document body and ttl before and after update

---

## next steps
read from array of keys and ttl times
loop through array
update each doc with the correct value

### psudo code
for k,ttl in doc_array:
  upsert(key, UpsertOptions(new_expiry))
