#!/usr/bin/env python
#Create GUI for mm by Wxpython
try:
    import wx
except:
    print "wx model not found, please download and install it from http://www.wxpython.org/download.php#stable"
    quit()
import wx.aui as aui
import wx.lib.sized_controls as sc
try:
    from PIL import Image
except:
    print "Pillow model not found, please download and install it from https://pypi.python.org/pypi/Pillow/"
    quit()
import struct,socket,os,subprocess,math,sys,re,time
from wx.lib.embeddedimage import PyEmbeddedImage
from wx.lib.wordwrap import wordwrap
import telnetlib

#-----------------ID define--------------------
ID_NEW = wx.NewId()
ID_OPEN = wx.NewId()
ID_SAVE = wx.NewId()
ID_SAVEAS = wx.NewId()
ID_CLOSE = wx.NewId()
ID_EXIT = wx.NewId()
ID_REFRESH = wx.NewId()
ID_RUN = wx.NewId()
ID_SETTINGS = wx.NewId()
ID_ABOUT = wx.NewId()
ID_ToolbarNew = wx.NewId()
ID_ToolbarOpen = wx.NewId()
ID_ToolbarSave = wx.NewId()
ID_ToolbarRefresh = wx.NewId()
ID_ToolbarAuto = wx.NewId()
ID_FirstDevice = ID_REFRESH+1000
popupID1 = wx.NewId()
popupID2 = wx.NewId()
popupID3 = wx.NewId()
popupID4 = wx.NewId()
popupID5 = wx.NewId()
popupID6 = wx.NewId()
popupID7 = wx.NewId()
popupID8 = wx.NewId()
popupID9 = wx.NewId()
ID_PaneBorderSize = wx.ID_HIGHEST + 1
ID_SashSize = ID_PaneBorderSize + 1
ID_CaptionSize = ID_PaneBorderSize + 2
ID_BackgroundColor = ID_PaneBorderSize + 3
ID_SashColor = ID_PaneBorderSize + 4
ID_InactiveCaptionColor =  ID_PaneBorderSize + 5
ID_InactiveCaptionGradientColor = ID_PaneBorderSize + 6
ID_InactiveCaptionTextColor = ID_PaneBorderSize + 7
ID_ActiveCaptionColor = ID_PaneBorderSize + 8
ID_ActiveCaptionGradientColor = ID_PaneBorderSize + 9
ID_ActiveCaptionTextColor = ID_PaneBorderSize + 10
ID_BorderColor = ID_PaneBorderSize + 11
ID_GripperColor = ID_PaneBorderSize + 12
template = """\
type= monkey script
count = 1
speed = 1.0
start data >>
"""
icon = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAACCpJ"
    "REFUWIXll3twnFUZxn/v9327SXaT7G42l82l3bRJmjZtkxahQAUspZ1axmK5VKsRGKWgqKOM"
    "o+IfOoOjdOrIgIwUL6MWBgtaBSkDDrYMUC7TQmlTCr3aJjSXXrIx3Vy3u993zvGP3dw6VfKn"
    "M74z356Zb78573Oe8573eQ78v4cYY8y0vzYGRAADCEopRATLsjDGgIAYQASlNbZlXXIa5bnY"
    "jg9jzPQAjH0iImhjMEph2wJiT3yDQYyAgNYay7IYHHV5/eXtjJ7+AAewS2bR/MkV1MVr0Fph"
    "WfbHAzDGICK5EUAAGHVh3949NNbPpqysbDypMQbLEjo6z7L90a/RkHqdfMfG7wvg+CK0e7Op"
    "XPlVlq+6Ec91p8+AiOB6muTgINse/wnFbg97jia54sZW7ryjFc/1cHxZWocvePzxx60s1i9z"
    "3L+CskVrCYcKsRJt1PS/xf4uPzPXb6Rl8WU4H5MZnUt+6qOP2PnM43R29hC78A5L5vsIVxag"
    "EgdQ3I7P78fzPBzH4VDbXuZkXuVU/iKu+foW6qrDuQlv5diOX7Jg5EmO7HmehYsvx5rIZcZH"
    "YwwYgxHQWgHQdfIwZd4pCjJnSMbWssP9AjNr8mkJdPDCll9wYP8+7NwWiIBRPqRoDnXVYbRy"
    "cd0MRivC89eQ0h4l3jn6Rz2s8YSA8rxcsWXrHAMiFiJC+8kORpTDuttW8ammAPrCMGIpTqcN"
    "ld5HHN/1DP0DwwDMX3Q5ibJPU5Q4wDNP/BbX2NiWAyIUlVbTnQkx6LkE83JFmAVgEMkSogzY"
    "wjil+/a+y/6/PsSVzXX0DlzgikUNBAqDWJkkr7x1mGikmKGUof6m+5lRVQYYus8m2LflPvJ6"
    "D+Eu/S5r1t2eO34OXR0nyAsEKa+ozDIgkl3prtde4503dvDKs1vwlMoyYQztbW+wblkjs2tK"
    "aIxHsS2NaA+XfGZWlHDgg2Mk7GoqykrwXJdMxqUmVs7CL26ivCKCr2MXI67GdhyMgRmzGiiv"
    "qMIYcESEVCrFo5seIJ04ybwlKyg1Z1BG8NsWiBAqDqLNefL9NtVlASyfxZ62Y9TGChmNNLLw"
    "tjVcedXSXDVN9AY93IsaOY0pb8FvC0ZrsCy01gggloUopczDP9uI07uf0kgx/0oHGD7fx80b"
    "7qPpsqUYrUn0nqX9xUeJBiA56vJG2wmWXz2f4uIAR9ramLl4Fb12Bf5QBaJdtJsimG9jvf0D"
    "EoMWczdsIx6Po41GLJtchSEITsrTlNqD5Bf7iZUVUWsJiaIizIl/0BGppLa2lvJYFcdjn2Dn"
    "U4+RTMOMljiRaIQXt7/ADfFRitr/Qk/3ICeSEMyzaKyu4FhXF/5IEcu//TTRimq0VtkVM9HM"
    "AMRobY58eIDjb24jGgpS6DfUxiLsfmcfp/oN9zy4Ba08lNbs+vuzdB19H2ekk4GO91hap4iE"
    "/XjKR3GgEL8vgEgALQXkCexNBlhy728I5DnjBY7IpPQgWmsjIoymPdLpNMrNcL63hxc3rWdl"
    "UxVd9Xey+tbWKf3pta0/p/LkQ/iKI7iZNDhx+geTlAQGMcaPZTto5WMgA433vkQ4WjmWLtfO"
    "J8IREbTWBPIcAnkOEKSkJELLjfeQPvIkBYe28pzxc+2Kz9CX6KXv8E669mwjY1ssiAq9/Ybi"
    "cCHGF2Eo1Ua40EVpgy/YTMe5BNH+ASKlVWilsGwLw6UYQLJqlhMdYzSe2Px584PE2p8gr7CE"
    "jnQpRd4pAsNH8cdXcvB8lKvtnQRDIY6etpk/ez4nuj+kOQ5DQ5popJa8/Bq2t2s++/3NRAoL"
    "svRfRMEUMZqsfMYojOWw9XebkT2bqIsqOqkn0nwLV63ZgIfNlgfupkm/Re8QNM6spKsvRV2w"
    "h4N9JQz5SlgzJ83ZZJDk4m+xeu06PM/DdpwpDEwRownZFcBGtOKODd9gq6+Ac36b5avXUx7O"
    "yxoTDLd886c8d/916PwSpC+DI37agp9j4dovUVLVyO5HVtAUOst5L8NYtx0zM5cEcDEIg4XR"
    "itY7vzL+v1Ze9jiJRaQ8RmNDNaOpNB+csWhpirPuR5vxA11n+slzbEYyivKZDYgIgiAGjExU"
    "wiU90xQmxEZ5Hp7nZd9ZNgbh3d1vk7mQotNpwTfSTdjrxgmE0Z6HUoqO93ZQH+hG/H5CoRBa"
    "KXI9P2vbcnFp05YDkR3Bchxsx0GprDS/tP1v/H7jdzj4/MNUBg0D4euIFtlYgSj5joMycOjt"
    "7Zw+7zHk5VMRK8OybWzbznnHiS34jwCmgMk9Y6z0dHURLy1AvBEWrN5AdM4SQlaS4uqmrCMa"
    "HCQ+p5kPU81EG1bx+vNPsfGH3yPR25vdRq3H5/7vjmhSGExOzQytX76LvXPnUVvXQGmsmmPP"
    "3k80GqaoqhEQTh7cjd1/nPpl6+kZ7CGiDtFz+AjJgUHKysuZ7AKnxUAOQfZHwEuniNdUUDtr"
    "Fq8+dg8L/O9jQrOYUTcPEUN1XRMy7xZubr2b6NxrePPQOa5avZ76hvqsElqTtWCa9wKDQXkK"
    "x3F4+g+/5v2df+L6G67n9NH3yJzbT8uym1hy16+wtMopHmil8JSirz9JVWzqysdqbNpbgGHc"
    "dneeOEqsLMyp9n+y8por6Bq5lroVd2AZjRHBaJWz5zZ+26YqVj5+DxhbzFhMHwDkjKogxqMm"
    "ZONEo4xULePyuc0Ei8NZvRdr3EmNHefsiq0pF5yxmH4NSBa5JbBszec5PBzBDc1h4ZLrssm1"
    "xhIr22jGu2k22cXPlGmnfzc0k5zyxCSe5yJiTTrjXKR3/+Pxb9ksx/x5efwJAAAAAElFTkSu"
    "QmCC")

