import tkinter as tk
import astarsearch as ass
import buildboundary as boundary

def GuiPrompt():
    master = tk.Tk()
    tk.Label(master, text="X Window Size").grid(row=0)
    tk.Label(master, text="Y Window Size").grid(row = 1)
    tk.Label(master, text="Number of X elements").grid(row = 2)
    tk.Label(master, text="Starting Cell").grid(row = 3)
    tk.Label(master, text="Ending Cell").grid(row = 4)
    tk.Label(master, text="Boundary File").grid(row = 5)
    # tk.Label(master, text="Rebuild Boundary").grid(row = 6)
    ewindowXMax = tk.Entry(master)
    ewindowYMax = tk.Entry(master)
    erefinemnetX = tk.Entry(master)
    ecellStart = tk.Entry(master)
    ecellEnd = tk.Entry(master)
    eboundaryfile = tk.Entry(master)
    rebuiltcheck = tk.IntVar()
    tk.Checkbutton(master, text="Rebuild Boundary", variable=rebuiltcheck).grid(row = 6)
    ewindowXMax.insert(0, "1500")
    ewindowYMax.insert(0, "1000")
    erefinemnetX.insert(0, "150")
    ecellStart.insert(0, "1, 1") 
    ecellEnd.insert(0, '148, 98')
    eboundaryfile.insert(0, "boundary.json")
    ewindowXMax.grid(row=0, column=1)
    ewindowYMax.grid(row=1, column=1)
    erefinemnetX.grid(row = 2, column=1)
    ecellStart.grid(row = 3, column=1)
    ecellEnd.grid(row = 4, column=1)
    eboundaryfile.grid(row = 5, column=1)
    runbutton = tk.Button(master, 
          text='Run', 
          command=master.quit).grid(row=7, 
                                    column=0, 
                                    sticky=tk.W, 
                                    pady=4)
    master.mainloop()
    windowXMax = int(ewindowXMax.get())
    windowYMax = int(ewindowYMax.get())
    refinemnetX = int(erefinemnetX.get())
    cellStart = tuple(map(int, ecellStart.get().split(', ')))
    cellEnd = tuple(map(int, ecellEnd.get().split(', ')))
    boundaryFilename = eboundaryfile.get()
    master.destroy()
    refinemnetY = int(windowYMax / (windowXMax / refinemnetX))
    if rebuiltcheck.get():
        boundary.CreateRandomBoundary(refinemnetX, refinemnetY, boundaryFilename)
    return windowXMax, windowYMax, refinemnetX, cellStart, cellEnd, boundaryFilename


if __name__ == "__main__":
    windowXMax, windowYMax, refinemnetX, cellStart, cellEnd, boundaryFilename = GuiPrompt()
    ass.run(windowXMax, windowYMax, refinemnetX, cellStart, cellEnd, boundaryFilename)
