#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx  
class MyFrame( wx.Frame ):  
    def __init__( self, parent, id, title ):  
        wx.Frame.__init__(self,parent,id,title,wx.DefaultPosition,wx.Size(300, 250))  
          
        self.formula = False  
          
        menubar = wx.MenuBar()  
        file = wx.Menu()  
        file.Append( 22, '&Quit', 'Exit Calculator' )  
        menubar.Append( file, '&File' )  
        self.SetMenuBar( menubar )  
          
        wx.EVT_MENU( self, 22, self.OnClose )  
        sizer = wx.BoxSizer( wx.VERTICAL )  
          
        self.display = wx.TextCtrl(self, -1, '', style=wx.TE_RIGHT)  
        sizer.Add(self.display, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 4)  
        gs = wx.GridSizer(4, 4, 3, 3)  
        gs.AddMany([(wx.Button(self, 20, 'Cls'), 0, wx.EXPAND),  
        (wx.Button(self, 21, 'Bck'), 0, wx.EXPAND),  
        (wx.StaticText(self, -1, ''), 0, wx.EXPAND),  
        (wx.Button(self, 22, 'Close'), 0, wx.EXPAND),  
        (wx.Button(self, 1, '7'), 0, wx.EXPAND),  
        (wx.Button(self, 2, '8'), 0, wx.EXPAND),  
        (wx.Button(self, 3, '9'), 0, wx.EXPAND),  
        (wx.Button(self, 4, '/'), 0, wx.EXPAND),  
        (wx.Button(self, 5, '4'), 0, wx.EXPAND),  
        (wx.Button(self, 6, '5'), 0, wx.EXPAND),  
        (wx.Button(self, 7, '6'), 0, wx.EXPAND),  
        (wx.Button(self, 8, '*'), 0, wx.EXPAND),  
        (wx.Button(self, 9, '1'), 0, wx.EXPAND),  
        (wx.Button(self, 10, '2'), 0, wx.EXPAND),  
        (wx.Button(self, 11, '3'), 0, wx.EXPAND),  
        (wx.Button(self, 12, '-'), 0, wx.EXPAND),  
        (wx.Button(self, 13, '0'), 0, wx.EXPAND),  
        (wx.Button(self, 14, '.'), 0, wx.EXPAND),  
        (wx.Button(self, 15, '='), 0, wx.EXPAND),  
        (wx.Button(self, 16, '+'), 0, wx.EXPAND)])  
        sizer.Add(gs, 1, wx.EXPAND)  
        self.SetSizer(sizer)  
        self.Centre()  
        wx.EVT_BUTTON(self, 20, self.OnClear)  
        wx.EVT_BUTTON(self, 21, self.OnBackspace)  
        wx.EVT_BUTTON(self, 22, self.OnClose)  
        wx.EVT_BUTTON(self, 1, self.OnSeven)  
        wx.EVT_BUTTON(self, 2, self.OnEight)  
        wx.EVT_BUTTON(self, 3, self.OnNine)  
        wx.EVT_BUTTON(self, 4, self.OnDivide)  
        wx.EVT_BUTTON(self, 5, self.OnFour)  
        wx.EVT_BUTTON(self, 6, self.OnFive)  
        wx.EVT_BUTTON(self, 7, self.OnSix)  
        wx.EVT_BUTTON(self, 8, self.OnMultiply)  
        wx.EVT_BUTTON(self, 9, self.OnOne)  
        wx.EVT_BUTTON(self, 10, self.OnTwo)  
        wx.EVT_BUTTON(self, 11, self.OnThree)  
        wx.EVT_BUTTON(self, 12, self.OnMinus)  
        wx.EVT_BUTTON(self, 13, self.OnZero)  
        wx.EVT_BUTTON(self, 14, self.OnDot)  
        wx.EVT_BUTTON(self, 15, self.OnEqual)  
        wx.EVT_BUTTON(self, 16, self.OnPlus)  
      
    def OnClear(self, event):  
        self.display.Clear()  
    def OnBackspace(self, event):  
        formula = self.display.GetValue()  
        self.display.Clear()  
        self.display.SetValue(formula[:-1])  
    def OnClose(self, event):  
        self.Close()  
    def OnDivide(self, event):  
        if self.formula:  
            return  
        self.display.AppendText('/')  
    def OnMultiply(self, event):  
        if self.formula:  
            return  
        self.display.AppendText('*')  
    def OnMinus(self, event):  
        if self.formula:  
            return  
        self.display.AppendText('-')  
    def OnPlus(self, event):  
        if self.formula:  
            return  
        self.display.AppendText('+')  
    def OnDot(self, event):  
        if self.formula:  
            return  
        self.display.AppendText('.')  
    def OnEqual(self, event):  
        if self.formula:  
            return  
        formula = self.display.GetValue()  
        self.formula = True  
        try:  
            self.display.Clear()  
            output = eval(formula)  
            self.display.AppendText(str(output))  
        except StandardError:  
            self.display.AppendText("Error")  
    def OnZero(self, event):  
        if self.formula:  
            self.display.Clear()  
            self.formula = False  
            self.display.AppendText('0')  
    def OnOne(self, event):  
        if self.formula:  
            self.display.Clear()  
            self.formula = False  
            self.display.AppendText('1')  
    def OnTwo(self, event):  
        if self.formula:  
            self.display.Clear()  
            self.formula = False  
            self.display.AppendText('2')  
    def OnThree(self, event):  
        if self.formula:  
            self.display.Clear()  
            self.formula = False  
            self.display.AppendText('3')  
    def OnFour(self, event):  
        if self.formula:  
            self.display.Clear()  
            self.formula = False  
            self.display.AppendText('4')  
    def OnFive(self, event):  
        if self.formula:  
            self.display.Clear()  
            self.formula = False  
            self.display.AppendText('5')  
    def OnSix(self, event):  
        if self.formula:  
            self.display.Clear()  
            self.formula = False  
            self.display.AppendText('6')  
    def OnSeven(self, event):  
        if self.formula:  
            self.display.Clear()  
            self.formula = False  
            self.display.AppendText('7')  
    def OnEight(self, event):  
        if self.formula:  
            self.display.Clear()  
            self.formula = False  
            self.display.AppendText('8')  
    def OnNine(self, event):  
        if self.formula:  
            self.display.Clear()  
            self.formula = False  
            self.display.AppendText('9')  
  