class AdbException(Exception):
    def __init__(self, message, id):
        if message.startswith('error: more than one device and emulator'):
            message = (message.strip() + """

            More than one connected Android device and/or emulator detected.
            Please pass an id to android.connect() or use the --serial option of
            runtests.py. Examples:

            a1=android.connect(id='019617680601302D')
            a2=android.connect(id='0196166B11033023')

            or

            python runtests.py --serial 019617680601302D mytest.py
            """)
        else:
            message = '%s (id=%s)' % (message.strip(), id)
        Exception.__init__(self, message)

class adb:
    def __init__(self,id):
        self.id=id
        self.s=socket.socket()
        self.s.settimeout(5.0)
        self.s.connect(('127.0.0.1',5037))
        self.xfer('host:transport-any' if id is None else
                ('host:transport:%s' % id))

    def close(self):
        self.s.close()

    def xfer(self, command):
        self.s.sendall('%04x%s' % (len(command), command))
        result=self.s.recv(4)
        if result == 'OKAY':
            return self
        if result == 'FAIL':
            raise AdbException('error: ' + self.s.recv(
                    int(self.s.recv(4),16)), self.id)
        raise AdbException('FAIL: %s' % repr(result), self.id)

    def read(self,n):
        b=''
        while len(b) < n:
            _ = self.s.recv(n-len(b))
            if len(_) is 0:
                self.s.close()
                break
            b += _
        return b

