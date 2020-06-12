#-*- coding: utf-8  -*-

import os
import wx
import wx.adv
import time
import sys
import json
import requests
from threading import Thread, Lock
from eggs import cherry_forever, get_random_verse

__appname__="votes"


def json_dumps(json_data, indent=4):
    return json.dumps(json_data, indent=indent)

def call_after(func):
    def _wrapper(*args, **kwargs):
        return wx.CallAfter(func, *args, **kwargs)
    return _wrapper

class WalletTaskBarICON(wx.adv.TaskBarIcon):
    def __init__(self, frame, title=__appname__, ):
        wx.adv.TaskBarIcon.__init__(self)
        self._title = title
        self.MainFrame = frame
        #self.SetIcon(wx.Icon(get_icon_file()), self._title)  
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DCLICK, self.on_double_click)

    # override
    def CreatePopupMenu(self):
        menu = wx.Menu()
        for name, handler in self.menu_attrs():
            if not name:    # empty: add separator
                menu.AppendSeparator()
                continue
            item = wx.MenuItem(None, wx.ID_ANY, text=name, kind=wx.ITEM_NORMAL) 
            menu.Append(item)
            self.Bind(wx.EVT_MENU, handler, item)
        return menu

    def menu_attrs(self):
        return (
            ('关于', self.on_about), 
            ('退出', self.on_exit)
        )

    def on_about(self, event):
        wx.MessageBox('程序作者：{}\n软件描述：{}'.format(__author__, __description__), "关于")

    def on_exit(self, event):
        wx.Exit()

    def on_double_click(self, event):
        if self.MainFrame.IsIconized():
            self.MainFrame.Iconize(False)

        if not self.MainFrame.IsShown():
            self.MainFrame.Show(True)
        self.MainFrame.Raise()


