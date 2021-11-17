'''A simplification layer over tkinter dialogs where contol type and format is based on intialisation variable
'''

from tkinter import *
#import tkMessageBox
import string

scroll_boxes = []   # contains (scroll_widget,dialog) used for mouse scrolling of selector boxes and integer fields
buttons = [] # contains (butten_widget, variable list,dialog,current_value) so that buttons can be called indirectly

class ControlDialog(Toplevel):
    '''tkinter dialog formated by a list of intial values passed at construction.
       Fields are validated on change and non-blocking error message boxes generated if required.
       Individual controls can callback to application if valid.
       Apply button (if required) sends callback to parent for action if fields valid.
    '''

    def __init__(self, parent, variables, title = None, callonchange = None, status_line = None, needs_apply = False):

        '''Initialize a dialog.

            parent -- a parent window (the application window)
            variables -- an tuple or list of format
                         ( label,              # must be unique or list/tuple
                           intial value,       # determines field type
                           callback_function,
                           maximum_value,
                           minimum_value,
                           float_precision     # how many decimals to display
                         )
                         If label is list or tuple then radio buttons
                         If initial value == None then field is button
                                          == bool then check box
                                          == int  then text field
                                          == float then text field
                                          == string then text field
                                          == list   then ?
                                          == tuple  then ?
                         For int and float types if a tuple is found then (reference,max,min)
                         If label does not end with >>> then the next field is on a new line
            title -- the dialog title
        '''
        Toplevel.__init__(self, parent)
        # self.transient(parent) - this dialog isn't transient
        if title:
            self.title(title)
        self.parent = parent
        self.variables = variables
        self.callonchange = callonchange
        self.needs_apply = needs_apply   # do we need an apply button (effects Return key also
        # note: if there are any text or number entry types then apply will appear regardless

        self.result = None
        self.exit_request = False

        body = Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()  # adds apply and exit buttons
        if status_line:
          self.status_line = Label(self, text=status_line, bd=1, relief=SUNKEN, anchor=W)
          self.status_line.pack(side=BOTTOM, fill=X)
        else:
          status_line = None
        #self.grab_set() - don't want to freeze parent

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.exit)

        # self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
        #                          parent.winfo_rooty()+50))

        self.initial_focus.focus_set()
        # self.wait_window(self) - main window must keep running
        self.message_box = None  # dialog used to indicate entry errors

    def __del__(self):
      '''Removes  any reference to iself in scroll_boxes and buttons arrays'''
      #rint "Removing child reference arrays"
      for sb in scroll_boxes:
        if sb[0] in self.entry:
          scroll_boxes.remove(sb)
          break
      for b in buttons:
        if b[0] in self.entry:
          buttons.remove(b)
          break

    def update(self):
      '''Updates both this dialog and any dependant message boxes'''
      if self.message_box != None:
        self.message_box.update()
        if self.message_box.exit_request == True:
          self.message_box.destroy()
          self.message_box = None
      else:
        Toplevel.update(self)

    def destroy(self):
      '''Destroy dialog window'''
      #rint "Destroy dialog"
      self.initial_focus = None
      self.__del__()  # call explicitly
      Toplevel.destroy(self) # doesn't seem to do anything until next update

    def body(self, master):
        '''Create dialog body.

          Returns widget that should have the initial focus.
          This is always called by the __init__ method.
        '''
        i = 0  # count entry fields of dialog
        coli = 0
        rowi = 0
        self.entry = []
        self.old_value = []
        self.current_value = []
        focus_entry = None
        for v in self.variables:
          if v == None or len(v) == 0:
            continue
          #rint "Variable:",v
          if type(v[0]) in (list,tuple):
            label_text = v[0][0]
          else:
            label_text = v[0]
          if label_text.endswith('>>>'):
            label_text = label_text[:-3]
            follows = True
          else:
            follows = False
          if len(v) == 1:  # just text
            Label(master, text=label_text).grid(row=rowi,column=coli, stick=W)
            self.old_value.append(None)
            self.current_value.append(None)
            self.entry.append(None)
          else:
            self.old_value.append(v[1])
            self.current_value.append(v[1])
            if v[1] == None or self.isListButton(v) or (not self.isSimple(v[1]) and len(v) > 2):  # call only or list call or call to instance
              if len(v) > 2:
                if v[1] == None:  # call only
                  entry = Button(master, text=label_text, command=v[2])
                else:  # where an instance is involved it will need to know the value v[1]
                  entry = Button(master, text=label_text)
                  # don't use call command directly so that source dialog info can be sent
                  buttons.append((entry,v,self))
                  entry.bind('<Button-1>',button_callback)
                entry.grid(row=rowi,column=coli, stick=W)
                self.entry.append(entry)
              else:
                print("ERROR: Button without a callback?")
                return
            elif type(v[1]) in (bool,):
              if len(v) < 3 or  not callable(v[2]):
                self.needs_apply = True
              intval = IntVar()
              intval.set(v[1])
              self.entry.append(Checkbutton(master, text=label_text,variable=intval,command=self.bool_command))
              self.entry[i].var = intval
              self.entry[i].grid(row=rowi,column=coli, stick=W)
            else:  # not a checkbox or a button
              if type(v[0]) in (list,tuple):
                # selector, list or radio button with list of labels
                option_index = 0
                options = v[0][1:]
                intval = IntVar()
                if v[1] not in (tuple,list):
                  # this test not for listBox type
                  if type(v[1]) != list:
                    option_index = 0  # start with the first in the list
                  elif type(v[1]) != int:
                    # initial value set from list
                    #rint "Inital option value:",v[1],type(v[1])
                    for o in options:
                      if o == v[1]:
                        break
                      option_index += 1
                    if option_index >= len(options):
                      option_index = 0
                  else:
                    option_index = v[1]
                    #rint "Initial value:",option_index
                if self.isSelectorBox(v):
                  # selector box style
                  self.current_value[i] = option_index  # needs to be an integer
                  self.needs_apply = True
                  Label(master, text=label_text[:-2]).grid(row=rowi,column=coli, stick=W)
                  coli += 1
                  #rint "What:",option_index,options
                  if len(options) == 0:
                    entry = Label(master, text="EMPTY",borderwidth=4,relief=GROOVE)
                  else:
                    option_text = self.getOptionText(options,option_index)
                    entry = Label(master, text=option_text,borderwidth=4,relief=GROOVE,background="#FFFFFF")
                    self.make_scrollable(entry)
                    entry.bind('<Key>',scroll_command) # selector boxes can use any key
                  entry.grid(row=rowi,column=coli, stick=W)
                  self.entry.append(entry)
                else:
                  # list or radio style
                  #rint "Radio or list type:",v[0]
                  if len(v) < 3 or  not callable(v[2]):
                    self.needs_apply = True
                  #rint "v[1]:",type(v[1])
                  #rint len(v[1]), len(v[0])
                  if self.isListBox(v):
                    # mult select so use list widget instead of radio
                    box = Frame(master)
                    Label(box, text=label_text).pack(anchor=W)
                    entry = Listbox(box,selectmode = MULTIPLE)
                    j = 0
                    for t in options:
                      #rint "Add ",t
                      entry.insert(END,t)
                      if v[1][j]:
                        entry.select_set(j)
                      j +=1
                    entry.pack(anchor=W)
                    self.entry.append(entry)
                    #self.entry[i].grid(row=rowi,column=coli)
                    sys.stdout.flush()
                  else:
                    # radio style
                    box = Frame(master,borderwidth=4,relief=RIDGE)
                    Label(box, text=label_text).pack(anchor=W)
                    intval.set(option_index)
                    j = 0
                    for t in options:
                      #rint "Radio entry:",t
                      entry = Radiobutton(box, text=t,variable=intval,value = j,command=self.radio_command)
                      if j == 0:
                        self.entry.append(entry)   # only need the first one
                      entry.var = intval
                      entry.pack(anchor=W)
                      j += 1
                  box.grid(row=rowi,column=coli, stick=W)
              else:
                self.needs_apply = True
                Label(master, text=label_text).grid(row=rowi,column=coli, stick=W)
                coli += 1
                entry = Entry(master)
                self.entry.append(entry)
                #rint v[0],v[1]
                entry.insert(0,self.format_entry(v,v[1]))
                entry.grid(row=rowi,column=coli, stick=W)
                if type(v[1]) == int:
                  self.make_scrollable(entry)
            # set focus - prefer non checkbutton type
            #rint "Entry sync:",len(self.entry),i
            if not focus_entry or (isinstance(focus_entry,Checkbutton) and not isinstance(self.entry[i],Checkbutton)):
              focus_entry = self.entry[i]
          if follows:
            coli +=1
          else:
            rowi += 1
            coli = 0
          i += 1
        return focus_entry # initial focus

    def getOptionText(self,options,optioni):
      ''' Returns text for optioni from list options as string regardless of type'''
      option = options[optioni]
      if type(option) in (str,):
        text = option
      elif self.isInstance(option):
        text = self.getInstanceName(option)
      else:
        text = str(option)
      return str(optioni) + ":"+text

    def getInstanceName(self,v):
      ''' Returns name of instance.
          If instances has a name member then use that, else use type.
      '''
      if hasattr(v,'name'):
        return (getattr(v,'name'))
      else:
        return objectTypeName(v)

    def isSimple(self,v):
      '''Returns True if v is str,int,float,tuple or list '''
      return type(v) in (bool,str,int,float,tuple,list)

    def isListButton(self,v):
      '''Returns True if this entry is for a list button'''
      return (type(v[1]) in (list,tuple) and type(v[0]) not in (list,tuple))

    def isInstance(self,v):
      '''Returns True if v is type instance'''
      return str(type(v)) in ("<type 'instance'>",)

    def isSelectorBox(self,v):
      '''Returns True if a selector box should be used for v as directed by +- suffix in label.'''
      label_text = v[0][0]
      if label_text.endswith('>>>'):
        label_text = label_text[:-3]
      return label_text.endswith('+-')

    def isListBox(self,v):
      '''Returns True if variable refers to a listbox '''
      return (type(v[1]) in (list,tuple) and len(v[0]) == len(v[1])+1)


    def make_scrollable(self,entry):
      '''Bind mouse buttons to increment or decrement control'''
      scroll_boxes.append((entry,self))  # so that mouse can increment
      entry.bind('<Button-1>',plus_command)
      entry.bind('<Button-2>',minus_command)
      entry.bind('<Button-3>',minus_command)
      entry.bind('<Button-4>',minus_command)  # scroll wheel
      entry.bind('<Button-5>',plus_command)

    def format_entry(self,v,val):
      '''Return integer and floats as text strings'''
      if type(v[1]) in (float,) and len(v) > 5:  # float with decimal places setting
        entry_str = "%.*f" % (v[5],val)
      else:
        entry_str = str(val)
      return entry_str

    def buttonbox(self):
        '''Add standard button box including exit and apply if required.
           override this if you don't want the standard buttons
        '''

        box = Frame(self)
        if self.needs_apply:
          w = Button(box, text="Apply", width=10, command=self.apply_change, default=ACTIVE)
          w.pack(side=LEFT, padx=5, pady=5)
          self.bind("<Return>", self.apply_change)
        w = Button(box, text="Exit", width=10, command=self.exit)
        w.pack(side=LEFT, padx=5, pady=5)
        self.bind("<Escape>", self.exit)

        box.pack()

    #
    # standard button semantics

    def apply_change(self, event=None):
        ''' Called from apply button or from keyboad Enter in text field.'''
        if not self.validate():
            #rint "At least one invalid field"
            self.initial_focus.focus_set() # put focus back
            return
        #rint "Valid fields so send apply"
        #self.withdraw()
        self.update_idletasks()
        self.apply()


    def exit(self, event=None):
      '''Set exit request so that parent update can remove this dialog.
         If parent has request_exit function then conditionally set.
      '''
      # put focus back to the parent window
      self.parent.focus_set()
      #rint "Request exit"
      try: # parents such as root don't have a request exit method
        self.exit_request = self.parent.request_exit(self)
      except:
        self.exit_request = True  # for parent = root, pole for exit_request in loop

    #def request_exit(self,child):
    #  ''' children of dialog have permission to exit'''
    #  print "Exit request"
    #  return True

    def bool_command(self):
        '''Look for changes in check boxes and use item callback if one has been set'''
        i = 0
        # check that all bool current values match gui check boxes
        for v in self.variables:
          if len(v) > 1 and v[1] != None:
            if type(v[1]) in (bool,):
               val = (self.entry[i].var.get() == 1)
               if self.current_value[i] != val:
                 self.current_value[i] = val
                 if len(v) > 2 and callable(v[2]):
                   v[2](v[0],val,0)  # stage 0
          i +=1



    def radio_command(self):
        ''' Look for changes in radio contols and use item callback if one is set
            Not available for list box type even though format similar
        '''
        i = 0
        # check that current values match settings for radio buttons
        for v in self.variables:
          if not self.noChoice(v) and type(v[1]) not in (list,tuple) and type(v[0]) in (list,tuple):  # radio type
            try:
              val = self.getEntry(v,i)
              index = v[0][1:].index(val)
            except:
              val = v[0][1]  # default to first value
              index = 0
            #rint self.current_value
            if self.current_value[i] != index:
              self.current_value[i] = index
              if len(v) > 2 and callable(v[2]):
                v[2](v[0][0],val,0)  # stage 0
          i +=1

    def set(self,index,val):
      ''' Used by external classes to change values on the fly
          index can be index to entry or a string matching label
      '''
      if type(index) == int:
        i = index
        if i < 0 or i >= len(self.variables):
          return                 # no match
        v = self.variables[i]
      else:  # find label string
        i = 0
        v = None
        if type(index) in (list,tuple):
          label = index[0]
        else:
          label = index
        for vv in self.variables:
          if type(vv[0]) in (list,tuple): # match found in list
            if label in vv[0]:
              v = vv
              break
          elif vv[0] == label:  # match found
            v = vv
            break
          i +=1
        if v == None:
          return    # no match found
      if type(v[1]) in (bool,) or type(v[0]) in (list,tuple):   # bool or radio
        options = v[0][1:]
        if type(val) != int:
          oi = 0
          for o in options:
            if o == val:
              break
            oi += 1
        else:
          oi = val
        if oi < 0 or oi >= len(options):
          print("ERROR:Selection ",oi," is outside of options:",options)
          if oi < 0:
            oi = 0
          else:
            oi = len(options)-1
        if self.isSelectorBox(v):
          self.entry[i].config(text=options[oi])
        elif self.isListBox(v):
          self.entry[i].select_set(oi)
        else:
          self.entry[i].var.set(oi)  # assumes caller knows what it's doing
      else:
        self.entry[i].delete(0, END)
        self.entry[i].insert(0,self.format_entry(v,val))
        #rint val,self.format_entry(v,val)
      self.current_value[i] = val
      self.old_value[i] = val

      #self.entry[i].config()  #format % args)
      #self.entry[i].update_idletasks()
    #
    # command hooks

    def setBy(self,fields):
      ''' As for set but using a list of index,value pairs'''
      for f in fields:
        self.set(f[0],f[1])

    def validate(self):
        ''' Validate the data in the controls.

        This method is called automatically to validate the data before apply callback used.
        If there is an error, a list of crimes will appear in a non-blocking message box.
        '''
        i = 0
        all_valid = True  # assumption
        msg = ""
        for v in self.variables:
          if self.noChoice(v): # ie text label or button for some purpose
            i += 1
            continue # nothing to validate
          if len(msg) > 0 and msg[-1] != '\n':
            msg += '\n'
          #rint "Validate:",self.getLabel(v)," of type:",type(v[1])
          # see if field can be converted
          invalid = False  # another assumption
          #try:
          try:
            val = self.getEntry(v,i)
            #rint "?Convert:",val," to ",v[1]
            if type(val) != type(v[1]) and type(v[0]) in (list,tuple):
              #rint "Convert type:",type(val)," to ",type(v[1])
              val = v[0][val+1]  # will throw exception if out of range or wrong type
          except:
            invalid = True
          else:
            #rint "Value is:",val," of type:",type(val)
            if type(v[0]) in (list,tuple):
              if type(v[1]) == list and type(v[1][0]) == bool:
                if len(v) > 3:
                  # check for max and min number of selections
                  selections = 0
                  for b in val:
                    if b:
                      selections += 1
                  #rint "Found ",selections," selections"
                  if v[3] != None and selections > v[3]:
                    msg += 'max of '+str(v[3]) + ' selections'
                    invalid = True
                  elif len(v) > 4 and v[4] != None and selections < v[4]:
                    msg += 'min of '+str(v[4]) + ' selections'
                    invalid = True
              elif type(v[1]) == int:
                invalid = (v[1]<0 or v[1]>= len(v[1:]))
              else:
                invalid = (val not in v[0][1:])  # just check it's one of the options
            elif v[1] != None and len(v) > 2:
              #rint v
              #  first limit format of entries
              if type(v[1]) == float:
                #rint "Limit:",v
                if len(v) > 5:  # limited decimal places
                  self.entry[i].delete(0, END)
                  self.entry[i].insert(0,self.format_entry(v,val))
              if type(val) in (float,int) and len(v) > 3:  # check range
                if v[3] != None and val > v[3]:      # None can be used as a maxvalue
                  invalid = True
                  msg += 'max='+str(v[3])+' '
                elif len(v) > 4 and v[4] != None and val < v[4]:
                  invalid = True
                  msg += 'min='+str(v[4])+' '
              if not invalid and callable(v[2]):  # check with callback if value is okay
                invalid = v[2](v[0],val,1)    # individual validation function - 1  = validation stage
          if invalid:
            msg += " for field: "+self.getLabel(v)
            ex = sys.exc_info()[0]
            if ex != None:
              msg += " has "+str(ex)

            all_valid = False
          try:
            if invalid:
              self.entry[i]['fg'] = "red"
            else:
              self.entry[i]['fg'] = "black"
          except:
            pass
          i += 1
          #rint "Invalid:",invalid
        if not all_valid:
          #tkMessageBox.showwarning("Bad input",msg)
          if self.message_box:
            self.message_box.destroy()
          self.message_box = ControlDialog(self,((msg,),),"Invalid Entry Warning")
        return all_valid

    def noChoice(self,v):
      '''Returns true if control item v has no options or settings '''
      return ((len(v) < 2) or (v[1] == None) or ((type(v[0]) not in (list,tuple)) and (self.isInstance(v[1]) or (type(v[1]) in (list,tuple)))))

    def getLabel(self,v):
      '''Returns label to display once macros in v[0] are removed.'''
      if type(v[0]) in (tuple,list):
        lbl = v[0][0]
      else:
        lbl = v[0]
      ei = lbl.find('+-')
      if ei < 0:
        ei = lbl.find('>>>')
      return lbl[:ei]


    def apply(self, event=None):  # event value is sent if attached to key
        '''Process the data in the controls and send it using the apply callback.
        This method is called after a return key is pressed or the apply button is clicked
        '''
        #if event:
          #rint event
        i = 0
        for v in self.variables:
          if len(v) > 1 and v[1] != None:
            try:
              val = self.getEntry(v,i)
            except:
              print("ERROR:exception during apply:",str(sys.exc_info()[0])," for field:",self.getLabel(v))
              changed = False
            else:
              changed = (self.old_value[i] != val)
              self.old_value[i] = val
            # check for individual callbacks
            if changed and len(v) > 2 and callable(v[2]):
              v[2](v[0],val,2)    # individual notification function - 2  = apply stage
          i += 1
        if callable(self.callonchange):
          self.callonchange(self)  # group notification


    def getEntry(self,v,i):
      '''Get the value in the control in list v referenced by index or label
         Intended for internal use.
      '''
      if self.noChoice(v):  # text or button type has no value and so is always valid
        return None
      if type(v[1]) in (bool,):
        val = (self.entry[i].var.get() == 1)
      else:
        #rint i, type(v[1][0]),self.entry[i].info
        if type(v[0]) in (list,tuple):
          if self.isSelectorBox(v):
            val = self.current_value[i]  # selector box always returns int
          elif self.isListBox(v):
          #if v[0][0].endswith(">>>"):  # Listbox
            selection = self.entry[i].curselection()
            reply = [False]*len(v[1])
            for s in selection:
              reply[int(s)] = True
            #rint "Field list entry:",reply
            if type(v[1]) == 'tuple':
              return tuple(reply)
            else:
              return reply
          else:  # radio button
            val = self.entry[i].var.get()
          if type(v[1]) != int:  # is initial value set from list
            try:
              val = v[0][val+1]
            except:   # value was invalid?
              val = 0
        else:  # text field of some type
          str = self.entry[i].get()
        #rint str
          if type(v[1]) in (int,):
            val = string.atoi(str)
          elif type(v[1]) in (float,):
            val = string.atof(str)
          else:
            val = str
      #rint "Field entry:",v[0],v[1],val,type(v[1]),type(val)
      return val

    def getValue(self,field_label):
      ''' As with getEntry but first parses the label and finds the index for the item.
          This is the one for applications to use.
      '''
      if type(field_label) in (list,tuple):
        label = field_label[0]
      else:
        label = field_label
      i = 0
      for v in self.variables:
        if type(v[0]) in (tuple,list):
          vl = v[0][0]  # label is first in list for radio or selector box types
        else:
          vl = v[0]
        #rint "Find field:",vl,field_label
        if vl == label:
          try:
            val = self.getEntry(v,i)
          except:
            print("ERROR:exception during getValue:",str(sys.exc_info()[0])," for field:",field_label)
            return None
          if type(val) == int and type(v[1]) != int and type(v[0]) in (list,tuple):
            options = v[0][1:]
            if val < 0 or val >= len(options):
              print("ERROR: Selector box selection index ",val," out of range of options:",options)
              if val < 0:
                return options[0]
              else:
                return options[-1]
            else:
              return options[val]
          else:
            return val
          #if type(v[0]) in (tuple,list):
            #rint 1+val, v[0]
          #  return v[0][1+val]  # return tuple item
          # else:
          return val
        i += 1
      print("Error: Request for field label not found for:",label)
      return None

    def setStatusLine(self, new_text):
      '''Set status line text if a status line was intiated.'''
      if self.status_line:
        self.status_line.config(text=new_text)  #format % args)
        self.status_line.update_idletasks()

    def widget_scroll(self,entryi,k):
      '''  Called through scroll_widget to increment (k='+') or decrement (k='-')
           the value for the control indexed by entryi
      '''
      i = self.entry.index(entryi)
      v = self.variables[i]
      if type(v[1]) == int or self.isSelectorBox(v):
        #if type(self.current_value[i]) != int:
          #rint "Selector:",v[1],self.current_value[i]
        if k == '+' and (len(v) < 4 or self.current_value[i] < v[3]):
          self.current_value[i] += 1
        elif k == '-' and (len(v) < 5 or self.current_value[i] > v[4]):
          self.current_value[i] -= 1
        #rint "Widget scroll:",self.current_value[i]
        if type(v[0]) in (list,tuple):
          options = v[0][1:]
          if self.current_value[i] < 0:
            self.current_value[i] = 0
          elif self.current_value[i] >= len(options):
            self.current_value[i] = len(options)-1
          if self.isSelectorBox(v):
            option_text = self.getOptionText(options,self.current_value[i])
            self.entry[i].config(text=option_text)
        else:
          self.entry[i].delete(0,END)
          self.entry[i].insert(0,self.format_entry(v,self.current_value[i]))

