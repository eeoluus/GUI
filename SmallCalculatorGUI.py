import tkinter as tk
from os import getcwd, listdir
from os.path import isfile, join

path = f'{getcwd()}/strats'
strats = [f for f in listdir(path) if isfile(join(path, f))]
stratNames = [s.split('.')[0] for s in strats]

def import_from(module, name):
    module = __import__(module, fromlist=[name])
    return getattr(module, name)

def logStrats(strats, view):
    """List available operations in the GUI window."""
    for strat in strats:
        view.log.insert(tk.END, strat)

def isStrat(userInput, strats):
    """Check if user-inputted operation exists in the strategies."""
    if userInput in strats:
        return True
    return False

class Controller:
    """Perform requested mathematical operations and control what the user sees."""
    
    def __init__(self, view):
        self.view = view
        self.taskBuffer = ['']
        
    def handleEntry(self, event):
        """Store the requested operation in a buffer or operate on integers.
        
        After this, ask for integers or list available operations again, respectively.
        """
        userInput = event.widget.get()
        self.view.log.insert(tk.END, userInput)
        
        if isStrat(userInput, stratNames):
            self.taskBuffer[0] = userInput
            self.view.log.insert(
                tk.END, 
                self.view.messageDict['integers']
                )            
        else:
            strList = list(userInput.split(', '))
            intList = list(map(int, strList))
            task = import_from(
                'strats', 
                self.taskBuffer[0]
                )
            result = task.operation(
                intList[0], 
                intList[1]
                )
            message = self.view.messageDict['result']
            resultMsg = f'{message} {result}'
            self.view.log.insert(
                tk.END, 
                resultMsg
                )
            self.view.log.insert(
                tk.END, 
                self.view.messageDict['nextOperation']
                )
            logStrats(stratNames, self.view)
            
    def start(self):
        self.view.setup(self)
        self.view.startMainLoop()
        
class TkView:
    
    def setup(self, controller):
        """Initialize the GUI window and divide it into two parts: the output and input boxes."""
        self.root = tk.Tk()
        self.root.geometry("500x500")
        self.root.title("Small Calculator")
        self.messageDict = {
            'welcome': 'Welcome to the Small Calculator! What do you want to do? Available operations are',
            'integers': 'Enter two integers separated by a comma and whitespace',
            'nextOperation': 'If you want to keep calculating, available operations are',
            'result': 'The result is'
            }
        
        self.log = tk.Listbox(self.root)
        self.log.insert(
            tk.END, 
            self.messageDict['welcome']
            )
        logStrats(stratNames, self)
        self.log.pack(fill=tk.BOTH, expand=1)
        
        self.entry = tk.Entry(self.root)
        self.entry.bind(
            '<Return>', 
            controller.handleEntry
            )
        self.entry.pack(fill=tk.BOTH, expand=1)
        
    def startMainLoop(self):
        self.root.mainloop()   

def main():
    app = Controller(TkView())
    app.start()
    
if __name__ == '__main__':
    main()
