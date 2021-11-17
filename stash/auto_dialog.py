'''Automatically generate Tkinter dialog to examine an instance of class, list or tuple
   using control_dialog module.
'''

from .control_dialog import *

autoDialogs = []

class AutoDialog(ControlDialog):
  '''Object explorer Tkinter dialog using ControlDialog methods but constructed purely on the contents of a
     single object passed at construction.
  '''
  def __init__(self,parent,control_obj,title = None,apply_callback=None):
    ''' Initialize a dialog.

            parent -- a parent window (the application window)
            control_obj -- can be an instance of class, list or tuple
            title -- title to appear in dialog window (uses object type if None)
            apply_callback -- function to notify for any value changes
    '''
    global autoDialogs
    var_list = self.build_list(control_obj)
    if title:
      dtitle = title
    else:
      dtitle = objectTypeName(control_obj)
    self.apply_callback = apply_callback
    if apply_callback == None:
      ap = None
    else:
      ap = changeAutoDialog
    ControlDialog.__init__(self,parent,var_list,dtitle,ap)
    autoDialogs.append(self)

  def __del__(self):
    '''Removes  any reference to iself in autoDialogs array'''
    if self in autoDialogs:
      autoDialogs.remove(self)
      #rint "Remove from autodialog"
      ControlDialog.__del__(self)

  def build_list(self,control_obj):
    '''Generate a list of labels and values based on the contents of control_obj'''
    self.control_obj = control_obj
    var_list = []
    if self.isInstance(control_obj):
      for p in dir(control_obj):
        if not self.isVariable(p):
          continue
        v = getattr(control_obj,p)
        self.add_field(var_list,p,v)
    else:  # must be list or tuple
      i = 0
      for v in control_obj:
        self.add_field(var_list,i,v)  # label is the index number
        i += 1
    return var_list

  def add_field(self,var_list,p,v):
      ''' Used by build_list() to add a field to the variable list'''
      #rint "Object name:",p," = ",v," is of type:",type(v)
      #if type(v) == tuple and not self.isInstance(v[0]):
      #  return  # can't alter anything so no point having it in dialog
      if self.isVariableType(v):
        name = self.genLabel(p,v)
        var = [name,v]
        if type(self.control_obj) == tuple and not (self.isInstance(v) or type(v) in (list,tuple)):
          # can't alter anything in tuple except to examine an instance, list or tuple
          var_list.append((name+' = >>>',))
          if type(v) == str:
            var = ('"'+v+'"',)  # show that it is a string
          else:
            var = (str(v),)
        elif type(v) in (int,float):  # these types can have a max or min value
          maxp = str(p) + '_max_value'
          if hasattr(self.control_obj,maxp):
            maxv = getattr(self.control_obj,maxp)
            var.append(None)
            var.append(maxv)
            minp = str(p) + '_min_value'
            if hasattr(self.control_obj,minp):
              minv = getattr(self.control_obj,minp)
              var.append(minv)
        elif self.isInstance(v) or type(v) in (list,tuple):
          #rint "Object [selection] and editing type",name
          if type(name) in (list,tuple):
            if len(var[0]) > 1:  # make sure it's not an empty list
              var[0][0] += '>>>'  # so that edit button can follow
              #rint "Instance list:",name
              var_list.append(var)  # add now so that edit goes on end
              #rint "PreEdit varlist:",var_list
              var = ("Edit",v,editInstanceCallback)
          elif type(v) == list:
            #rint "Edit type",v[0]
            var = ("Edit list:"+name,v,editInstanceCallback)
          elif type(v) == tuple:
            #rint "View type",v[0]
            var = ("View tuple:"+name,v,editInstanceCallback)
          elif type(p) == int: # as for list index
            var = (str(p)+">>>",)
            var_list.append(var)
            var = (self.getInstanceName(v),v,editInstanceCallback)  # simle push button to edit
          else:
            var.append(editInstanceCallback)  # simle push button to edit
        #rint "Add:",var
        var_list.append(var)
       
  def isMember(self,p):
    ''' Returns True if there is a member of control object called by str p'''
    if self.isInstance(self.control_obj):
      return hasattr(self.control_obj,p)
    else:
      return False

  def isVariable(self,p):
    ''' Returns True when variable named p does not have a name starting with underscore,
        and rejects all methods and special members which are not to be shown on the dialog
        Special members are:
          *_max_value = indicates that variable * shall not exceed this value
          *_min_value = indicates that variable * shall not go below this value
          *_values = list or tuple of value that variable * may equal.
    '''
    if p.startswith('_'):  # not ment to be fiddled with
      return False
    if p.endswith('_max_value'):
      if self.isMember(p[:-10]):  # only ignored if the prefix exists by itself
        return False
    elif p.endswith('_min_value'):
      if self.isMember(p[:-10]):
        return False
    elif p.endswith('_values'):
      if self.isMember(p[:-7]):
        return False
    return True

  def isVariableType(self,v):
    '''Returns True if field item v refers to a simple or instance type
    '''
    if self.isSimple(v):
      return True
    if self.isInstance(v):
      return True
    return False

  def genLabel(self,p,v):
    ''' Return label based on p being an index or a label and v being a list, tuple or instance.
        Returned Label may be a list if the value is an enumerated type (usually indicated by there
        also being a *_values special member cataloging the options.
    '''
    if type(p) == int:
      return str(p)  # probably a list index
    else:
      name = p
    #rint "Gen:",p," type:",type(v)
    if type(v) == list:  # list object can be edited
      if self.isAllInstance(v):
        name = [name+'+-',] + v
        #rint "List edit type",type(p)

    elif self.isSimple(v) or self.isInstance(v):
      pv = name + '_values'
      #rint "Test:",pv
      if hasattr(self.control_obj,pv):  # enumerated variable
        pvalues = getattr(self.control_obj,pv)
        #rint "Values:",pvalues
        name = [name+'+-',] + list(pvalues)  # note: pvalues may not be strings
        # control_dialog selector mode will convert to strings when required
    return name

  def isAllInstance(self,v):
    ''' Returns True of all the values in list/tuple v are of type instance.'''
    for vp in v:
      #rint "Is type:",type(vp)," an instance"
      if not self.isInstance(vp):
        return False
    return True

  def request_exit(self,child):
    ''' Called by child dialog to confirm that it is okay to exit '''
    child.destroy()
    return True # not really required as child has gone

  def refresh(self):
    ''' Update all the values shown on the dialog using the values in control_obj'''
    var_list = self.build_list(self.control_obj)
    self.setBy(var_list)

  def change(self):
    ''' Update all the values in control_obj using the values shown in dialog and
        call apply_callback if one is set.
    '''
    #rint "Auto dialog change"
    if self.isInstance(self.control_obj):
      for p in dir(self.control_obj):
        if not self.isVariable(p):
          continue
        v = getattr(self.control_obj,p)
        if type(v) in (bool,str,int,float,list):
          #rint "change variable:",p,v
          name = self.genLabel(p,v)
          if type(name) in (list,tuple):
            name = name[0]
          if type(v) == list:
            name = "Edit:"+name
          vn = self.getValue(name)
          if vn != v:
            #rint "Was[",v,"] Now[",vn,"]"
            setattr(self.control_obj,p,vn)
            #rint getattr(self.control_obj,p)
    else:  # assume it is list
      #rint "Apply changes to list of length:",len(self.control_obj)
      i = 0
      for v in self.control_obj:
        if type(v) in (tuple,):
          continue
        vn = self.getValue(str(i))
        #rint "Was[",v,"] Now[",vn,"]"
        if v != vn:
          self.control_obj[i] = vn
        i += 1
      #rint self.control_obj
    if self.apply_callback:
      self.apply_callback(self)

