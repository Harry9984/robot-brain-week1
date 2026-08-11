import csv

data = [
    ["Red Shirt", "199"],
    ["Shirt, Red (Large)", "299"],
    ["Blue Hat", "99"],
]

with open("data/out.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["title", "price"])
    w.writerows(data)
