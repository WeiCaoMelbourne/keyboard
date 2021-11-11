'''Wrapper around tkinter to simplify menu and dialog creation for rapid application development.
'''

import tkinter
import tkinter.messagebox as tkMessageBox 
import tkinter.filedialog as tkFileDialog
from .managed_dialog import *
from .control_dialog import *
from .auto_dialog import *
# import managed_dialog
# import control_dialog

# **************** menu methods ******************************************

gui_bool = {}  # dictionary of all gui states

class control_gui(tkinter.Frame):
  ''' Simplified menu and controls for main tkinter window.
  '''
  def __init__(self, parent, menu_design=None, control_design=None, status_str=None):
    '''Initialise window:
         parent = usually the tk root.
         menu_design = nested array of menu elements.
                       eg. (('File',(('Open',open_callback),('Save',save_callback))),('About'...))
         control_design = array of text or button elements
                       eg. ('This is just some text>>>',('Exit Button',exit_callback))
                       Note: The >>> indicates that the next element is to appear to the right of this one.
         status_str = initial string to put in the status line at the bottom of the window.
         Note: menu items shown have only command_on callbacks which will be triggered
         whenever the menu item is clicked.
         Menu items can additionally have a:
           - command_off callback (which infers that the former only occurs when switched on),
           - an identifier variable which must be unique for this gui instance.
           - a state variable to indicate if this item is intially selected,
           - a depends list which indicates which menu items must active for this item to be enabled.
    '''
    tkinter.Frame.__init__(self, parent)
    self.parent = parent
    parent.title("Control dialog")  # assumes we are using this to control an application
    self.menu_commands = []   # commands and check buttons
    self.menu_dict = {}  # used to index menu items
    menu = tkinter.Menu(parent)
    parent.config(menu=menu)
    for m in menu_design:
      #rint "Menu1:",m
      submenu = tkinter.Menu(menu)
      self.menu_inc(submenu)  # due to tearoff option
      menu.add_cascade(label=m[0], menu=submenu)
      for sm in m[1]:
        #rint "Menu2:",sm
        if sm[0] == "Seperator":
          submenu.add_separator()
          self.menu_inc(submenu) # due to seperator
        else:
          self.menu_add(submenu,sm)  # alt is window.quit)

    self.menu_depends()

    body = tkinter.Frame(self)
    self.initial_focus = self.body(body,control_design)
    body.pack(padx=5, pady=5)

    if status_str != None:
      self.status_line = tkinter.Label(self, text=status_str, bd=1, relief=tkinter.SUNKEN, anchor=tkinter.W)
      self.status_line.pack(side=tkinter.BOTTOM, fill=tkinter.X)
    if not self.initial_focus:
      self.initial_focus = self
    self.initial_focus.focus_set()

  def getLabel(self, text):
    ''' Returns string to appear after macro suffixes are removed'''
    if text.endswith('>>>'):
      return text[:-3], True
    else:
      return text,False

  def body(self, master,control_design):
    '''Create frame body, controls and menu items and then returns the widget that should have initial focus.
      This is called by the __init__ method.
    '''
    if control_design == None:
      return None
    # first scan for number of columns
    columns = 1
    for c in control_design:
      if type(c) in (tuple,list):
        t,g = self.getLabel(c[0])
      else:
        t,g = self.getLabel(c)
      if g:
        coli +=1
        if coli >= columns:
          columns = coli + 1
      else:
        coli = 0
    #rint "There were %d columns" % (columns,)
    # now for the show

    rowi = 0
    coli = 0
    i = 1
    for c in control_design:
      try:
        if type(c) in (tuple,list):
          t,g = self.getLabel(c[0])
          if len(c) > 1 and c[1] != None:
            widget = tkinter.Button(master, text=t, command=c[1])
          else:
            widget = tkinter.Label(master, text=t)
          if len(c) > 2:
            widget.config(fg=c[2])
        else:
          t,g = self.getLabel(c)
          widget = tkinter.Label(master, text=t)
      except:
        print("ERROR: Something wrong with format of control_design in item ",i)
      #rint g, coli
      if not g and columns - coli > 1:
        widget.grid(row=rowi,column=coli, stick=W, columnspan = columns - coli)
      else:
        widget.grid(row=rowi,column=coli, stick=W)
      if g:
        coli +=1
      else:
        rowi +=1
        coli = 0
      i += 1
    #button.pack(side=tkinter.LEFT)
    focus_entry = None
    return focus_entry # initial focus

  def menu_inc(self,menu):
    ''' Used in body() to skip tear off options and seperator items'''
    if menu in self.menu_dict:
      count = self.menu_dict[menu] + 1
      self.menu_dict[menu] = count
    else:
      count = 0
      self.menu_dict[menu] = count
    return count

  '''Notes regarding use of menu without using tkinter.mainloop()
     Adding a normal menu command fails due to some thread problem
  '''
  def menu_add(self,menu_parent,item):
    ''' Add a menu item to the management arrays for command_true, command false,
        identifier variable, state and depends.
    '''
    #item = (label,command_true,command_false,variable,state,depends):
    global gui_bool
    var = tkinter.IntVar()
    command_true = None
    command_false = None
    variable = None
    state = False
    depends = False
    if len(item) > 1:
      command_true = item[1]
      if len(item) > 2:
        command_false = item[2]
        if len(item) > 3:
          variable = item[3]
          if len(item) > 4:
            state = item[4]
            if len(item) > 5:
              depends = item[5]
    if state:
      var.set(1)
    # need to keep track of how many items in this menu - there must be a better way
    count = self.menu_inc(menu_parent)
    self.menu_commands.append((var,variable,command_true,command_false,depends,menu_parent,count))
    gui_bool[variable] = state
    menu_parent.add_checkbutton(label=item[0], variable = var)

  def menu_set(self, variable, state = True, act = True):
    ''' used by application to set a menu item (identified by variable) to state.
        Normally this will also trigger the attached callbacks if set but this may be
        inhibited if act = False (required for radio button type behaviour).
    '''
    for c in self.menu_commands:
      if c[1] == variable:  # menu tickable
        if state:
          val = 1
        else:
          val = 0
        c[0].set(val)  # set tick box on gui
        if not act:
          gui_bool[c[1]] = (val == 1)
          print("Set menu:",c[1]," to ",gui_bool[c[1]])
        #else
        #  let next menu_update take the appropriate action
        break
    self.menu_depends()

  def menu_depends(self):
    ''' check menu item dependancies to determine which items should be enabled. '''
    #i = 0
    for c in self.menu_commands:
      state = tkinter.NORMAL
      if c[4]:   # are there any depenadancies at all (ie not None)
        for d in c[4]:
          if not gui_bool[d]:  # one of the dependancies is not met
            state = tkinter.DISABLED
            break
      #print c[1],c[4],c[6],state
      try:
        c[5].entryconfig(c[6],state=state)
      except:
      #  print "No state for index:",c[6]
        pass
      #try:
      #  c[5].entryconfig(c[6],label=str(i))
      #except:
      #  print "No label for index:",c[6]
      #  pass
      #i += 1

  def menu_update(self):
    ''' Update this dialog and all it children including any menu checks.
        This is not usually called directly but rather through global update().
    '''
    for c in self.menu_commands:
      val = (c[0].get() == 1)
      if val and c[1] == None: # command type so remove select state
        if c[2] != None:  # command for val will be true
          c[2]()
        c[0].set(0)
      if c[1] != None:
        if val != gui_bool[c[1]]:    # only active if change of state
          gui_bool[c[1]] = val
          self.menu_depends()
          #rint val, c, gui_bool
          if val:
            if c[2] != None:  # command if val true
              c[2]()
          else:
            if c[3] != None:  # command if val false
              c[3]()
            elif c[2] != None:   # no false command, so don't allow to untick
              c[0].set(1)

  def setStatusLine(self, new_text):
    '''Set status line if this was set in constructor.'''
    if self.status_line:
      self.status_line.config(text=new_text)  #format % args)
      self.status_line.update_idletasks()