def screenshot(id):
    """ Take a screen shot, saving it to 'filename' """
    stream = adb(id).xfer('framebuffer:')
    version = struct.unpack('<I', stream.read(4))[0]
    if version == 16:
        # Cupcake-style, without a header
        bpp=version
        size, width, height = struct.unpack('<3I', stream.read(12))
        r_off,r_len,g_off,g_len,b_off,b_len,a_off,a_len=11,5,5,6,0,5,0,0
    elif version == 1:
        bpp,size,width,height,r_off,r_len,g_off,g_len,b_off,b_len,a_off,a_len=struct.unpack('<12I',stream.read(48))
    else:
        raise Exception('Unsupported DDMS_RAWINFO_VERSION: %d' % version)
    data=stream.read(size)
    stream.close()

    is_bgr = (r_off > b_off)

    try:
        """ PIL has problems parsing these BMPs, so we can't just do:

                import PIL.ImageFile
                p=PIL.ImageFile.Parser()
                p.feed(BMP+DIB+data)
                p.close().save(filename)
        """
        import PIL.Image
        modes=(	{16:('BGR;16'), 24:('BGR'), 32:('BGRX')} if is_bgr else
                {16:('RGB;16'), 24:('RGB'), 32:('RGBX')})
        return PIL.Image.fromstring('RGB', (width, height), data,
                    'raw', modes[bpp])
    except ImportError:
        raise Exception('a.device.screenshot requires the PIL module to save to this format on this device. Please download and install PIL from http://www.pythonware.com/products/pil/')

class TextEditor(wx.TextCtrl):
    def __init__(self, parent, id=-1, value=wx.EmptyString, pos=wx.DefaultPosition, 
                 size=wx.DefaultSize, style=0,cwd = '' ):
        wx.TextCtrl.__init__(self, parent, id, value, pos, size, style, validator = wx.DefaultValidator, name = wx.TextCtrlNameStr)
        self.path = cwd
        self.origin = value
        
    def IsNeedSave(self):
        if self.origin != self.GetValue():
            return True
        else:
            return False

