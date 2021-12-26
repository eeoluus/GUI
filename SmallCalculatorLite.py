import sys
import tkinter as tk
from itertools import chain
from os import getcwd, listdir
from os.path import isfile, join

class standardOutput:
    """Context manager for temporary redirection of stdout output."""
    
    def __init__(self, newOutput):
        self.newOutput = newOutput

    def __enter__(self):
        self.oldOutput = sys.stdout
        sys.stdout = self.newOutput

    def __exit__(self, excType, excVal, excTb):
        sys.stdout = self.oldOutput

def insertAutoScroll(*args, widget=None, placement=tk.END):
    """Automatically scroll where you insert text.
    
    widget -- The tkinter widget where you insert the text.
    args -- Each argument must contain a list of messages.
    placement -- Where the message is inserted in the widget. Defaults to tk.END.
    """
    if widget is None:
        widget = log
    flatIterable = chain(*args)
    for message in flatIterable:
        widget.insert(placement, message + '\n')
        widget.see(placement)

def write(self, string):
    """Unbound method for redirecting the stdout stream to a widget."""
    self.insert(tk.END, string)
    self.see(tk.END)
        
def importFrom(package, module):
    """Import a module from a package."""
    package = __import__(package, fromlist=[module])
    return getattr(package, module)

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
    event.widget.delete(0, tk.END)
    messageList = [userInput]
    insertAutoScroll(messageList)

    if isStrat(userInput, stratNames):
        taskBuffer[0] = userInput
        insertAutoScroll(messageDict['integers'])
        
    else:
        intList = [int(string) for string in userInput.split(', ')]
        task = importFrom(
            'strats', 
            taskBuffer[0]
            )
        result = task.operation(
            intList[0], 
            intList[1]
            )
        resultMsg = [f"{messageDict['result'][0]} {result}"]
        insertAutoScroll(
            resultMsg,
            messageDict['nextOperation'],
            stratNames
            )
        
def setup():
    """Initialize the GUI window and divide it into two parts: the output and input boxes."""
    root = tk.Tk()
    root.geometry("500x500")
    root.title("Small Calculator")
    
    log = tk.Text(root)
    insertAutoScroll(
        messageDict['welcome'],
        stratNames,
        widget=log    #the callback default won't yet be evaluated correctly
        )
    log.configure(
        font='TkFixedFont', 
        bg='#000000', 
        fg='#00FF00'
        )
    log.write = write.__get__(log)    #enables redirection of stdout output
    log.pack(fill=tk.BOTH, expand=1)

    entry = tk.Entry(root)
    entry.bind('<Return>', handleEntry)
    entry.configure(
        font='TkFixedFont', 
        bg='#000000', 
        fg='#00FF00',
        insertbackground='#00FF00'
        )
    entry.icursor(tk.END)
    entry.pack(fill=tk.BOTH, expand=1)

    return root, log

if __name__ == '__main__':  
    
    path = f'{getcwd()}/strats'
    strats = [f for f in listdir(path) if isfile(join(path, f))]
    stratNames = [s.split('.')[0] for s in strats]

    taskBuffer = ['']
    messageDict = {
        'welcome': ['Welcome to the Small Calculator! What do you want to do? Available operations are'],
        'integers': ['Enter two integers separated by a comma and whitespace'],
        'nextOperation': ['If you want to keep calculating, available operations are'],
        'result': ['The result is']
        }

    root, log = setup()   ##root.pack_slaves() also usable for getting the widgets, if the returns get too numerous
        
    with standardOutput(log):
        root.mainloop()