# ****************** popup dialogs **********************************

def popup_dialog_callback(dialog):  # typically old value and dialog instance
  '''Called by a change or apply in child popup to trigger associated callback'''
  # need to check which dialog is source of call
  for key,value in popup_dialog_dict.items():
    if not value[0]:
      continue
    if value[0] == dialog:
    #if related(value[0],widget):  # see if event came from a child of this dialog
      # copy new values to associated list
      print("Found destination for callback event")
      #for i in range(len(value[2])): # for each value in variable array
      #  value[2][i] = new_values[i]
      #  print "Variable array element #",i," =",value[2][i]
      value[1](dialog)  #   refresh_callback()
      break

max_val = 1e20
min_val = -1e20

popup_dialog_dict = {}   # dictionary of tuple(dialog,event_function,event_variable) using same key as gui_bool

depth = 0
child = 0

def related(parent, relation):
  ''' Return True if an assumed relation is really a child of parent
      Not currently used but retained for contingency.
  '''
  global depth,child
  # print "Related?:",depth,parent.winfo_name,relation.winfo_name
  if parent == relation:
    return True          # it is youself, ya daft wee git
  depth += 1
  if relation.master:
    return related(parent,relation.master)  # check if relations parent is parent and so on upwards
  return False

def popup_dialog_keyEvent(event):
  ''' Find the dialog that caused this event and pass the event to it
      This is callback is bound to control key events in popup dialogs created here.
  '''
  for key,value in popup_dialog_dict.items():
    if not value[0]:
      continue
    if value[0] == widget:  # find correct dialog