class SettingsPanel(wx.Panel):
    def __init__(self, parent, frame):
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition,
                          wx.DefaultSize)

        self._frame = frame
        
        vert = wx.BoxSizer(wx.VERTICAL)

        s1 = wx.BoxSizer(wx.HORIZONTAL)
        self._border_size = wx.SpinCtrl(self, ID_PaneBorderSize, "", wx.DefaultPosition, wx.Size(50,20))
        s1.Add((1, 1), 1, wx.EXPAND)
        s1.Add(wx.StaticText(self, -1, "Operating interval:"))
        s1.Add(self._border_size)
        s1.Add((1, 1), 1, wx.EXPAND)
        s1.SetItemMinSize(1, (180, 20))
        
        grid_sizer = wx.GridSizer(0, 2)
        grid_sizer.SetHGap(1)
        grid_sizer.Add(s1)
        grid_sizer.Add((1, 1))


        cont_sizer = wx.BoxSizer(wx.VERTICAL)
        cont_sizer.Add(grid_sizer, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(cont_sizer)
        self.GetSizer().SetSizeHints(self)
        

    def CreateColorBitmap(self, c):
        image = wx.EmptyImage(25, 14)
        
        for x in xrange(25):
            for y in xrange(14):
                pixcol = c
                if x == 0 or x == 24 or y == 0 or y == 13:
                    pixcol = wx.BLACK
                    
                image.SetRGB(x, y, pixcol.Red(), pixcol.Green(), pixcol.Blue())
            
        return image.ConvertToBitmap()

class RunPanel(sc.SizedDialog):
    def __init__(self, parent, id ,script):
        sc.SizedDialog.__init__(self, None, -1, "Running ...", 
                        style=wx.DEFAULT_DIALOG_STYLE )
        
        pane = self.GetContentsPane()
        pane.SetSizerType("form")
        
        wx.StaticText(pane, -1, "Runing script:")
        wx.StaticText(pane, -1, script)
        
        wx.StaticText(pane, -1, "Run For (1-10000):")
        nestedPane = sc.SizedPanel(pane, -1)
        nestedPane.SetSizerType("horizontal")
        nestedPane.SetSizerProps(expand=True)
        self.textCtrl = wx.SpinCtrl(nestedPane, -1, "",(30, 50))
        self.textCtrl.SetRange(1,10000)
        choices = wx.Choice(nestedPane, -1, choices=["times", "hours"])
        choices.SetSelection(0)
        
        wx.CheckBox(pane, -1, "Checking Memory Leak").Enable(False)
        
        self.choice = "times"
        self.text = "1"
        self.SetButtonSizer(self.CreateStdDialogButtonSizer(wx.OK | wx.CANCEL))
        self.Fit()
        self.SetMinSize(self.GetSize())
        self.Bind(wx.EVT_CHOICE, self.OnChoice, choices)
        self.Bind(wx.EVT_TEXT, self.OnType, self.textCtrl)
        
    def OnChoice(self,event):
        self.choice = event.GetString()
        
    def OnType(self, event):
        try:
            int(self.textCtrl.GetValue())
        except:
            dlg = wx.MessageDialog(self, 'Only number is available here!',
                               'Error',
                               wx.OK | wx.ICON_ERROR
                               #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                               )
            dlg.ShowModal()
            dlg.Destroy()
            self.textCtrl.SetValue(int(event.GetString()[:-1]))
        else:
            self.text = int(self.textCtrl.GetValue())
        event.Skip()

class DurationDialog(sc.SizedDialog):
    def __init__(self, parent):
        sc.SizedDialog.__init__(self, None, -1, "Dragging ...", 
                        style=wx.DEFAULT_DIALOG_STYLE )
        
        pane = self.GetContentsPane()
        pane.SetSizerType("form")
        
        wx.StaticText(pane, -1, "Dragging duration(1000 - 5000 ms)")
        self.textCtrl = wx.SpinCtrl(pane, -1, "",(30, 50))
        self.textCtrl.SetRange(1000,5000)
        self.text = "1000"
        self.SetButtonSizer(self.CreateStdDialogButtonSizer(wx.OK | wx.CANCEL))
        self.Fit()
        self.SetMinSize(self.GetSize())
        self.Bind(wx.EVT_TEXT, self.OnType, self.textCtrl)
        
    def OnType(self, event):
        try:
            int(self.textCtrl.GetValue())
        except:
            dlg = wx.MessageDialog(self, 'Only number is available here!',
                               'Error',
                               wx.OK | wx.ICON_ERROR
                               #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                               )
            dlg.ShowModal()
            dlg.Destroy()
            self.textCtrl.SetValue(int(event.GetString()[:-1]))
        else:
            self.text = int(self.textCtrl.GetValue())
        event.Skip()
        
class Device:
    def __init__(self, id):
        self.id = id
        if self.shell('cd /sdcard-ext').stdout.read().find("No such file or directory") == -1 and self.shell('cd /sdcard-ext').stdout.read().find("Permission denied") == -1:
            self.local = '/sdcard-ext/'
        elif self.shell('cd /sdcard').stdout.read().find("No such file or directory") == -1: 
            self.local = '/sdcard/'
        else:
            raise Exception('sdcard can not find, is it available?')
            quit()
        self.shell('monkey --port 5230')
        tcp = 'adb -s %s forward tcp:5230 tcp:5230'%self.id
        subprocess.Popen(tcp.split(' '), stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
        
    def __del__(self):
        host = '127.0.0.1'
        port = 5230
        self.tn = telnetlib.Telnet(host,port)
        self.tn.write('quit\n')
        self.tn.close()

    def shell(self, command):
        adbcommand = 'adb -s %s shell' % self.id
        commandlist = (adbcommand).split(' ')
        a = subprocess.Popen(commandlist, stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
        command = command+"\nexit\n"
        a.stdin.write(command)
        return a
        
    def monkey(self, filename, choice , number):
        pushcommand = 'adb -s %s push filename %s'%(self.id,self.local)
        pushcommand = pushcommand.split(' ')
        pushcommand[4] = filename
        print pushcommand
        subprocess.Popen(pushcommand, stdout = subprocess.PIPE, stderr = subprocess.STDOUT).wait()
        if choice == "times":
            loops = number
        elif choice == "hours":
            loops = self.calcloopNumber(filename,number)
        casename = os.path.split(filename)[1]
        shelllocal = self.generateSh(casename,loops)
        pushshell = 'adb -s %s push filename %s'%(self.id,self.local)
        pushshell = pushshell.split(' ')
        pushshell[4] = shelllocal
        subprocess.Popen(pushshell, stdout = subprocess.PIPE, stderr = subprocess.STDOUT).wait()
        self.shell('sh %smonkey.sh&'%self.local)
        logfolder = self.local+'result-'+casename
        return logfolder
        
    def action(self, action):
        host = '127.0.0.1'
        port = 5230
        self.tn = telnetlib.Telnet(host,port)
        self.tn.write(action+'\n')
        time.sleep(2)
        self.tn.write('done\n')
        self.tn.close()
        return
    
    def generateSh(self,casename,loop):
        content = """\
mkdir {local}result-{casename} ; logcat -c;logcat -v threadtime -f {local}result-{casename}/logcat.log & monkey --bugreport -v -v --monitor-native-crashes --ignore-security-exceptions --kill-process-after-error -f {local}{casename} {loop} > {local}result-{casename}/monkey.log 2>&1;kill -9 $! >/dev/null 2>&1 &
"""
        content = content.format(casename = casename,loop = loop,local = self.local)
        fp = open(os.path.join(os.path.dirname(sys.argv[0]),"monkey.sh"),"w")
        fp.write(content)
        fp.close()
        
        return os.path.join(os.path.dirname(sys.argv[0]),"monkey.sh")
        
    def calcloopNumber(self,filename,hours):
        fp = open(filename)
        lines = fp.readlines()
        oper =0
        wait =0
        p = re.compile("Dispatch.*")
        q = re.compile("UserWait\((\d*)\)")
        for line in lines:
            if p.search(line) != None:
                oper+=1
            w = q.search(line)
            if w != None:
                wait += int(w.group(1))
        if oper + wait == 0:
            return 1
        else:
            loop = int(hours) * 3600 /(((oper/2*500)+wait)/1000)
            return loop
        
    
class PyAUIFrame(wx.Frame):
    def __init__(self, id=-1, title="", pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE |
                                            wx.SUNKEN_BORDER |
                                            wx.CLIP_CHILDREN):

        wx.Frame.__init__(self, None, id, title, pos, size, style)
        self.newfilelist = []
        self._mgr = aui.AuiManager()
        self._mgr.SetManagedWindow(self)
        self.SetIcon(icon.GetIcon())
        self.CreateMenuBar()
        tb_bmp1 = wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, wx.Size(16, 16))
        tb_bmp2 = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, wx.Size(16, 16))
        tb_bmp3 = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_TOOLBAR, wx.Size(16, 16))
        tb_bmp4 = wx.ArtProvider.GetBitmap(wx.ART_HELP_SIDE_PANEL, wx.ART_TOOLBAR, wx.Size(16, 16))
        tb_bmp5 = wx.ArtProvider.GetBitmap(wx.ART_REPORT_VIEW, wx.ART_TOOLBAR, wx.Size(16, 16))
        
        tb1 = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,wx.TB_FLAT | wx.TB_NODIVIDER )
        tb1.SetToolBitmapSize(wx.Size(16, 16))
        tb1.AddTool(ID_ToolbarNew,  tb_bmp1)
        tb1.AddTool(ID_ToolbarOpen,  tb_bmp2)
        tb1.AddTool(ID_ToolbarSave,  tb_bmp3)
        tb1.Realize()
        
        tb2 = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,wx.TB_FLAT | wx.TB_NODIVIDER | wx.TB_HORZ_TEXT)
        tb2.SetToolBitmapSize(wx.Size(16, 16))
        tb2.AddLabelTool(ID_ToolbarRefresh, "Refresh", tb_bmp4)
        tb2.Realize()
        
        self.tb3 = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,wx.TB_FLAT | wx.TB_NODIVIDER | wx.TB_HORZ_TEXT)
        self.tb3.SetToolBitmapSize(wx.Size(16, 16))
        self.tb3.AddCheckLabelTool(ID_ToolbarAuto, "Auto-Refresh", tb_bmp5)
        self.tb3.Realize()
        
        self._mgr.AddPane(self.CreateImageView(), aui.AuiPaneInfo().
                          Name("pic_content").Caption("Screen capturer").CaptionVisible(False).MinSize(wx.Size(360,640)).Resizable(False).
                          Left().CloseButton(False).MaximizeButton(False))
        self._mgr.AddPane(self.CreateNotebook(), aui.AuiPaneInfo().
                          Name("text_content").Caption("Text Editor").CaptionVisible(False).BestSize(wx.Size(500,640)).
                          Right().CloseButton(False).MaximizeButton(False))
        self._mgr.AddPane(tb1, aui.AuiPaneInfo().Name("tb1").ToolbarPane().Top().Fixed().Floatable(False))
        self._mgr.AddPane(tb2, aui.AuiPaneInfo().Name("tb2").ToolbarPane().Top().Fixed().Floatable(False))
        self._mgr.AddPane(self.tb3, aui.AuiPaneInfo().Name("tb3").ToolbarPane().Top().Fixed().Floatable(False))      
        
        self._mgr.AddPane(SettingsPanel(self, self), aui.AuiPaneInfo().
                          Name("settings").Caption("Settings").Resizable(False).
                          Dockable(False).Float().Hide().CloseButton(True).MaximizeButton(True))
        
        self._mgr.GetPane("pic_content").Show().Left().Layer(1).Row(0).Position(0)
        self._mgr.GetPane("text_content").Show().Center().Layer(0).Row(0).Position(0)
        self.statusbar = self.CreateStatusBar(2, wx.ST_SIZEGRIP)
        self.statusbar.SetStatusWidths([-2, -3])
        self.statusbar.SetStatusText("Ready", 0)
        self.statusbar.SetStatusText("Welcome To use Monkey Master 2.0!", 1)
        self.screenshot.Bind(wx.EVT_MOTION,self.OnEnterImage)
        self.screenshot.Bind(wx.EVT_LEAVE_WINDOW,self.OnLeaveImage)
        self.screenshot.Bind(wx.EVT_RIGHT_UP,self.OnRightClickImage)
        
        self.Bind(aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.OnPageClose)
        self.Bind(wx.EVT_MENU, self.OnRefreshImage, id=ID_ToolbarRefresh)
        self.Bind(wx.EVT_MENU, self.OnNewFile, id=ID_ToolbarNew)
        self.Bind(wx.EVT_MENU, self.OnNewFile, id=ID_NEW)
        self.Bind(wx.EVT_MENU, self.OnOpenFile, id=ID_ToolbarOpen)
        self.Bind(wx.EVT_MENU, self.OnOpenFile, id=ID_OPEN)
        self.Bind(wx.EVT_MENU, self.OnSaveAsFile, id=ID_SAVEAS)
        self.Bind(wx.EVT_MENU, self.OnSave, id=ID_SAVE)
        self.Bind(wx.EVT_MENU, self.OnSave, id=ID_ToolbarSave)
        self.Bind(wx.EVT_MENU, self.OnClose, id = ID_CLOSE)
        self.Bind(wx.EVT_MENU, self.updateDeviceMenu, id=ID_REFRESH)
        self.Bind(wx.EVT_MENU, self.OnSettings ,id = ID_SETTINGS)
        self.Bind(wx.EVT_MENU, self.OnRunning, id = ID_RUN)
        self.Bind(wx.EVT_MENU, self.OnAbout, id = ID_ABOUT)
        self.Bind(wx.EVT_MENU, self.OnExit, id = ID_EXIT)
        self.Bind(wx.EVT_MENU_RANGE, self.OnSelectDevice, id=ID_FirstDevice, id2=ID_FirstDevice+10)
        
        self._mgr.Update()
        
    def getDevices(self):
        dev_list=[]
        os.popen("adb start-server")
        files=os.popen("adb devices")
        for i in files:
            if "device" in i and "devices" not in i:
                devid=i.split()[0]
                ro_name=os.popen("adb -s "+devid+" shell getprop ro.product.model")
                dev_list.append((" ".join([devid, ro_name.read().strip()])))
                ro_name.close()
        files.close()
        return dev_list
        
    def updateDeviceMenu(self,event):
        for item in self.device_menu.GetMenuItems():
            self.device_menu.RemoveItem(item)
        self.dev_list = self.getDevices()
        self.device_menu.Append(ID_REFRESH, "Refresh")
        self.device_menu.AppendSeparator()
        if self.dev_list == []:
            self.device_menu.Append(ID_FirstDevice+0, "No Device")
            self.device_menu.Enable(ID_FirstDevice+0, False)
            self.dev = None
        else:
            pos = 0
            if not hasattr(self, "dev") or self.dev == None: 
                self.dev = Device(self.dev_list[0].split()[0]) 
            for dev in self.dev_list:
                pos += 1 
                self.device_menu.AppendRadioItem(ID_FirstDevice+pos, dev)
                if self.dev.id == dev.split()[0]:
                    self.device_menu.FindItemById(ID_FirstDevice+pos).Check(True)
                
    def OnSelectDevice(self, event):
        id =  self.device_menu.GetLabel(id = event.GetId()).split()[0]
        self.dev = Device(id)
        self.OnRefreshImage(event)
        
    def CreateImageView(self):
        if self.dev != None:
            pil = screenshot(self.dev.id)
        else:
            bgcolor = (192,192,192) 
            pil = Image.new('RGB',(360,640),bgcolor)
        image = wx.EmptyImage(pil.size[0], pil.size[1])
        image.SetData(pil.convert('RGB').tostring())
        assert image.IsOk()== True
        y = image.GetHeight()
        self.scale = 640.0/y
        rescale = image.Rescale(360 ,640)
        new_png = rescale.ConvertToBitmap()
        self.screenshot = wx.StaticBitmap(self, -1, new_png, (0, 0), (new_png.GetWidth(), new_png.GetHeight()))
        return self.screenshot
        
    def CreateNotebook(self):
        client_size = self.GetClientSize()
        self.ctrl = aui.AuiNotebook(self, -1, wx.Point(client_size.x, client_size.y),
                              wx.Size(430, 200))
        art = aui.AuiSimpleTabArt()
        self.ctrl.SetArtProvider(art)
        self.filecount = 1
        #self.page_bmp = wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, wx.Size(16, 16))
        
        self.ctrl.AddPage(TextEditor(self.ctrl, -1, template, wx.DefaultPosition, wx.DefaultSize,
                                 wx.TE_MULTILINE|wx.NO_BORDER,''), "File"+str(self.filecount), True)
        
        self.newfilelist.append(self.ctrl.GetSelection())
        return self.ctrl

    def CreateMenuBar(self):
        # create menu
        mb = wx.MenuBar()

        file_menu = wx.Menu()
        file_menu.Append(ID_NEW,"New")
        file_menu.Append(ID_OPEN,"Open")
        file_menu.Append(ID_SAVE,"Save")
        file_menu.Append(ID_SAVEAS,"Save as ..")
        file_menu.Append(ID_CLOSE,"Close")
        file_menu.AppendSeparator()
        file_menu.Append(ID_EXIT, "Exit")
        
        self.device_menu = wx.Menu()
        self.device_menu.Append(ID_REFRESH,"Refresh")
        self.device_menu.AppendSeparator()
        self.updateDeviceMenu(None)
        
        run_menu = wx.Menu()
        run_menu.Append(ID_RUN,"Run")
        
        setting_menu = wx.Menu()
        setting_menu.Append(ID_SETTINGS,"Settings")
        setting_menu.Enable(ID_SETTINGS, False)
        help_menu = wx.Menu()
        help_menu.Append(ID_ABOUT,"About")
    
        mb.Append(file_menu,"&File")
        mb.Append(self.device_menu,"&Device")
        mb.Append(run_menu,"&Run")
        mb.Append(setting_menu,"&Settings")
        mb.Append(help_menu,"&Help")
        
        self.SetMenuBar(mb)
        
    def OnNewFile(self,event):
        self.filecount += 1
        pagename = "File"+str(self.filecount)
        self.ctrl.AddPage(TextEditor(self.ctrl, -1, template, wx.DefaultPosition, wx.DefaultSize,
                                 wx.TE_MULTILINE|wx.NO_BORDER,''), pagename, True)
        self.newfilelist.append(self.ctrl.GetSelection())
        
    def OnEnterImage(self,event):
        pos = event.GetPosition()
        pos_x = round(pos.x/self.scale)
        pos_y = round(pos.y/self.scale)
        x_y = "("+str(pos_x)+','+str(pos_y)+")"
        self.statusbar.SetStatusText(x_y, 0)
    
    def OnLeaveImage(self,event):
        self.statusbar.SetStatusText("Ready", 0)
        
    def OnRefreshImage(self, event):
        if self.dev != None:
            pil = screenshot(self.dev.id)
        else:
            bgcolor = (192,192,192) 
            pil = Image.new('RGB',(360,640),bgcolor)
        image = wx.EmptyImage(pil.size[0], pil.size[1])
        image.SetData(pil.convert('RGB').tostring())
        assert image.IsOk()== True
        y = image.GetHeight()
        self.scale = 640.0/y
        rescale = image.Rescale(360 ,640)
        new_png = rescale.ConvertToBitmap()
        self.screenshot.SetBitmap(new_png)
        
    def OnRightClickImage(self,event):
        self.currentpos = event.GetPosition()
        if not hasattr(self, "IsDragging"):
            self.IsDragging = False

        self.Bind(wx.EVT_MENU, self.OnTapandRefresh, id=popupID1)
        self.Bind(wx.EVT_MENU, self.OnLongTapandRefresh, id=popupID2)
        self.Bind(wx.EVT_MENU, self.OnDragStart, id=popupID3)
        self.Bind(wx.EVT_MENU, self.OnDragEndandRefresh, id=popupID4)
        self.Bind(wx.EVT_MENU, self.OnPressBack, id=popupID5)
        self.Bind(wx.EVT_MENU, self.OnPressHome, id=popupID6)
        self.Bind(wx.EVT_MENU, self.OnPressMenu, id=popupID7)
        self.Bind(wx.EVT_MENU, self.OnPressPower, id=popupID8)
            
        popupmenu = wx.Menu()
        popupmenu.Append(popupID1, "Tap")
        popupmenu.Append(popupID2, "Long Tap")
        popupmenu.Append(popupID3, "Drag Start")
        popupmenu.Append(popupID4, "Drag End")
        submenu = wx.Menu()
        submenu.Append(popupID5, "Back")
        submenu.Append(popupID6, "Home")
        submenu.Append(popupID7, "Menu")
        popupmenu.AppendMenu(popupID9, "Press Hardkey", submenu)
        popupmenu.Append(popupID8, "Wakeup Screen")
        
        if not self.IsDragging:
            popupmenu.Enable(popupID1, True)
            popupmenu.Enable(popupID2, True)
            popupmenu.Enable(popupID3, True)
            popupmenu.Enable(popupID4, False)
            popupmenu.Enable(popupID9, True)
        else:
            popupmenu.Enable(popupID1, False)
            popupmenu.Enable(popupID2, False)
            popupmenu.Enable(popupID3, False)
            popupmenu.Enable(popupID4, True)
            popupmenu.Enable(popupID9, False)
            
        self.PopupMenu(popupmenu)
        popupmenu.Destroy()
    
    def OnTapandRefresh(self, event):
        x,y = self.currentpos.x/self.scale , self.currentpos.y/self.scale
        index = self.ctrl.GetSelection()
        textctrl = self.ctrl.GetPage(index)
        textctrl.SetInsertionPointEnd()
        textctrl.WriteText(" DispatchPointer(0,0,0,%d,%d,0,0,0,0,0,0,0)\n"% (x,y))
        textctrl.WriteText(" DispatchPointer(100,0,1,%d,%d,0,0,0,0,0,0,0)\n"% (x,y))
        textctrl.WriteText(" UserWait(%d)\n"% 2000)
        action = "tap %d %d"% (x,y)
        if self.tb3.GetToolState(ID_ToolbarAuto):
            self.dev.action(action)
            self.OnRefreshImage(event)

    def OnLongTapandRefresh(self, event):
        x,y = self.currentpos.x/self.scale , self.currentpos.y/self.scale
        index = self.ctrl.GetSelection()
        textctrl = self.ctrl.GetPage(index)
        textctrl.SetInsertionPointEnd()
        textctrl.WriteText(" DispatchPointer(0,0,0,%d,%d,0,0,0,0,0,0,0)\n"% (x,y))
        textctrl.WriteText(" UserWait(%d)\n"% 1500)
        textctrl.WriteText(" DispatchPointer(100,0,1,%d,%d,0,0,0,0,0,0,0)\n"% (x,y))
        textctrl.WriteText(" UserWait(%d)\n"% 2000)
        action = "touch down %d %d\n"% (x,y)
        action += "sleep %d\n"% 1500
        action += "touch up %d %d"% (x,y)
        if self.tb3.GetToolState(ID_ToolbarAuto):
            self.dev.action(action)
            self.OnRefreshImage(event)
        
    def OnDragStart(self,event):
        self.dragstartx = self.currentpos.x/self.scale
        self.dragstarty = self.currentpos.y/self.scale
        self.IsDragging = True
        
    def OnDragEndandRefresh(self,event):
        dlg = DurationDialog(self)
        dlg.CenterOnScreen()

        # this does not return until the dialog is closed.
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            dura = int(dlg.text)
            dlg.Destroy()
            self.IsDragging = False
            self.dragendx = self.currentpos.x/self.scale
            self.dragendy = self.currentpos.y/self.scale
            index = self.ctrl.GetSelection()
            textctrl = self.ctrl.GetPage(index)
            textctrl.SetInsertionPointEnd()
            gaps = 0
            points = self.CalcDragPoint(self.dragstartx,self.dragstarty,self.dragendx,self.dragendy)
            duration = int(dura/(len(points)+1))
            textctrl.WriteText(" DispatchPointer(%d,0,0,%d,%d,0,0,0,0,0,0,0)\n"% (gaps,self.dragstartx,self.dragstarty))
            action = "touch down %d %d\n"% (self.dragstartx,self.dragstarty)
            textctrl.WriteText(" UserWait(%d)\n"% duration)
            action += "sleep %d\n"% duration
            for x,y in points:
                gaps += 100
                textctrl.WriteText(" DispatchPointer(%d,0,2,%d,%d,0,0,0,0,0,0,0)\n"% (gaps,x,y))
                action += "touch move %d %d\n"% (x,y)
                textctrl.WriteText(" UserWait(%d)\n"% duration)
                action += "sleep %d\n"% duration
            gaps += 100
            textctrl.WriteText(" DispatchPointer(%d,0,1,%d,%d,0,0,0,0,0,0,0)\n"% (gaps,self.dragendx,self.dragendy))
            action += "touch up %d %d\n"% (self.dragendx,self.dragendy)
            textctrl.WriteText(" UserWait(%d)\n"% 2000)
            if self.tb3.GetToolState(ID_ToolbarAuto):
                self.dev.action(action)
                self.OnRefreshImage(event)
        else:
            dlg.Destroy()
            

        
    def CalcDragPoint(self,x1,y1,x2,y2):
        k = (y2-y1)/(x2-x1)
        alpha = math.atan(k)
        x0 = 30*math.cos(alpha)
        y0 = 30*math.sin(alpha)
        n = abs(int((x2-x1)/x0))
        points = []
        if x1 <= x2:
            for i in range(n):
                xn = x1 + (i+1)*x0
                yn = y1 + (i+1)*y0
                points.append([xn,yn])
        elif x1 > x2:
            for i in range(n):
                xn = x1 - (i+1)*x0
                yn = y1 - (i+1)*y0
                points.append([xn,yn])
        return points
    
    def OnPressBack(self,event):
        index = self.ctrl.GetSelection()
        textctrl = self.ctrl.GetPage(index)
        textctrl.SetInsertionPointEnd()
        textctrl.WriteText(" DispatchKey(0,0,0,4,0,0,0,0)\n")
        textctrl.WriteText(" DispatchKey(100,0,1,4,0,0,0,0)\n")
        textctrl.WriteText(" UserWait(%d)\n"% 2000)
        action = "press 4"
        if self.tb3.GetToolState(ID_ToolbarAuto):
            self.dev.action(action)
            self.OnRefreshImage(event)
            
    def OnPressHome(self,event):
        index = self.ctrl.GetSelection()
        textctrl = self.ctrl.GetPage(index)
        textctrl.SetInsertionPointEnd()
        textctrl.WriteText(" DispatchKey(0,0,0,3,0,0,0,0)\n")
        textctrl.WriteText(" DispatchKey(100,0,1,3,0,0,0,0)\n")
        textctrl.WriteText(" UserWait(%d)\n"% 2000)
        action = "press 3"
        if self.tb3.GetToolState(ID_ToolbarAuto):
            self.dev.action(action)
            self.OnRefreshImage(event)
            
    def OnPressMenu(self,event):
        index = self.ctrl.GetSelection()
        textctrl = self.ctrl.GetPage(index)
        textctrl.SetInsertionPointEnd()
        textctrl.WriteText(" DispatchKey(0,0,0,82,0,0,0,0)\n")
        textctrl.WriteText(" DispatchKey(100,0,1,82,0,0,0,0)\n")
        textctrl.WriteText(" UserWait(%d)\n"% 2000)
        action = "press 82"
        if self.tb3.GetToolState(ID_ToolbarAuto):
            self.dev.action(action)
            self.OnRefreshImage(event)

    def OnPressPower(self,event):
        action = "wake"
        self.dev.action(action)
        self.OnRefreshImage(event)
            
    def OnOpenFile(self, evt):
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=os.path.join(os.path.dirname(sys.argv[0]),'scripts'),
            defaultFile="",
            wildcard= "TXT file (*.txt)|*.txt",
            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
            )

        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()

            for path in paths:
                fp = open ( path, 'r' )
                content = fp.read()
                self.ctrl.AddPage(TextEditor(self.ctrl, -1, content, wx.DefaultPosition, wx.DefaultSize,
                         wx.TE_MULTILINE|wx.NO_BORDER, path), os.path.split(path)[1], True)
                fp.close()
        dlg.Destroy()
        
    def OnSaveAsFile(self, evt):
        dlg = wx.FileDialog(
            self, message="Save file as ...", 
            defaultDir=os.path.join(os.path.dirname(sys.argv[0]),'scripts'), 
            defaultFile="", wildcard="TXT file (*.txt)|*.txt", style=wx.SAVE
            )

        dlg.SetFilterIndex(2)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            index = self.ctrl.GetSelection()
            textctrl = self.ctrl.GetPage(index)
            self.ctrl.SetPageText(index,os.path.split(path)[1])
            textctrl.path = path
            data = textctrl.GetValue()
            
            fp = file(path, 'w')
            fp.write(data)
            fp.close()
            textctrl.origin = textctrl.GetValue()
            
        dlg.Destroy()
    
    def OnSave(self,evt):
        index = self.ctrl.GetSelection()
        textctrl = self.ctrl.GetPage(index)
        if textctrl.path == '':
            self.OnSaveAsFile(evt)
        else:
            data = textctrl.GetValue()
            fp = file(textctrl.path, 'w') 
            fp.write(data)
            fp.close()
            textctrl.origin = textctrl.GetValue()
            
    def OnClose(self,event):
        index = self.ctrl.GetSelection()
        page = self.ctrl.GetPage(index)
        if page.IsNeedSave():
            res = wx.MessageBox("Your script has not saved yet!!\nCLOSE ANYWAY?",
                                "Warning", wx.YES_NO, self)
            if res == wx.YES:
                self.ctrl.DeletePage(index)
        else:        
            self.ctrl.DeletePage(index)
        
    def OnPageClose(self,event):
        index = event.GetEventObject().GetSelection()
        page = event.GetEventObject().GetPage(index)
        if page.IsNeedSave():
            res = wx.MessageBox("Your script has not saved yet!!\nCLOSE ANYWAY?",
                                "Warning", wx.YES_NO, self)
            if res != wx.YES:
                event.Veto()

        
    def OnSettings(self, event):

        #floating_pzane = self._mgr.GetPane("settings").Float().Show()

        self._mgr.Update()
        
    def OnRunning(self, event):
        index = self.ctrl.GetSelection()
        title = self.ctrl.GetPageText(index)
        page = self.ctrl.GetPage(index)
        if page.path != '' and page.IsNeedSave() == False and isinstance(self.dev,Device):
            dlg = RunPanel(self, -1,title)
            dlg.CenterOnScreen()
    
            # this does not return until the dialog is closed.
            val = dlg.ShowModal()
            if val == wx.ID_OK:
                filename = self.ctrl.GetPage(index).path
                choice = dlg.choice
                number = dlg.text
                logfolder = self.dev.monkey(filename, choice, number)
                dlg.Destroy()
                notice = wx.MessageDialog(self, 'You script is running in offline mode!!\nYou can disconnect your phone now.\n\nLogs will be stored to %s/' % logfolder,
                   'Start',
                   wx.OK | wx.ICON_INFORMATION
                   #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                   )
                notice.ShowModal()
                notice.Destroy()
            else:
                dlg.Destroy()
    
        else:
            message = 'You must select an available device!!' if not isinstance(self.dev,Device) else 'You must save your script before running!!'
            dlg = wx.MessageDialog(self, message,
                   'Error',
                   wx.OK | wx.ICON_ERROR
                   #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                   )
            dlg.ShowModal()
            dlg.Destroy()
            
    def OnAbout(self, event):
        # First we create and fill the info object
        info = wx.AboutDialogInfo()
        info.Name = "Monkey Master"
        info.Version = "2.0.3"
        info.Copyright = "(C) 2012 Motorola Mobility Corporation"
        info.Description = wordwrap(
            "\"Monkey Master\" program is a cross-platform GUI Tool for android test.\n"
            "It can be used on both user and userdebug release.\n"
            "Based on Google monkey tool. \nDesigned for Stability&&Memory test. \n\n"
            
            "Evolve from monkey master 1.X\n"
            "Specially thanks Hao Xi(hcr387), Xu Yimin(pwj674)'s contribution to this tool.\n"
            "Motorola Mobility -- China System Test, CT458"
            ,
            350, wx.ClientDC(self))
        info.WebSite = ("https://sites.google.com/a/motorola.com/ct458-automation/auto-tools-release/mm20", "Monkey Master home page")
        info.Developers = [ "Wang Xuanyu (xwm763)" ]

        #info.License = wordwrap(licenseText, 500, wx.ClientDC(self))

        # Then we call wx.AboutBox giving it that info object
        wx.AboutBox(info)
        
    def OnExit(self, event):
        self.Close()

if __name__ == '__main__':
    app = wx.App()
    frame = PyAUIFrame(wx.ID_ANY, "MonkeyMaster 2.0", size=(800, 750))
    frame.Show()
    app.MainLoop()
