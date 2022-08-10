import json
import random
import tkinter as tk
def CreateRandomBoundary(NX, NY, filename = "boundary.json"):
    master = tk.Tk()
    tk.Label(master, text="Number of boundary Cells").grid(row=0)
    nrandentry = tk.Entry(master)
    nrandentry.insert(0, "12000")
    nrandentry.grid(row=0, column=1)
    tk.Button(master, 
          text='Rebuild', 
          command=master.quit).grid(row=6, 
                                    column=0, 
                                    sticky=tk.W, 
                                    pady=4)
    master.mainloop()
    Nrandom = int(nrandentry.get())
    master.destroy()
    # filename = "boundary.json"
    # NX = 150
    # NY = 100
    boundarynodes = []
    # Nrandom = 12000

    for x in range(0, NX):
        boundarynodes.append((x, 0))
    for x in range(0, NX):
        boundarynodes.append((x, NY-1))
    for y in range(0, NY):
        boundarynodes.append((0, y))
    for y in range(0, NY):
        boundarynodes.append((NX-1, y))

    for iter in range(0, Nrandom):
        boundarynodes.append((random.randint(0, NX-1), random.randint(0, NY-1)))

    with open(filename, 'w') as ofile:
        json.dump(boundarynodes, ofile)

if __name__ == "__main__":
    pass