class MainFrame(wx.Frame):
    _FRAMES_MIN_SIZE = (900, 600)
    _BASIC_TITLE = "投票情况"
    API_BUTTON_CLICK_EVENT_PREFIX_ = "api_button_on_click_"

    def __init__(self, *args, **kwargs):
        super(MainFrame, self).__init__(*args, **kwargs)
        # Set taskBarIcon
        self.taskbar_icon = WalletTaskBarICON(frame=self, title=self._BASIC_TITLE)
        #default testnet
        self.title_write('{}'.format(self._BASIC_TITLE))
        self.layout_mainframe()

    def _on_close(self, event):
        self._window_hide_flag = False
        dlg = wx.MessageDialog(self, "是否隐藏到状态盘？(状态盘双击打开)", "退出", wx.YES_NO | wx.ICON_QUESTION)
        self._window_hide_flag = dlg.ShowModal() == wx.ID_YES
        dlg.Destroy()
        self.close()

    def close(self):
        if self._window_hide_flag:
            self.Hide()
        else:
            # self.taskbar_icon.on_exit(wx.EVT_MENU)
            self.taskbar_icon.Destroy()
            self.Destroy()

    def status_bar_write(self, msg=""):
        self.status_bar.SetStatusText(msg)

    def title_write(self, title=_BASIC_TITLE):
        self.SetTitle(title)

    def layout_mainframe(self):
        super().__init__(parent=None)


        self.SetSize(size=self._FRAMES_MIN_SIZE)
        self.Center()

        sp_window = wx.SplitterWindow(parent=self, id=-1)
        self.panel_left = wx.Panel(parent=sp_window, name="Wallet")
        self.panel_right = wx.Panel(parent=sp_window, name="Commands")

        # 设置左右布局的分割窗口self.panel_left和self.panel_right
        sp_window.SplitVertically(self.panel_left, self.panel_right, 1)

        # 为self.panel_right面板设置一个布局管理器
        # default static_text
        self.right_boxsizer = wx.BoxSizer(wx.VERTICAL)
        self.panel_right.SetSizer(self.right_boxsizer)

        # label and label BoxSizer | 水平
        self.right_label_BoxSizer = wx.BoxSizer()
        self.api_label = wx.StaticText(self.panel_right, style=wx.ALIGN_CENTER, label='钱包命令')
        # self.right_label_BoxSizer.Add(self.api_label, proportion=1, flag=wx.EXPAND|wx.ALL|wx.ALIGN_CENTER, border=3)
        self.right_label_BoxSizer.Add(self.api_label)

        # param_list and param_list BoxSizer | 垂直
        self.right_param_BoxSizer = wx.BoxSizer(wx.VERTICAL)

        # Buttons | 水平
        self.right_buttons_BoxSizer = wx.BoxSizer(wx.VERTICAL)
        self.api_button_ok = wx.Button(self.panel_right, label='执行')
        self.right_buttons_BoxSizer.Add(self.api_button_ok, flag=wx.ALIGN_RIGHT, border=3)

        # result
        self.right_output_BoxSizer = wx.BoxSizer()
        self.output_text = wx.TextCtrl(self.panel_right, size=(1000, 768), style=wx.TE_MULTILINE|wx.HSCROLL|wx.TE_RICH|wx.TE_PROCESS_ENTER)
        self.right_output_BoxSizer.Add(self.output_text, proportion=0, flag=wx.EXPAND|wx.ALL, border=3)

        # layout
        self.panel_right.SetSizer(self.right_boxsizer)
        self.right_boxsizer.Add(self.right_label_BoxSizer, flag=wx.EXPAND|wx.ALL, border=3)
        self.right_boxsizer.Add(self.right_param_BoxSizer, flag=wx.EXPAND|wx.ALL, border=3)
        self.right_boxsizer.Add(self.right_buttons_BoxSizer, flag=wx.EXPAND|wx.ALL, border=3)
        self.right_boxsizer.Add(self.right_output_BoxSizer, flag=wx.EXPAND|wx.ALL, border=3)

        self.status_bar = self.CreateStatusBar()
        # Bind extra events
        self.Bind(wx.EVT_CLOSE, self._on_close)
        
        self.title_update_thread()
 
    def title_update_thread(self):
        self._thread = Thread(target = self.run, args = ())
        self._thread.daemon = True
        self._thread.start()
        self.started = True

    def run(self):
        while True:
            try:
                if self.sdk:
                    head_block_number = self.sdk.info()['head_block_number']
                    block_msg = "区块高度：{}".format(head_block_number)
                    if self.sdk.wallet:
                        if self.sdk.wallet.created():
                            if self.sdk.wallet.locked():
                                title_msg = "{} | 钱包已锁定".format(block_msg)
                            else:
                                title_msg = "{} | 钱包已解锁".format(block_msg)
                        else:
                            title_msg = "{} | 钱包未创建".format(block_msg)
                    else:
                        title_msg = "钱包初始化失败"
                else:
                    title_msg = "SDK 初始化失败"
            except Exception as e:
                title_msg = repr(e)
            self.updateDisplay(title_msg)
            self.status_bar_write(get_random_verse())
            time.sleep(2)

    @call_after
    def updateDisplay(self, msg):
        title = '{} | {}'.format(self._BASIC_TITLE, msg)
        self.SetTitle(title)


    def gen_param_column(self, parent_panel, label_tip):
        boxsizer = wx.BoxSizer() # 水平: [label, input]
        param_label = wx.StaticText(parent_panel, label=label_tip[0])
        boxsizer.Add(param_label, proportion=2, flag=wx.EXPAND|wx.ALL, border=3)
        param_input_text = wx.TextCtrl(parent_panel, value=label_tip[1])
        boxsizer.Add(param_input_text, proportion=8, flag=wx.EXPAND|wx.ALL, border=3)
        return boxsizer, param_input_text

    def button_api_layout(self, is_hide=False):
        if is_hide:
            self.api_button_ok = wx.Button(self.panel_right, label='执行')
            self.right_buttons_BoxSizer.Add(self.api_button_ok, flag=wx.ALIGN_RIGHT, border=3)
        else:
            self.right_boxsizer.Hide(self.right_buttons_BoxSizer)

    def param_columns_layout(self, api_name):
        # clear param BoxSizer
        self.right_boxsizer.Hide(self.right_param_BoxSizer)
        # self.right_boxsizer.Hide(self.right_buttons_BoxSizer)
        self.right_boxsizer.Layout()


        # if api_name not in API_CLASS:
            # self.right_buttons_BoxSizer.Add(self.api_button_ok, flag=wx.ALIGN_RIGHT, border=3)

        if api_name in API_LIST:
            api_obj = API_LIST[api_name]
            # log_manager.log("params: {}".format(api_obj["params"]))
            params = api_obj["params"]
            for i in range(0, len(params)):
                column_text = "param{}_input_text".format(i+1)
                boxsizer, input_text = self.gen_param_column(self.panel_right, params[i])
                self.right_param_BoxSizer.Add(boxsizer, flag=wx.EXPAND|wx.ALL, border=3)
                setattr(self, column_text, input_text)
            
        self.right_boxsizer.Layout()

    def func_egg(self, event):
        text = get_random_verse()
        self.show_output_text(text)

    def show_output_text(self, text, is_clear_text=True):
        # log_manager.log("text: {}".format(text))
        if is_clear_text:
            self.output_text.Clear()
        self.output_text.AppendText(text+'\n')
        # self.output_text.AppendText('\n')


    def api_button_on_click_JSON_Format(self, event):
        json_text = self.output_text.GetValue().strip()
        button_label = self.api_button_ok.GetLabel()
        text = ""
        new_label = "执行"
        try: 
            json_obj = json.loads(json_text)
            if button_label == "执行":
                new_label = "压缩"
                text = json_dumps(json_obj)
            elif button_label == "压缩":
                text = json_dumps(json_obj, indent=None)
                text = text.replace("\\", "")
        except Exception as e:
            text = "{}\n error: {}".format(json_text, repr(e))
        self.api_button_ok.SetLabel(new_label)
        self.show_output_text(text)

 
class App(wx.App):
    def OnInit(self):
        frame = MainFrame()
        frame.Show()
        return True
 
    def OnExit(self):
        return 0
 
def Main():
    app = App()
    app.MainLoop()
 
if __name__ == '__main__':
    Main()

