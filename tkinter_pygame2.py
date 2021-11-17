import pygame
from copy import *
from pygame.locals import *
import tkinter
import tkinter.messagebox as tkMessageBox
import sys   # for exit and arg

# initialise
pygame.init()
ScreenSize = (200,100)
pygame.display.set_caption("Pygame tkinter Demo 1 - Robert Parker (c2009)")
Surface = pygame.display.set_mode(ScreenSize)

testMode = 0

def Draw():
  global view_surface, centres
  #Clear view
  Surface.fill((80,80,80))
  pygame.display.flip()

def refreshDraw():
  Draw()

def about_callback():
  t1 = "Pygame Meets tkinter by Robert Parker (c)2009"
  t2 = "Pygame is python interface to SDL media layer indended for game creation but used for much more (ref. www.pygame.com)"
  t3 = "tkinter is based on Tk GUI toolkit developed by Scriptics (http://www.scriptics.com) (formerly developed by Sun Labs)."
  t4 = "Thanks to Fredrik Lundh 'An introduction to tkinter' (c)1999"
  about_text = t1 + "\n" + t2 + "\n"+ t3 + "\n" + t4
  tkMessageBox.showinfo("ABOUT",about_text)

def GetInput():

  for event in pygame.event.get():
    global status_mode, status_str, Done
    if event.type == QUIT:
      if tkMessageBox.askokcancel("Quit", "Do you really wish to quit?"):
        Done = True
      #return True
    if event.type == KEYDOWN:
    #   print event
    #   print event.key
    #   print event.unicode
      status_mode = True
      if type(event.unicode) == chr:
        status_str = "Key %c[%3d]"%(event.unicode,event.key)
      else:
        status_str = "Key [%3d]"%(event.key,)
      #keystate = pygame.key.get_pressed()
      keymod = pygame.key.get_mods()
    if event.type == MOUSEBUTTONDOWN:
      print(event.button)
  keystate = pygame.key.get_pressed()
  return False

def tk_key_event(event):
  ''' transfer key event in tkinter dialog to pygame event handler'''
  print(event.keycode, event.keysym, event.keysym_num)
  trans_dict = { 192:96,107:270,109:269,107:270,109:269,37:276,39:275,38:273,40:274,45:277,36:278,33:280,46:127,35:279,34:281 }
  if trans_dict.has_key(event.keycode):
    code = trans_dict[event.keycode]
  else:
    code = event.keycode
  pygame.event.post(pygame.event.Event(KEYDOWN,{'key':code,'unicode':event.keysym}))

Done = False

def quit_callback():
  global main_dialog, Done
  if tkMessageBox.askokcancel("Quit", "Do you really wish to quit?"):
    Done = True

def main():
  global status_mode, status_str, main_dialog

  menu_design = (("Help",
                    (("About",about_callback),
                    )
                 ),
                )
  status_str = "Status"
  fps_str = "FPS"

  root = tkinter.Tk()
  root.protocol("WM_DELETE_WINDOW", quit_callback)
  main_dialog =  tkinter.Frame(root)
  root.title("Test dialog")
  status_line = tkinter.Label(main_dialog, text=status_str, bd=1, relief=tkinter.SUNKEN, anchor=tkinter.W)
  status_line.pack(side=tkinter.BOTTOM, fill=tkinter.X)
  main_dialog.pack()
#   main_dialog.bind('', tk_key_event)
  menubar = tkinter.Menu(root)
  menubar.add_command(label="About", command=about_callback)
  root.config(menu=menubar)


  clock = pygame.time.Clock()
  # lets get some performance statistics
  gameframe = 0
  ticks = pygame.time.get_ticks()

  status_mode=  False  # show FPS for the moment

  main_dialog_status_str = ""
  while not Done:
    try:
      main_dialog.update()
    except:
      print("dialog error")
    if status_str != main_dialog_status_str:
      main_dialog_status_str = status_str
      status_line.config(text=status_str)  #format % args)
      status_line.update_idletasks()

    if GetInput():  # input event can also comes from diaglog
      break
    Draw()
    clock.tick(100) # slow it to something slightly realistic
    gameframe += 1

    # display stats in pygame title bar and in tk window status line
    if gameframe % 10 == 0:
      t = pygame.time.get_ticks()
      fps = (float(10)*1000.0)/(t-ticks)
      ticks = t
      #rint "TestMode#%d fps: %.2f over %d frames" % (testMode,fps,gameframe)
      period = 1.0/fps
      fps_str = "%5.1f FPS"%fps
      pygame.display.set_caption(fps_str)
    if not status_mode:
      status_str = fps_str
    if gameframe % 100 == 0:
      sys.stdout.flush()
      ticks = pygame.time.get_ticks() # don't include stdout time in frame period


#   print("Average fps: %.2f over %d frames" % ((float(gameframe)*1000.0)/(pygame.time.get_ticks()-ticks),gameframe))
  main_dialog.destroy()

if __name__ == '__main__': 
    main()