#    if related(value[0],event.widget):  # see if event came from a child of this dialog
      value[1](event,value[2],value[0])  # yes, so do something with value
      break


parent_destroy_callback = None

def make_gui(menu_design, key_event_callback=None, control_design=None, status_str=None):
  ''' The main call by an application to tkfront which handles all tkinter initialisation
      and the creation of a main window based on menu_design and control_design (see constructor
      for the control_gui class in this module)
      key_event_callback is used to handle any key events for this window.
      status_str = string to appear in a status line at the bottom of the window if required.
  '''
  global root, main_dialog
  root = tkinter.Tk()
  root.protocol("WM_DELETE_WINDOW", quit_callback)
  main_dialog = control_gui(root,menu_design,control_design,status_str)
  main_dialog.pack()
  if key_event_callback != None:
    main_dialog.bind('<Key>',key_event_callback)
  return main_dialog
#
#
# def create_popup_dialog(dialog_name,
#                         dialog_settings_array,
#                         dialog_title,
#                         apply_callback):
#   '''
#      dialog_settings_array describes fields - see control dialog
#      odiag is a array of (event_handler, state, name, depends, refresh_callback)
#   '''
#   if key not in popup_dialog_dict:
#     popup_dialog_dict[dialog_name] = [None,apply_callback]   # no dialog yet, apply function
#   if not popup_dialog_dict[dialog_name][0]:
#     print "Creating view dialog"
#     # view orientation also has FOVY
#     dialog = ControlDialog(main_dialog,dialog_settings_array,dialog_title,popup_dialog_callback,None,False)
#     dialog.transient(main_dialog)
#     dialog.bind('<Control-Key>',popup_dialog_keyEvent)
#     popup_dialog_dict[dialog_name][0] = dialog
#   return popup_dialog_dict[dialog_name][0]
#
#

def create_popup_dialog(key, dialog_settings_array, dialog_title, dialog_callback):
  ''' Creates a dialog using the control_dialog module.
        key = identify the menu item that called dialog
        dialog_settings_array = values required by ControlDialog - refer control dialog constructor
        dialog_title = title to appear in the dialog title bar
        dialog_callback = the callback to be used when the apply button (if it exists) is pressed.
  '''
  if key not in popup_dialog_dict:
    popup_dialog_dict[key] = [None,]   # no dialog yet
  if not popup_dialog_dict[key][0]:
    #rint "Creating dialog"+key
    dialog = ControlDialog(main_dialog,dialog_settings_array,dialog_title,dialog_callback,None,True)
    dialog.transient(main_dialog)
    dialog.bind('<Control-Key>',popup_dialog_keyEvent) # orient_keyEvent)
    popup_dialog_dict[key][0] = dialog
  return popup_dialog_dict[key][0]

def create_popup_managed_dialog(key, dialog_settings_array, dialog_title, dialog_callback):
  ''' Creates a dialog using the managed_dialog module.
        key = identify the menu item that called dialog
        dialog_settings_array = values required by ManagedDialog - refer managed dialog constructor
        dialog_title = title to appear in the dialog title bar
        dialog_callback = the callback to be used when the apply button (if it exists) is pressed.
  '''
  if key not in popup_dialog_dict:
    popup_dialog_dict[key] = [None,]   # no dialog yet
  if not popup_dialog_dict[key][0]:
    #rint "Creating dialog"+key
    dialog = ManagedDialog(main_dialog,dialog_settings_array,dialog_title,dialog_callback,None,True)
    dialog.transient(main_dialog)
    dialog.bind('<Control-Key>',popup_dialog_keyEvent) # orient_keyEvent)
    popup_dialog_dict[key][0] = dialog
  return popup_dialog_dict[key][0]

