
'''
*************************WARNING**********************************************
****************EXPERIMENTIAL CODE/SOFTWARE***********************************
                CODE/SOFTWARE HEREAFTER software
******************************************************************************
Copyright (c) <2020> <Gerald Teacher>
VERSION (1.0.0)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import json
from tkinter import *
from tkinter import ttk
from tkinter import simpledialog,filedialog
from tkinter.font import families
import tkinter.messagebox
from tkinter.scrolledtext import ScrolledText
import os,sys
from pathlib import Path,WindowsPath
from archicad import ACConnection

def on_about():
    info = """Copyright(c) 2021, under MIT Open License \
              \n    Beta - 1.0.1 \nVersion 1.0.01 \nAdd-On ver 1.1.0.0""" 
            
    tkinter.messagebox.showinfo('Information',info)
def comboclick(event):
    global data,entries,buffer,style_field
    cb = event.widget
    
    cbStyleName = cb.get()
   
    if   not 'keyStyles' in data and not cbStyleName in data['keyStyles']:
        return
        
    if cbStyleName in data['keyStyles']:
        for index,value in enumerate(data['keyStyles'][cbStyleName].values()):
            buffer[index].set(value)
           
            if index >= 4 and index <= 6:
                if value == 0:
                    ind = 0
                else:
                    ind = 1
                style_field[index].current(ind)
            
    else:
        return
def deleteStyle(cb):
    global styleVal

    name = cb.get()
    styleVal = list(cb['values'])
    styleVal.remove(name)
    cb['values'] = styleVal
    cb.current(0)
def addStyle(cb):
    global styleVal,savedata

    name = simpledialog.askstring("NewStyle", "Enter new Style Name")
    if name:
       styleVal = cb['values']
       styleVal = list(styleVal)
       styleVal.append(name)
       index = styleVal.index(name)
       cb['values'] = styleVal
       cb.current(index)
       savedata.set(True)
def saveDefaults(entries,buffer,cb):
    global keyStyles,data,warn1,savedata
    defaultStyle = {}
    keyStyles[cb.get()] = defaultStyle
    for index,x in enumerate(entries):
        defaultStyle[entries[index][0]] = buffer[index].get()
        if not 'keyStyles' in data.keys():
            data['keyStyles'] = {}
        if not 'default' in data['keyStyles'].keys():
            data['keyStyles']['default'] = {}
    data['keyStyles']['default']=defaultStyle
    for key,value in keyStyles[cb.get()].items():
        
        pass

    

    savedata.set(True)
   #   End of saveDefaults
def saveStyle(entries,buffer,cb):
    global data,warn1

    newStyle = {}
    cbStyleName = cb.get()
    if cbStyleName == 'default':
        tkinter.messagebox.showinfo('Selection Error','Use "save as default" \nfor default style')
        return
   
    for index,x in enumerate(entries):
        newStyle[entries[index][0]] = buffer[index].get()
    if not 'keyStyles' in data.keys():
        data['keyStyles'] = {}
    if not cbStyleName in data['keyStyles'].keys():
        data['keyStyles'][cbStyleName] = {}
    data['keyStyles'][cbStyleName]=newStyle
    savedata.set(True)
   
    #   End of saveStyle 
def msg_box(root,text):
    sub=Toplevel(root)
    sub.geometry('445x145+1100+300')
    sub.title('Warning')
    sub.config(relief=RAISED)

    lbl=Label(sub,text=text,font=('arial',20,'bold'),width=20,anchor=N,bd=6,relief=RIDGE,
              padx=0,pady=0).grid(row=0,column=0)
def key_command(event):
    entry=root.focus_get()
    
    return
def remember_focus(event):
    global focused_entry

    return
def onFrameConfigure(canvas):
    """Reset the scroll region to encompass the inner frame"""
    canvas.configure(scrollregion=canvas.bbox("all"))
def populate(frame,skip):
    global yscrollbar
    
    for widget in frame.winfo_children():
        widget.destroy()
    '''Put in some fake data'''
    Label(frame,text='KEY',font=('Arial',16,'bold')).grid(row=0,column=0,sticky='nesw')
    Label(frame, text='NOTES', font=('Arial', 16, 'bold')).grid(row=0, column=1,sticky='nesw')

    cs = disc.curselection()
    if cs:
       cs=disc.get(cs)
    else:
        return
    mylist_keys = list(data['discipline'][cs].keys())
    sortkeys=sorted(mylist_keys)
    mylist_values =list(data['discipline'][cs].values())


    for row in range(len(mylist_keys)):

        v = StringVar()
        v.set(sortkeys[row])

        ent=Entry(frame, textvariable=v, width=7, borderwidth="1",
              relief="solid", highlightbackground="red", highlightcolor="green", highlightthickness=3 )
        ent.grid(row=row + 1, column=0)
        ent.myID = (data['discipline'][cs][sortkeys[row]], sortkeys[row])
        ent.bind('<FocusIn>', on_focus)

        if skip==0:
            text=ScrolledText(frame,width=50,height=1,wrap=WORD,borderwidth='3',bg= 'light yellow',relief='sunken',
                              highlightbackground="red", highlightcolor="green", highlightthickness=3 )
            sortvalue=data['discipline'][cs][sortkeys[row]]
            #print(sortvalue)
            text.insert(END,sortvalue)
            text.grid(row=row+1,column=1,pady=0) # changed pad from 5 to 0
            text.myID = (data['discipline'][cs][sortkeys[row]], sortkeys[row])
            text.bind('<FocusIn>', on_focus)
            skip=1
        else:
            text = ScrolledText(frame, width=50, height=1, wrap=WORD, borderwidth='1',bg= 'white',relief='sunken',
            highlightbackground = "red", highlightcolor="green", highlightthickness=3,)
            sortvalue = data['discipline'][cs][sortkeys[row]]
            text.insert(END, sortvalue)
            text.grid(row=row+1, column=1,pady=0) #changed pad from 5 to 0
            text.myID = (data['discipline'][cs][sortkeys[row]], sortkeys[row])
            text.bind('<FocusIn>', on_focus)
            skip = 0
        text.bind('<FocusIn>', on_focus)
        yscrollbar.set('0','.5')
def make_canvas(root):
    global canvas,canvasframe
    skip = 0
    populate(canvasframe, skip)
    return canvas
def go():
    global canvas,root

    cs=disc.curselection()
    if cs:
        pass
    else:
        return
    cs= disc.get(cs)
    mylist=list(data['discipline'][cs].values())
    canvas=make_canvas(root)
    return canvas
def fndeldisc():
    global savedata,filelocation
    savedata.set(True)
    cs=disc.get(disc.curselection())
    ans = simpledialog.messagebox.askyesno('Alert', f'Do you want to delete discipline {cs}?',icon='warning')
    if ans==False:
        
        return
    del data['discipline'][cs]
    disc.delete(ANCHOR)
    with open(filelocation, 'w') as fp:
        json.dump(data, fp)
def fnadddisc():
    global savedata,discname,filelocation

    savedata.set(True)
    cs=discname.get() # user entry of new discipline category name
    if cs=='':
        simpledialog.messagebox.showinfo('Alert', 'Enter a Discipline to add, in the box below',icon='warning')
        return
    discname.set('') # clear field
    data['discipline'][cs]={}
    disc.insert(END,cs)
    with open(filelocation, 'w') as fp: #filelocation is Global
        json.dump(data, fp)
def on_keysave():
    global savedata,note,noteentry
    savedata.set(True)
   
    note.delete(1.0,END)
def on_keydelete():
  global savedata,filelocation

  savedata.set(True)
  key=simpledialog.askstring('Delete KeyNote','Enter key in the selected Disciple to delete?')
  if key:
      pass
  else:
      simpledialog.messagebox.showinfo('Alert','You must enter a key')
      return

  selecdisc=disc.curselection()
  if selecdisc:
      selecdisc = disc.get(selecdisc)
     # print(data['discipline'][selecdisc][key])
      del data['discipline'][selecdisc][key]
      with open(filelocation, 'w') as fp:
          json.dump(data, fp)
  else:
      simpledialog.messagebox.showinfo('Alert','You must select a Discipline')
      return
def makenote():
   global note,keyentry,data,savedata

   savedata.set(True)
   try:
        xdisc=disc.get(disc.curselection())
   except:
       tkinter.messagebox.showinfo("Key Entry", "You must first select a Discipline")
       return

   if xdisc:
       getkey=keyentry.get()

       if data['discipline'][xdisc].get(getkey,"Empty") == 'Empty':
           ans=tkinter.messagebox.askyesno("Key Entry", f"Key is available {getkey}\n CONTINUE?")
           if ans==TRUE:
               data['discipline'][xdisc][getkey]=note.get(1.0,END)
               note.delete(1.0, END)
               keyentry.set('')
               go()
           else:
               return
       else:
           tkinter.messagebox.showinfo("Key Entry", "Key already exists\n Choose another")
           return
   else:
       tkinter.messagebox.showinfo("Key Entry","You must first select a Discipline")
       return
def on_close():
    global data, savedata,filelocation
    
    if savedata.get():
        answer = tkinter.messagebox.askquestion('Save Data', 'Do You want to save changes?')
        if answer == 'yes':
            with open(filelocation, 'w') as fp:
                json.dump(data, fp)
    answer=tkinter.messagebox.askquestion('Quit Program','Do You want to Quit?')
    if answer=='yes':
        root.destroy()
def on_focus(event):
    global selectedkey,msgkey,selectedkeynote,varck
    selectedkey=event.widget.myID[1]
    selectedkeynote=event.widget.myID[0]
   
    msgkey.set(f'Key Selected {selectedkey}')
def on_update():
    global savedata,disc,filelocation
    savedata.set(True)
    key = simpledialog.askstring('UpDate KeyNote?', 'First--Edit required note field in applicable Discipline\n'
    'Click on desired key\note in note field to UpDate?\n'
    'Make sure that the updated key field is listed below\n( green outline)\n'
    'OR------- Just enter key in entry box below-----------',initialvalue=selectedkey)
    if key==None: #cancel
       simpledialog.messagebox.showinfo('Response','Update Canceled')
       return
    elif key:# OK with key
        simpledialog.messagebox.showinfo('response','ok received')
        pass
    else: #OK pressed but no key entered
        simpledialog.messagebox.showinfo('Alert', 'You must enter a key')
        return
    simpledialog.messagebox.showinfo('TODO', 'Remove Block Update')
    return
    cs=disc.curselection()
    if cs:
       # print(data['discipline'][cs][key])
        data['discipline'][cs][key]='Add revised stuff here'
        with open(filelocation, 'w') as fp:
            json.dump(data, fp)
    else:
        simpledialog.messagebox.showinfo('Alert', 'You must select a Discipline')
        return

def archicad_element(key):
    global disc
    
    parameters = {}
    for  index,x in enumerate(entries):
        parameters[x[0]] = buffer[index].get()
    parameters['txt'] = selectedkey
    parameters['note']= selectedkeynote
    ind = disc.curselection()
    parameters['Discipline']=  disc.get(ind)
  
    response = acc.ExecuteAddOnCommand(act.AddOnCommandId('AdditionalJSONCommands','KeyNote'),parameters)

    if response:
        tkinter.messagebox.showerror('Command Failed',response)
        print(response)
    
    
    sys.exit()
def place_key():
    global selectedkey,selectedkeynote
    answer = tkinter.messagebox.askquestion('Confirm Placement of New KEY', f'Do you want to place key \n{selectedkey}')
    if answer=='yes':
        if varck.get()==0:
            archicad_element(selectedkey)
        else:
            archicad_element(selectedkeynote)
    else:
        tkinter.messagebox.showinfo('Cancel','First select applicable Discipline\n'
          'Then select desired key in note listing box' )
def on_save_file():
    global savedata, filelocation
    
    with open(filelocation, 'w') as fp:
        json.dump(data, fp) 
        savedata.set(False)
def on_saveas_file():
    global savedata,currentFile,filelocation,data,fileloc

    #savedata.set(False)
    askname=filedialog.askopenfilenames=filedialog.asksaveasfilename(filetypes = [("json files","*.json"),("all files","*.*")],
                defaultextension='.json')
    print(askname)
   
    with open(askname , 'w') as fp:
        json.dump(data, fp) 
        savedata.set(False)
    print(os.path.split(askname))
    currentFile.set(os.path.split(askname)[1])
    filelocation = askname
    fileloc.set(askname)
def on_new_file():
    global datafilelocation,data,discname,currentFile,filelocation,savedata

    disc.delete(0,'end')
    dict={}
    #dict['properties']={'font':'Arial','size':'id','emphasis':'bold','color':'red'}
    dict['discipline']={'Electrical':{},'HVAC':{},'General':{},'Plumbing':{},'Structural':{},'Demolition':{},'Mechanical':{},'Kitchen':{}}
    data=dict
    for x in sorted(list(data['discipline'].keys())):
        disc.insert(END, x)
    wd = os.getcwd()
    home = wd + '\\newFile.json'
    filename = os.path.basename(home)
    filelocation = home
    currentFile.set('newFile.json')
    savedata.set(True)
def on_open_file():
    global data,disc,filename,currentFile,savedata,filelocation,path

    home = str(Path.home())
    home = home + '/documents/'
    selectedfile= filedialog.askopenfilename(initialdir=home,title='Jason File')
    currentFile.set(os.path.basename(selectedfile))
    with open(selectedfile,'r') as fp:
        data = json.load(fp)
        disc.delete(0,END)
        for x in sorted(list(data['discipline'].keys())):
            disc.insert(END, x)
        filelocation = selectedfile
    savedata.set(False)
def on_open_default():
    global data,disc,filename,currentFile,filelocation,savedata,path

    #wd = path.absolute()
    wd = str(Path.home())
    wd = wd + '/documents/keynotes/document.json'
    home = wd 
    filename =  os.path.basename(wd)
   
    try:
        with open(str(home),'r')  as fp:
            data = json.load(fp)
            for x in sorted(list(data['discipline'].keys())):
                disc.insert(END, x)
            currentFile.set(filename) 
            filelocation = home
            savedata.set(False)
    except:
        currentFile.set('No Data File Open')
        simpledialog.messagebox.showinfo('File Error', f'\nDefault not found!\nUse "OPEN" to browse for json file!')
def place_style():
    global cb, txtStyle,data,styleVal,buffer,shapes,warn1,style_field

    dlgStyle=Toplevel(root)
    
    dlgStyle.geometry('300x450+100+100')
    dlgStyle.title('KeyNote Style')
    dlgStyle.config(relief=RAISED)
    cb = ttk.Combobox(dlgStyle)
    cb.bind("<<ComboboxSelected>>",  comboclick)
    cb.grid(row=15, column= 0)
    if 'keyStyles' in data.keys():
        keysty = data['keyStyles'].keys()
        if keysty:
            cb['values'] =  list(keysty)

    for index, x in enumerate(entries):
        Label(dlgStyle,text=x[0],font=('arial',10)).grid(row=index,column=0,sticky=NW)
        if  x[2] == 'str':
            buf = StringVar()
        elif x[2] == 'int':
            buf = IntVar ()
        elif x[2] == 'double':
            buf = DoubleVar()
        else:
            buf = BooleanVar()
        buf.set(x[3])
        buffer.append(buf)
        
        if ('keyStyles' in data.keys()) and ('default' in data['keyStyles'].keys()):
                #hold = data['keyStyles']['default'][x[0]] 
                if x[0]== 'Symbol Shape':
                    ent1 = ttk.Combobox(dlgStyle,textvariable = buffer[index],width= 9,font=('arial',10))
                    ent1.grid(row=index,column=1,sticky=W)
                    ent1['values'] = shapes
                elif x[0]== 'Font Type':
                    ent1= ttk.Combobox(dlgStyle,textvariable = buffer[index],width= 9,font=('arial',10))
                    ent1.grid(row=index,column=1,sticky=W)
                    ent1['values'] = font_style
                elif x[0]== 'Font Style Bold' or x[0]== 'Font Style Italic' or x[0]== 'Font Style UnderLine' :
                    style_field[index] = ttk.Combobox(dlgStyle,textvariable = buffer[index],width= 9,font=('arial',10))
                    style_field[index].grid(row=index,column=1,sticky=W)
                    style_field[index]['values'] = status_bool
                    style_field[index].current(0)
                else:
                    ent = Entry(dlgStyle,textvariable = buffer[index],font=('arial',10))
                    ent.grid(row=index,column=1)
                #buffer[index].set(hold)
        else:  
            if index == 0:
                warn1=Label(dlgStyle, text= 'Default Style Not Saved',bg = 'IndianRed1')
                warn1.grid(row=18,column=1,sticky=W)      
            if x[0]== 'Symbol Shape':
                    ent1 = ttk.Combobox(dlgStyle,textvariable = buffer[index],width= 9,font=('arial',10))
                    ent1.grid(row=index,column=1,sticky=W)
                    ent1['values'] = shapes
            else:
                    ent = Entry(dlgStyle,textvariable = buffer[index],font=('arial',10))
                    ent.grid(row=index,column=1)
            buf.set(x[3])
    if 'keyStyles' in data.keys():
            styleVal = list(data['keyStyles'].keys())
            if not'default' in styleVal:
                styleVal.append('default')
                
    if 'default' not in styleVal:
        styleVal.append('default')
    cb['values'] = styleVal
    cb["foreground"] = 'red'
    index = styleVal.index('default') 
    cb.current(index)
    
    btnStyle = Button(dlgStyle,text='Save Style', command= lambda:saveStyle(entries,buffer,cb),bg='yellow')
    btnStyle.grid(row=15, column=1,sticky=W,pady=10)
    btnStyle1 = Button(dlgStyle,text='Save As Default', command=lambda: saveDefaults(entries,buffer,cb),bg='yellow')
    btnStyle1.grid(row=16, column=1,sticky=W)
    btnStyle2 = Button(dlgStyle,text='Add New Style', command=lambda: addStyle(cb),bg='yellow')
    btnStyle2.grid(row=16, column=0,sticky=W)
    btnStyle3 = Button(dlgStyle,text='Delete Style', command=lambda: deleteStyle(cb),bg='yellow')
    btnStyle3.grid(row=17, column=0,sticky=W)
    btnStyle4 = Button(dlgStyle,text='Return', command=lambda: dlgStyle.destroy(),bg='yellow')
    btnStyle4.grid(row=18, column=0,sticky=W)
    dlgStyle.attributes('-topmost',True)

'''************************************Start of Entry Code*******************************'''

conn = ACConnection.connect()
if not conn:
    #tkinter.messagebox.showerror('Archicad','Archicad Not Found')
    sys.exit()
   

acc = conn.commands
act = conn.types
acu = conn.utilities

# Globals'

selectedkey=''
selectedkeynote = ''
filelocation = ''
path = WindowsPath()
keyStyles = {}
buffer = []
data={}
styleVal = []
cb =''
warn1 = ''
shapes = ['circle','rect','hexagon','pentagon','triangle']
status_bool = [False,True]
font_style = ['Arial','Courier','Lucida Handwriting','Times New Roman']
entries =  [    ('Symbol Shape','shape','str','hexagon'),
                ('Text Pen'    ,'tpen','int',6),
                ('Font Type'   ,'fontType','str','Ariel'),
                ('Font Size','fsz','double',12.8),
                ('Font Style Bold','gs_text_style_bold','bool',False),
                ('Font Style Italic','gs_text_style_italic','bool',False),
                ('Font Style UnderLine','gs_text_style_underline','bool',False),
                ('Contour Pen','gs_cont_pen','int',5),
                ('Fill Type','gs_fill_type','int',16),
                ('Fill Pen','gs_fill_pen','int',6),
                ('Fill BackGround Pen','gs_back_pen','int',0),
                ('typeTextRotation','typeTextRotation','str','Horizontal'),
                ('Classification','typeClass','str','keynote'),
                ('CircleDiameter','circleDiameter','double',.23),
                ('Class_Root','class_root','str','ARCHICAD Classification - v 2.0')]
style_field = [None] * len(entries)
#Globals

root = Tk()
savedata =  BooleanVar(root,False) #'False' #False # No data changed
for z in range(10):
    Grid.rowconfigure(root,z,weight=1)
for z in range(5):
    Grid.columnconfigure(root,z,weight=1)

focused_entry=''
root.option_add('*Dialog.msg.font', 'Helvetica 18')

root['bg']='light gray'
root.title('KeyNote Selection Manager')
root.geometry('800x700')

############################## Grid Row #0    ##############################################
currentFile= StringVar()
savedState = StringVar()
def savecall(name,index,mode):
   if savedata.get():
    savedState.set('Data \nNOT Saved')
    status.config(bg= 'red')
   else:
        savedState.set('Data Saved')
        status.config(bg ='light green')
savedata.trace('w',savecall)


 #  Cuurent file in use
Label(root,text='Current filename:',font=('arial',14,'bold')).grid(row=0,column=1,sticky=NW)
Entry(root,textvariable=currentFile,font=('arial',16,'bold'),justify='center').grid(row=0,column=1,sticky=N)
status = Label(root,textvariable=savedState,width = 16,font=('arial',14,'bold'))
status.grid(row=1,column=1,sticky=N)
savedata.set(True)
deldisc=Button(root,text='Delete \nDiscipline',command=fndeldisc,width=7,font=('arial',10,'bold'),)
deldisc.grid(column=0,row=0,sticky=W)

############################## End Grid Row #0 ###########################################

############################## Grid Row #1     ##############################################
adddisc=Button(root,text='Add New \nDiscipline',command=fnadddisc,width=7,font=('arial',10,'bold'),)
adddisc.grid(row=1,column=0,sticky=W)
############################## End Grid Row #1  #########################################

############################## Grid Row #2      ########################################
discname=StringVar()
addtextdisc=Entry(root,textvariable=discname,font=('arial',14,'bold'),width = 12,)
addtextdisc.grid(row=2,column=0,sticky=W)
place_key = Button(root,text="Place KeyNote",command=lambda : archicad_element(buffer)) # Sets note in Archicad
place_key.grid(row=1,column=1,sticky=W)
############################## End Grid Row #2   #################################

############################## Grid Row #3       #################################
lbl_value= Variable()
disc=Listbox(root,selectmode=SINGLE,relief=RAISED,font=('Arial',8,'bold'),bd=3,listvariable=lbl_value,
             highlightcolor='green',highlightthickness=5,highlightbackground='green',width=10)
disc.bind('<<ListboxSelect>>',lambda x:go())
disc.grid(row=3,column=0,sticky=N+S+W)

'''**************************** Setup the Canvas system with frame as base *********************'''

canvas = Canvas(root, borderwidth=15, background="white", width=550,height=250,
                 highlightbackground="green",highlightcolor="green",highlightthickness=5,
               )
canvasframe = Frame(canvas, background="white")
canvasframe.pack()
canvasframe.pack_propagate(False) #fix frame size to that of canvas and not its widgets
yscrollbar = Scrollbar(root,orient='vertical',command=canvas.yview)
canvas.configure(yscrollcommand=yscrollbar.set)
yscrollbar.grid(row=2, column=2, rowspan=3,sticky=(N,S,W))
canvas.grid(row=3,column=1,sticky=NSEW)

item = canvas.create_window((0,0),window=canvasframe)

canvasframe.bind('<Configure>',lambda event,canvas=canvas: onFrameConfigure(canvas))
canvaslabel= Label(canvasframe,text='Select a Discipline',font=('Arial',25,'bold')).grid(row=0,column=0,sticky=NSEW)

'''***************************End of canvas setup-- canvas is re-built upon any discipline selection *****************'''
############################## End Grid Row #3    ###############################################

############################## Grid Row #4        ##################################################
lbl_add_keynote=Label(root,text='Add New Key and Note',bg='light yellow',font=('arial',18,'bold'))
lbl_add_keynote.grid(row=4,column=1,sticky=N)
##############################   End Grid Row #4  ###############################################

##############################  Grid Row #5       ##################################################
frame1=Frame(root,bg='light gray', highlightbackground="black",highlightcolor="green",highlightthickness=5,)
frame1.grid(row=5,column=1,sticky=(N,E,W))

frame2=Frame(frame1,bg='light gray')

frame2.grid(row=0,column=0,sticky=NSEW)
for z in range(5):
    Grid.rowconfigure(frame1, z, weight=1)
for z in range(5):
    Grid.columnconfigure(frame1, z, weight=1)
for z in range(5):
    Grid.rowconfigure(frame2, z, weight=1)
for z in range(5):
    Grid.columnconfigure(frame2, z, weight=1)
notelbl=Label(frame2,text='Note Description',anchor='center',bg='light yellow',font=('arial',16,'bold'))
notelbl.grid(row=1,column=1,sticky=NSEW)
keylbl=Label(frame2,text='Key',bg='light yellow',font=('arial',16,'bold'))
keylbl.grid(row=1,column=0,sticky=NSEW)
keyentry=StringVar()
key=Entry(frame2,width=10,textvariable=keyentry)
key.grid(row=2,column=0,padx=0,sticky=NW) 
noteentry=StringVar()
note=ScrolledText(frame2,width=45,height=5,wrap=WORD,font=('arial',14,'bold'))
note.grid(row=2,column=1,sticky=NSEW)
note_clear=Button(frame2,text='clear \nkeynote',command=lambda:note.delete(1.0,END),bg= 'yellow')
note_clear.grid(row=2,column=2,sticky=W)

frame3=Frame(root,bg='light gray',pady=0)
frame3.grid(row=5,column=0,sticky=(N,E,W))
for z in range(5):
    Grid.rowconfigure(frame3, z, weight=1)
for z in range(5):
    Grid.columnconfigure(frame3, z, weight=1)
delkey=Button(frame3,text="Delete \nKeynote",command=on_keydelete,width=7,font=('Arial',10,'bold'))
delkey.grid(row=0,sticky=W)
addkeynote=Button(frame3,text='New \nKeynote',command=makenote,width=7,font=('Arial',10,'bold'))
addkeynote.grid(row=1,sticky=W)
update=Button(frame3,text="UpDate \nKeynote",command=on_update,width=7,font=('Arial',10,'bold'))
update.grid(row=2,sticky=W)
quit=Button(frame3,text="QUIT",command=on_close,width=7,font=('Arial',10,'bold'))
quit.grid(row=3,pady=0,sticky=NW)
######################################## End Grid Row #5    ###########################################
msg_text='Some text for testing'

frm_keys = Frame(root,bg='light gray',pady=0)
frm_keys.grid(row=1,column=1,sticky=(N,W,E))

####################################### End Grid Row #5   ########################################
menubar=Menu(root,bg='blue',fg='red')
root.config(menu=menubar)

filesubmenu=Menu(menubar,tearoff=0,bg='white',fg='black',activebackground='yellow', activeforeground='black')
filesubmenu.add_command(label='New Jason File',command=on_new_file)
filesubmenu.add_command(label='Open',command=on_open_file)
filesubmenu.add_command(label='Save',command=on_save_file)
filesubmenu.add_command(label='Save As',command=on_saveas_file)
filesubmenu.add_command(label='Exit',command=on_close)
menubar.add_cascade(label='File',menu=filesubmenu)
helpsubmenu=Menu(menubar,tearoff=0,bg='white',fg='black',activebackground='yellow', activeforeground='black')
menubar.add_cascade(label='Help',menu=helpsubmenu)
helpsubmenu.add_command(label='About',command=on_about)

#################################### Grid Row #6      ################################################
on_open_default()
##########################################  End Grid Row #6 ##############################
msgkey=StringVar()
msgkey.set('Select a Key')
msg=Message(root,text='This is a message',font=('Arial',8,'bold'),bg='light yellow',relief=RAISED,
            textvariable=msgkey,takefocus= FALSE)
msg.grid(row=2,column=1,sticky= E)
varck=IntVar()

vardisc=IntVar()
vardisc.set(0)

mystyle=Button(root,text="Set Style",command=place_style,width=10,bg='light green',font=('Arial',10,'bold'))
mystyle.grid(row =1,column = 1,sticky = E)
fileloc =StringVar()
fileloc.set(filelocation)
location =Label(root,textvariable=fileloc,anchor='center',bg='light yellow',font=('arial',16,'bold'))
location.grid(row=4,column=1,sticky=NSEW)
root.protocol("WM_DELETE_WINDOW",on_close)
root.mainloop()
