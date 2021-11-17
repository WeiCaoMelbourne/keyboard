'''The next layer above control_dialog.py that sits over Tkinter dialogs where contol type and format is based on intialisation variable
   For the managed dialogs, instances of objects can be updated (ie managed) by the dialog itself.
'''

from .control_dialog import *

class ManagedDialog(ControlDialog):
  '''Tkinter dialog using ControlDialog methods with additional functions to manage updating
     of controls on source value change and visa versa.'''
  def __init__(self, parent, variables, title = None, callonchange = None, status_line = None, needs_apply = False):
    ''' If variable item is a tuple then assume that the contents are an object and a descriptor
        The descriptor should be an integer for an object of type list,
        or should be a string variable name for an object of type class/struct
    '''
    self.managed_variables = []
    adjusted_variables = []
    for v in variables:
      if len(v) > 1 and type(v[1]) == tuple:
        self.managed_variables.append((v[0],list(v[1]))+v[2:])  # v[1] must be list to allow setObj()
        desc = v[1]
        v = list(v) # so that we can change v[1]
        try:
          v[1] = self.getManaged(desc)
        except IndexError:
          continue
        #rint "Adjusted ",desc," to ",v[1]
      adjusted_variables.append(v)
    ControlDialog.__init__(self,parent,adjusted_variables,title,callonchange,status_line,needs_apply)

  def getManaged(self,desc):
    ''' Gets the ojbect being serviced by a widget using the descriptor desc which should contain an object and a interger or string '''
    #rint desc
    obj = desc[0]
    p = desc[1]
    if type(p) == int and type(obj) == list:
      return obj[p]        # return list value
    elif type(p) == str:
      return getattr(obj,p)  # return instance member
    print("ERROR: Unrecognised managed dialog field:",desc)
    raise IndexError  #return None

  def setManaged(self,desc,val):
    ''' Sets the value of the serviced object as for  getManaged()'''
    obj = desc[0]
    p = desc[1]
    if type(p) == int and type(obj) == list:
      obj[p]=val
    elif type(p) == str:
      setattr(obj,p,val)

  def change(self):
    ''' Called by gui when gui values have been changed (usually by the apply button)
        to update all the serviced objects
    '''
    for v in self.managed_variables:
      try:
        val = self.getValue(v[0])
        self.setManaged(v[1],val)
      except IndexError:
        pass

  def setObj(self, old_obj, new_obj):
    ''' Called by application when serviced object has changed either in value or identity
        - for just value the old_obj and new_obj will be the same object instance '''
    for v in self.managed_variables:
      if v[1][0] == old_obj:
        v[1][0] = new_obj
        try:
          val = self.getManaged(v[1]) # get value of new object member
        except IndexError:
          pass
        else:
          self.set(v[0],val)
          #rint "Changing ",v[0]," to value:",val

def equalList(l1,l2):
  ''' Compare the elements of two lists and returns True if they are equal'''
  #rint "List1:",l1
  #rint "List2:",l2
  if type(l1) not in (list,tuple):
    print("ERROR:L1 Not list but type:",type(l1))
    return False
  if type(l2) not in (list,tuple):
    print("ERROR:L2 Not list but type:",type(l2))
    return False
  for i in range(len(l1)):
    if l1[0] != l2[0]:
      return False
  return True

def equalObj(obj1,obj2):
  ''' Compare the values of parameters inside of two objects and returns True if their contents are equal
  '''
  if obj1 == obj2:
    return True
  # obj1 and obj2 are expected to be different objects, otherwise what is the point.
  for p in dir(obj1):
      v1 = getattr(obj1,p)
      try:
        v2 = getattr(obj2,p)
      except:
        print("Objects not equal")
        return False
      if v1 != v2:
        return False
  return True

# test code follows

def main():
  ''' Set of scaffold/unit tests'''

  def change_callback(dialog):
    dialog.change()
    print("change callback")
    # print "int_val:",var_group.int_val
    # print "float_val:",var_group.float_val
    # print "bool_val:",var_group.bool_val
    # print "str_val:",var_group.str_val
    # print "selector_val:",var_group.selector_val
    # print "list_val:",var_group.list_val
    # print "radio_val:",var_group.radio_val

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

  class var_class:
    int_val = 1
    float_val = 2.34574563
    bool_val = True
    str_val = "Hello"
    selector_options = ("Aust","B","C")
    selector_val = "B"
    list_val = [False,True,True]
    radio_val = 0

  var_group = var_class()

  class_instance = test_class()

  min_val = 1.3
  max_val = 3.4

  var_list = (("Just some text>>>",),
              ("Test button",None,test_press),
              ("Test button2",class_instance,test_press2),
              ("Test Float:",(var_group,'float_val'),None,max_val,min_val,3),
              ("Test Bool:",(var_group,'bool_val'),bool_fn),
              ("Test String:",(var_group,'str_val')),
              (("Test selector box+-",)+var_group.selector_options,(var_group,'selector_val'),selector_fn),
              (("Test list>>>","Sydney","Melbourne","Adelaide"),(var_group,'list_val'),list_fn),
              (("Test radio","One","Two","3"),(var_group,'radio_val'),radio_fn),
              ("Test Int:",(var_group,'int_val'),int_fn))
  status_line = "This is the status line"
  dialog = ManagedDialog(root,var_list,"Control Dialog Test",change_callback,status_line,False)
  frame = 0
  while not dialog.exit_request:
    dialog.update()
    dialog.lift()
    sys.stdout.flush()
    dialog.setStatusLine('%10d' % frame)
    frame += 1
  dialog.destroy()  # don't need to do this here but it is good practice

if __name__ == '__main__': 
  main()