class MyApp(wx.App):  
    def OnInit(self):  
        frame = MyFrame(None, -1, "calculator.py")  
        frame.Show(True)  
        self.SetTopWindow(frame)  
        return True  
app = MyApp(0)  
app.MainLoop()  

'''
import wx
app = wx.App()
win = wx.Frame(None,title = "编辑器", size=(410,335))
bkg = wx.Panel(win)

loadButton = wx.Button(bkg, label = '打开')
saveButton = wx.Button(bkg, label = '保存')
filename = wx.TextCtrl(bkg)
contents = wx.TextCtrl(bkg, style = wx.TE_MULTILINE | wx.HSCROLL)

hbox = wx.BoxSizer()
hbox.Add(filename, proportion =1, flag = wx.EXPAND)
hbox.Add(loadButton, proportion =0,flag = wx.LEFT, border = 5)
hbox.Add(saveButton, proportion =0,flag = wx.LEFT, border = 5)

vbox = wx.BoxSizer(wx.VERTICAL)
vbox.Add(hbox,proportion = 0,flag = wx.EXPAND | wx.ALL, border = 5)
vbox.Add(contents, proportion = 1,flag=wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, border = 5)

bkg.SetSizer(vbox)
win.Show()
app.MainLoop()

'''
'''
# First things, first. Import the wxPython package.
import wx

# Next, create an application object.
app = wx.App()

# Then a frame.
frm = wx.Frame(None, title="Hello World")

# Show it.
frm.Show()

# Start the event loop.
app.MainLoop()




import wx

class HelloFrame(wx.Frame):
    """
    A Frame that says Hello World
    """

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(HelloFrame, self).__init__(*args, **kw)

        # create a panel in the frame
        pnl = wx.Panel(self)

        # put some text with a larger bold font on it
        st = wx.StaticText(pnl, label="Hello World!")
        font = st.GetFont()
        font.PointSize += 10
        font = font.Bold()
        st.SetFont(font)

        # and create a sizer to manage the layout of child widgets
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(st, wx.SizerFlags().Border(wx.TOP|wx.LEFT, 25))
        pnl.SetSizer(sizer)

        # create a menu bar
        self.makeMenuBar()

        # and a status bar
        self.CreateStatusBar()
        self.SetStatusText("Welcome to wxPython!")


    def makeMenuBar(self):
        """
        A menu bar is composed of menus, which are composed of menu items.
        This method builds a set of menus and binds handlers to be called
        when the menu item is selected.
        """

        # Make a file menu with Hello and Exit items
        fileMenu = wx.Menu()
        # The "\t..." syntax defines an accelerator key that also triggers
        # the same event
        helloItem = fileMenu.Append(-1, "&Hello...\tCtrl-H",
                "Help string shown in status bar for this menu item")
        fileMenu.AppendSeparator()
        # When using a stock ID we don't need to specify the menu item's
        # label
        exitItem = fileMenu.Append(wx.ID_EXIT)

        # Now a help menu for the about item
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        # Make the menu bar and add the two menus to it. The '&' defines
        # that the next letter is the "mnemonic" for the menu item. On the
        # platforms that support it those letters are underlined and can be
        # triggered from the keyboard.
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        # Give the menu bar to the frame
        self.SetMenuBar(menuBar)

        # Finally, associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        # activated then the associated handler function will be called.
        self.Bind(wx.EVT_MENU, self.OnHello, helloItem)
        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)


    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)


    def OnHello(self, event):
        """Say hello to the user."""
        wx.MessageBox("Hello again from wxPython")


    def OnAbout(self, event):
        """Display an About Dialog"""
        wx.MessageBox("This is a wxPython Hello World sample",
                      "About Hello World 2",
                      wx.OK|wx.ICON_INFORMATION)


if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = HelloFrame(None, title='Hello World 2')
    frm.Show()
    app.MainLoop()

'''

'''
class DeriveThread():
    def __init__(self, name, do_action):
        self.name = name
        self.do_action = do_action



def info():
    print("==================")

thread = DeriveThread("aa", info())
thread.do_action

'''