def changeAutoDialog(dialog):
  ''' Call the change function for dialog - used by Apply button on dialog so that
      the underlying control_dialog class can be used without modification.
  '''
  dialog.change()

def editInstanceCallback(value,dialog = None,stage=0):
  ''' called by autoDialog to create a new child dialog to edit/view a instance of a class,
      list or tuple.  Tuples can only be viewed though instances and lists within them
      can themselves be edited.
  '''
  #rint "Edit instance",value,dialog
  if stage != 0:   # don't want this to occur at apply stage
    return
  i = 0
  new_value = None
  for v in dialog.variables:
    if len(v) > 1:
      #rint "Test:",v[0]
      if v[1] == value[1] and type(v[0]) in (list,tuple):
        new_value = v[0][1 + dialog.current_value[i]]
    i += 1
  if new_value == None:
    new_value = value[1]
  for a in autoDialogs:
    if a.control_obj == new_value:  # already exists
      try:
        a.lift()
        #rint "Dialog for this object already exists"
        return  # just lift the old dialog back to top
      except:
        print("Dialog doesn't seem to exist anymore")
        autoDialogs.remove(a)
  parent = dialog
  src_obj = dialog.control_obj
  name = ""
  if type(src_obj) == list:
    if new_value in src_obj:
      index = src_obj.index(new_value)
      name = "#"+str(index)
  else:  # assume instance    
    for p in dir(src_obj):
      #rint p
      if p.startswith('_'):
        continue
      v = getattr(src_obj,p)
      if v == new_value:
        name = p
        break
  title = name + " <" + objectTypeName(new_value) + ">"
  if type(new_value) == tuple:
    tl = "View: "+title
    ap = None  # tuple values cannot be changed
  else:
    tl = "Edit: "+title
    ap = parent.apply_callback
  auto_dialog = AutoDialog(parent,new_value,tl,ap)
  auto_dialog.lift()

