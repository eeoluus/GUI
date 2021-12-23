import tkinter as tk
from os import getcwd, listdir
from os.path import isfile, join

def logStrats(strats, log):
    """List available operations in the GUI window."""
    for strat in strats:
        log.insert(tk.END, strat)

def import_from(module, name):
    module = __import__(module, fromlist=[name])
    return getattr(module, name)

def isStrat(userInput, strats):
    """Check if user-inputted operation exists in the strategies."""
    if userInput in strats:
        return True
    return False

def handleEntry(event):
    """Store the requested operation in a buffer or operate on integers.

    After this, ask for integers or list available operations again, respectively.
    """
    userInput = event.widget.get()
    log.insert(tk.END, userInput)

    if isStrat(userInput, stratNames):
        taskBuffer[0] = userInput
        log.insert(tk.END, messageDict['integers'])   
        
    else:
        intList = [int(string) for string in userInput.split(', ')]
        task = import_from(
            'strats', 
            taskBuffer[0]
            )
        result = task.operation(
            intList[0], 
            intList[1]
            )
        resultMsg = f"{messageDict['result']} {result}"
        log.insert(tk.END, resultMsg)
        log.insert(tk.END, messageDict['nextOperation'])
        logStrats(stratNames, log)
        
def main():
    """Initialize the GUI window and divide it into two parts: the output and input boxes."""
    root = tk.Tk()
    root.geometry("500x500")
    root.title("Small Calculator")
    
    log = tk.Listbox(root)
    log.insert(tk.END, messageDict['welcome'])
    logStrats(stratNames, log)
    log.pack(fill=tk.BOTH, expand=1)

    entry = tk.Entry(root)
    entry.bind('<Return>', handleEntry)
    entry.pack(fill=tk.BOTH, expand=1)
    
    return root, log

if __name__ == '__main__':  
    
    path = f'{getcwd()}/strats'
    strats = [f for f in listdir(path) if isfile(join(path, f))]
    stratNames = [s.split('.')[0] for s in strats]

    taskBuffer = ['']
    messageDict = {
        'welcome': 'Welcome to the Small Calculator! What do you want to do? Available operations are',
        'integers': 'Enter two integers separated by a comma and whitespace',
        'nextOperation': 'If you want to keep calculating, available operations are',
        'result': 'The result is'
        }

    root, log = main()   ##root.pack_slaves() also usable for getting the widgets, if the returns get too numerous
    root.mainloop()