def minus_command(event):
  ''' Global decrement callback for mouse press in dialog area
      Used to operate a scrollable widget such as a select_box or integer text field.
  '''
  scroll_widget(event.widget,'-')

def plus_command(event):
  ''' Global increment callback for mouse press in dialog area
      Used to operate a scrollable widget such as a select_box or integer text field.
  '''
  scroll_widget(event.widget,'+')

def scroll_command(event):
  ''' Used by integer text fields to handle scroll keys + and -'''
  scroll_widget(event.widget,event.keysym)

def scroll_widget(widget,k):
  '''Finds the scroll widget that matches widget and uses the associated dialog to call widget_scroll'''
  for sb in scroll_boxes:
    if sb[0] == widget:
      #rint "Scroll box found"
      sb[1].widget_scroll(widget,k)
      return

def button_callback(event):
  ''' Used for indirect call to unrecognised value buttons
      This usually means a list or instance has been associated with a button and
      the callback will then create a dialog to edit it - refer auto_dialog.py.
  '''
  widget = event.widget
  for b in buttons:
    if b[0] == widget:
      var = b[1]  # a reference to variable list used for selectorbox field in dialog
      if callable(var[2]):
        #rint "Simple call"
        var[2](var,b[2])  # callback will assume this is stage 0

def objectTypeName(obj):
  ''' Try to create a name just from obj type (usually an instance, list or tuple)
  '''
  if type(obj) == list:
    name = "list "
  elif type(obj) == tuple:
    name = "tuple "
  else:
    name = repr(obj)
    si = name.find('__main__.')
    if si < 0:
      si = name.find('<')
      if si >= 0:
        si += 1
    else:
      si += 9
    ei = name.find(' instance')
    if si >= 0 and ei >= 0:
      name = "class "+name[si:ei]
    else:
      name = "Object ID#"+str(id(obj))
  return name

