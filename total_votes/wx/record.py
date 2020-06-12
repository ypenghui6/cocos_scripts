
pip3 install -U wxPython


左边钱包命令列表
        # self.tree = self.create_TreeCtrl(self.panel_left)
        # self.Bind(wx.EVT_TREE_SEL_CHANGING, self.wallet_tree_on_click, self.tree)
        # left_boxsizer.Add(self.tree, 9, flag=wx.EXPAND | wx.ALL, border=3)

选择所要使用的链
		# self.chain_boxsizer = self.gen_chain_BoxSizer(self.panel_left)        

	def gen_chain_BoxSizer(self, parent):
        chain_staticBox = wx.StaticBox(parent, label=u'请选择您使用的链: ')
        chain_boxsizer = wx.StaticBoxSizer(chain_staticBox, wx.VERTICAL)
        # self.testnetCheck = wx.RadioButton(chain_staticBox, -1, TESTNET_CHAIN, style=wx.RB_GROUP) 
        # self.mainnetCheck = wx.RadioButton(chain_staticBox, -1, MAINNET_CHAIN) 
        # self.customizeCheck = wx.RadioButton(chain_staticBox, -1, CUSTOMIZE_CHAIN) 

        # default = "{},{}".format(CHAIN_CONFIG[CUSTOMIZE_CHAIN]["address"], FAUCET_CONFIG[CUSTOMIZE_CHAIN])
        # self.customizeChainText = wx.TextCtrl(chain_staticBox, value=default, size=(180, 20))

        # self.customizeCheck.Bind(wx.EVT_RADIOBUTTON, self.on_customize_chain) 
        # self.testnetCheck.Bind(wx.EVT_RADIOBUTTON, self.on_testnet_chain) 
        # self.mainnetCheck.Bind(wx.EVT_RADIOBUTTON, self.on_mainnet_chain) 

        # chain_boxsizer.Add(self.mainnetCheck, proportion=0, flag=wx.EXPAND|wx.ALL, border=3)
        # chain_boxsizer.Add(self.testnetCheck, proportion=0, flag=wx.EXPAND|wx.ALL, border=3)
        # chain_boxsizer.Add(self.customizeCheck, proportion=0,flag=wx.EXPAND|wx.ALL, border=3)
        # chain_boxsizer.Add(self.customizeChainText, proportion=0,flag=wx.EXPAND|wx.ALL, border=3)
        return chain_boxsizer


设置左边布局

	    # 设置最小窗格大小，左右布局指左边窗口大小
        # sp_window.SetMinimumPaneSize(80)

        # 为self.panel_left面板设置一个布局管理器
        # left_boxsizer = wx.BoxSizer(wx.VERTICAL)
        # self.panel_left.SetSizer(left_boxsizer)

        # self.chain_boxsizer = self.gen_chain_BoxSizer(self.panel_left)

        # left_boxsizer.Add(self.chain_boxsizer, 1, flag=wx.EXPAND | wx.ALL, border=3)

        # sp_window = wx.SplitterWindow(parent=self, id=-1)
        # self.panel_right = wx.Panel(parent=sp_window, name="Commands")


设置app图标
		# Set the app icon
        '''
        app_icon_path = get_icon_file()
        if app_icon_path is not None:
            self.app_icon = wx.Icon(app_icon_path, wx.BITMAP_TYPE_ICO)
            self.SetIcon(self.app_icon)
        '''