# test code follows

def main():
  ''' Scaffold/unit tests '''
  def apply_callback(dialog):
    print("Apply callback")
    int_value = dialog.getValue('IntValue')
    print("Value:",int_value)
    if dialog == test_dialog:
      test_auto_dialog.set('IntValue',int_value)
    else:
      test_dialog.set('IntValue',int_value)

  # value callbacks - may be called immediatly on change (stage = 0), at validation (state = 1) or
  # if and only if a change occured from the orininal value at apply stage (return key or apply button)

  def int_fn(name="",value = None, stage = 0):
    if stage == 1:
      return False
    print("int is ", value," at stage:", stage)

  class test_subclass:
    def __init__(self,name):
      self.name = name
      self.v = 4
      self.v2 = 5.5

  class test_subclass2:
    def __init__(self):
      self.v = 9
      self.v2 = 8.5

  sub_objs = []
  sub_objs2 = []
  for i in range(3):
    sub_objs.append(test_subclass("SubClass"+str(i)))
    sub_objs2.append(test_subclass2())

  class test_class:

    test_int_max_value = 7
    test_season_values = ("Spring","Summer","Winter")

    def __init__(self):
      self.test_bool = False
      self.test_int = 4
      self.test_int_min_value = 3
      self.unknown_min_value = 5
      self.unknown_values = (True,False,True)
      self.IntValue = 4
      self.test_float = 5.5
      self.test_string = "Hello"
      self.test_season = "Summer"
      self.sub_object = test_subclass("OneSubClass")
      self.sub = sub_objs[0]
      self.sub_values = sub_objs  # this one doesn't get dialoged
      self.class_tuple = ("1st","2nd","3rd")
      self.class_list = [True,3,5.5,"Help"]
      self.sub2 = sub_objs2[0]
      self.sub2_values = sub_objs2

  #import sys

  root = Tk()
  test_object = test_class()

  var_list = (("IntValue",test_object.IntValue,int_fn),)
  test_dialog = ControlDialog(root,var_list,"Control Dialog Test",apply_callback,None,False)
  test_dialog.update()
  test_dialog.lift()

  test_auto_dialog = AutoDialog(root,test_object,None,apply_callback)
  test_auto_dialog.update()
  test_auto_dialog.lift()

  frame = 0
  while not test_dialog.exit_request and not test_auto_dialog.exit_request:
    test_dialog.update()
    test_auto_dialog.update()
    #sys.stdout.flush()
    frame += 1
  test_dialog.destroy()              # not required but good practise
  test_auto_dialog.destroy()    # not required but good practise

if __name__ == '__main__': main()