# test code follows

def main():
  ''' Scaffold / unit test code'''

  def test_callback(dialog):
    #rint "Test callback:",dialog.variables
    print("Radio value:",dialog.getValue("Test radio"))

  def test_press():
    print("button pressed")

  class test_class:
    def __init__(self):
      pass

  def test_press2(value,parent,stage=0):
    print("button pressed:",value,parent,stage)
    return False # possibly required for stage 1 validation

  # value callbacks - may be called immediatly on change (stage = 0), at validation (state = 1) or
  # if and only if a change occured from the orininal value at apply stage (return key or apply button)

  def int_fn(name="",value = None, stage = 0):
    if stage == 1:
      return False
    print("int is ", value," at stage:", stage)

  def bool_fn(name="",value = None, stage = 0):
    print("bool is ", value, " at stage:",stage)

  def selector_fn(name="",value = None, stage = 0):
    if stage == 1:
      return False
    print("selector is ", value," at stage:", stage)

  def list_fn(name="",value = None, stage = 0):
    if stage == 1:
      return False
    print("list is ", value," at stage:", stage)

  def radio_fn(name="",value = None, stage = 0):
    if stage == 1:
      return False
    print("radio is ", value," at stage:", stage)

  import sys

  root = Tk()
  int_val = 1
  float_val = 2.34574563
  min_val = 1.3
  max_val = 3.4
  bool_val = True
  str_val = "Hello"
  selector_options = ("Aust","B","C")
  selector_val = "B"
  list_val = [False,True,True]
  radio_val = 0
  class_instance = test_class()
  var_list = (("Just some text>>>",),
              ("Test button",None,test_press),
              ("Test button2",class_instance,test_press2),
              ("Test Float:",float_val,None,max_val,min_val,3),
              ("Test Bool:",bool_val,bool_fn),
              ("Test String:",str_val),
              (("Test selector box+-",)+selector_options,selector_val,selector_fn),
              (("Test list>>>","Sydney","Melbourne","Adelaide"),list_val,list_fn,2,1),
              (("Test radio","One","Two","3"),radio_val,radio_fn),
              ("Test Int:",int_val,int_fn))
  status_line = "This is the status line"
  dialog = ControlDialog(root,var_list,"Control Dialog Test",test_callback,status_line,False)
  #app.mainloop()
  frame = 0
  dialog.update()
  dialog.lift()
  while not dialog.exit_request:
#    try:
    dialog.update()
    sys.stdout.flush()
    dialog.setStatusLine('%10d' % frame)
    #if frame % 100 == 0:
    #  dialog.set("Test Int:",frame)
    frame += 1
  dialog.destroy()  # don't need to do this here but it is good practice

if __name__ == '__main__': main()