def create_popup_auto_dialog(key, obj, title = None, apply_callback = None):
  ''' Creates a dialog using the auto_dialog module.
        key = identify the menu item that called dialog
        obj = instance of class, list or tuple that the dialog is to edit/view
        dialog_title = title to appear in the dialog title bar
        dialog_callback = the callback to be used when the apply button (if it exists) is pressed.
  '''
  if key not in popup_dialog_dict:
    popup_dialog_dict[key] = [None,]   # no dialog yet
  if not popup_dialog_dict[key][0]:
    #rint "Creating dialog"+key
    if title == None:
      ktitle = key
    else:
      ktitle =title
    dialog = AutoDialog(main_dialog,obj,ktitle,apply_callback)
    dialog.transient(main_dialog)
    dialog.bind('<Control-Key>',popup_dialog_keyEvent) # orient_keyEvent)
    popup_dialog_dict[key][0] = dialog
  return popup_dialog_dict[key][0]

def destroy_popup_dialog(key):
  '''Removes references of popup dialog from popup_dialog_dict.
     Usually called following a request by that dialog to exit in the update function.
  '''
  if key in popup_dialog_dict and popup_dialog_dict[key][0] != None:           # not required so if exist then destroy
    #rint "Destroying view dialog"
    popup_dialog_dict[key][0].destroy()
    popup_dialog_dict[key][0] = None
  if key in gui_bool.keys():
    gui_bool[key] = False

# def destroy_popup_dialog(key):
#   if key in popup_dialog_dict and popup_dialog_dict[key][0] != None:           # not required so if exist then destroy
#     print "Destroying dialog"
#     popup_dialog_dict[key][0].destroy()
#     popup_dialog_dict[key][0] = None
#   if key in gui_bool.keys():
#     gui_bool[key] = False

def get_popup_dialog(key):
  '''Returns instance of dialog referenced by the key that was used in creation.
  '''
  #rint "Get_popup_dialog:",key,popup_dialog_dict
  return popup_dialog_dict.get(key)
  
# helper functions

def open_dialog(type_str = "All",suffix_str = "*.*"):
  '''Direct wrapper for tkinter file open selection box'''
  return tkFileDialog.askopenfilename(filetypes=[(type_str, suffix_str),])

def save_dialog(type_str = "All",suffix_str = "*.*",default = ""):
  '''Direct wrapper for tkinter file saveas selection box'''
  return tkFileDialog.asksaveasfilename(filetypes=[(type_str, suffix_str),])

def quit_callback():
  '''Presents blocking message box to check user really wanted to leave.
  '''
  if tkMessageBox.askokcancel("Quit", "Do you really wish to quit?"):
    main_dialog.destroy()
    if parent_destroy_callback:
      parent_destroy_callback()
    return True
  return False

def about_dialog(text):
  '''Present blocking text box (block means the application is paused)'''
  tkMessageBox.showinfo("ABOUT",text)
  
error_box = None

def error_dialog(text, blocking = True):
  '''Presents text block with error message.
       If blocking set to False then application will not pause on error - this may be
       desired in some real time applications.
       Note: popup dialogs always use non-blocking error boxes on validation errors.
  '''
  global error_box
  if blocking:
    tkMessageBox.showerror("ERROR",text)
  else:
    if error_box == None:  # can not create new error till last one cleared
      error_box = ControlDialog(main_dialog,((text,),),"ERROR WARNING")

main_dialog_status_str = ""

def update(status_str = ""):
    ''' Called in main loop of application to update main, popup and message dialogs
        The status message can also be changed in not empty.
    '''
    global main_dialog_status_str, error_box
    main_dialog.menu_update()
    try:
      main_dialog.update()
    except:
      print("dialog error")
    if status_str != main_dialog_status_str:
      main_dialog_status_str = status_str
      main_dialog.setStatusLine(status_str)
    #main_dialog.lift()

    if error_box != None:
      error_box.update()
      if error_box.exit_request == True:
        error_box.destroy()
        error_box = None

    for key,value in popup_dialog_dict.items():
      if value[0] != None:
        value[0].update()  # update dialog
        if value[0].exit_request:
          main_dialog.menu_set(key,False)  # then let next update deal with it
          destroy_popup_dialog(key)  # only need this for imagedialogs but doesn't clear tick

