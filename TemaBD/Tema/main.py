import tkinter
import GUI

if __name__ == '__main__':
    root = tkinter.Tk()
    root.title("League Of Legends Database")
    root.geometry("850x500")
    root.resizable(False, False)
    gui = GUI.GUI(root)
    root.mainloop()
