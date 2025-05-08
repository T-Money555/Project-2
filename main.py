from gui import *

def main() -> None:
    """
    Begins the creation of a GUI using tkinter through the gui class
    """
    window = Tk()
    window.title('Grade Database Filer')
    window.geometry('500x400')
    window.resizable(False, False)
    Gui(window)

    window.mainloop()

if __name__ == '__main__':
    main()