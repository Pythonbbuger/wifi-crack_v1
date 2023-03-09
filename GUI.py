#from aic import *
from tkinter import *
import tkinter
from tkinter import font
import tkinter.scrolledtext
from turtle import color, width
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import datetime
from tkinter import ttk
from random import randint
from SQL import WifiDatabase
from Capture import *


class Dashboard(tkinter.Tk):    
    
    def __init__(self):
        super().__init__()
        self.title("Dashboard of Wi-Fi Access Point")
        self.geometry("1920x1080")
        self.db = WifiDatabase()
        base_frame=tkinter.Frame(self)
        base_frame.pack(fill=tkinter.BOTH,expand=True)

        # Left Panel
        base_frame.columnconfigure(0, pad=30)
        base_frame.columnconfigure(1, pad=30)
        base_frame.columnconfigure(2, weight=1)
        base_frame.columnconfigure(3, pad=30)

        # Right Panel
        base_frame.columnconfigure(4, pad=30)
        base_frame.columnconfigure(5, pad=30)
        base_frame.columnconfigure(6, weight=1)
        base_frame.columnconfigure(7, pad=30)

        # Auto resize of bottom result panel
        base_frame.rowconfigure(7, weight=1)

        #title
        lbl_main_title=tkinter.Label(base_frame,text="Dashboard of Wi-Fi Access Point",font=("Arial",30))
        lbl_main_title.grid(row=0,column=0,padx=0,pady=0)

        #bar_frame
        bar_frame=tkinter.LabelFrame(base_frame,text="Bar Data",border=4,font=("Arial",10))
        bar_frame.grid(row=1,column=0,rowspan=3,columnspan=2,padx=15,pady=0,sticky=tkinter.E+tkinter.S+tkinter.N+tkinter.W)
        bar_frame.rowconfigure(0)
        
        #AP clients dict
        bar_data_dict = {"ABC":randint(0,20),"BBC":randint(0,20),"CBC":randint(0,20),"BAC":randint(0,20),"BCC":randint(0,20),"CCC":randint(0,20),"CAC":randint(0,20),"CBA":randint(0,20)}
        
        AP_name = bar_data_dict.keys()
        Client_no = bar_data_dict.values()
        
        key_list=list(AP_name)
        value_list=list(Client_no)

        max_clients_no=max(value_list)
        most_used_AP=list(AP_name)[list(Client_no).index(max_clients_no)]

        

        # create a figure
        figure = Figure(figsize=(8, 4), dpi=100,facecolor='#f0f0f0')

        # create FigureCanvasTkAgg object
        figure_canvas = FigureCanvasTkAgg(figure,master=bar_frame)


        # create axes
        axes = figure.add_subplot(111)

        # create the barchart
        axes.bar( AP_name, Client_no)
        axes.set_title('Client(s) number of AP')
        axes.set_ylabel('Number')
        axes.set_xlabel('AP name')

        figure_canvas.get_tk_widget().grid(row=0,column=0)
        
        #show how many AP are successfully cracked

        self.success_info=tkinter.LabelFrame(bar_frame)
        self.success_info.grid(row=10,column=0,columnspan=9,padx=5, pady=5,sticky=tkinter.E+tkinter.S+tkinter.W+tkinter.N)
        
        lbl_mostuseAP=tkinter.Label(self.success_info,text=f"{most_used_AP} is the most used AP nearby, there are {max_clients_no} client(s) using it now.",font=("Arial",10))
        lbl_mostuseAP.grid(row=0,column=0,sticky=tkinter.W)
        
        bar_result = str(bar_data_dict).strip('}{').replace('[', '').replace(']', '')

        lbl_bar_info=tkinter.Label(self.success_info,text=f"Client(s) number: ({bar_result})",font=("Arial",10))
        lbl_bar_info.grid(row=1,column=0,sticky=tkinter.W+tkinter.N)

        #pie_frame
  
              
        self.success_cracked_number=randint(0,20)
        self.unsuccess_cracked_number=randint(0,20)

        self.success_rate=round(self.success_cracked_number/((self.success_cracked_number+self.unsuccess_cracked_number))*100,2)

        pie_frame=tkinter.LabelFrame(base_frame,text="Pie Data",border=4,font=("Arial",10))
        pie_frame.grid(row=5,column=0,columnspan=2,padx=15,pady=0,sticky=tkinter.E+tkinter.S+tkinter.N+tkinter.W)
        pie_frame.rowconfigure(0)

        labels = ['Success' , 'Fail']
        success_number = [self.success_cracked_number,self.unsuccess_cracked_number]

        fig = Figure(figsize =(8, 3),facecolor='#f0f0f0') # create a figure object
        ax = fig.add_subplot(111) # add an Axes to the figure

        ax.pie(success_number, radius=1, labels=labels,autopct='%0.2f%%', shadow=True,)
        pie_chart = FigureCanvasTkAgg(fig,pie_frame)
        pie_chart.get_tk_widget().grid(row=0,column=0)
        
        lbf_pie=tkinter.LabelFrame(pie_frame)
        lbf_pie.grid(row=10,column=0,columnspan=8,padx=5,pady=5,sticky=tkinter.N+tkinter.S+tkinter.E+tkinter.W)

        lbl_success_cracked=tkinter.Label(lbf_pie,text=" "*5+f"Success number: {self.success_cracked_number} "+" "*45)
        lbl_success_cracked.grid(row=0,column=0,sticky=tkinter.N+tkinter.W)

        lbl_unsuccess_cracked=tkinter.Label(lbf_pie,text=f"Fail number: {self.unsuccess_cracked_number} "+" ")
        lbl_unsuccess_cracked.grid(row=0,column=2,sticky=tkinter.N+tkinter.E)
 
        lbl_success_rate=tkinter.Label(lbf_pie,text=f"Crack success rate : {self.success_rate} %"+" "*40)
        lbl_success_rate.grid(row=0,column=1,sticky=tkinter.N+tkinter.E)
        #process_frame
        
        self.process_date=f"[20/11/2022 13:24:12]"
        self.process_information=F"{self.process_date} Scanning nearby Wi-Fi Access Point... ..." 


        process_frame=tkinter.LabelFrame(base_frame,text="Process",border=3,font=("Arial",10))
        process_frame.grid(row=6,column=0,rowspan=7,columnspan=2,padx=15,pady=5,sticky=tkinter.E+tkinter.S+tkinter.W+tkinter.N)

        self.__txt_output=tkinter.scrolledtext.ScrolledText(process_frame,width=97,height=8)
        self.__txt_output.grid(row=2,column=1,columnspan=4,padx=5,sticky=tkinter.W+tkinter.N+tkinter.E+tkinter.S)
        
        self.__txt_output.insert(INSERT,f"{self.process_information}")
        #AP_frame
        AP_frame=tkinter.LabelFrame(base_frame,text="AP Info",border=4,font=("Arial",10))
        AP_frame.grid(row=1,column=2,rowspan=8,columnspan=8,padx=15,pady=0,sticky=tkinter.E+tkinter.N+tkinter.S+tkinter.W)
        
        ##lbf_time=tkinter.Frame(AP_frame)
        ##lbf_time.grid(row=0,column=4,padx=30,sticky=tkinter.N+tkinter.W+tkinter.E+tkinter.S)

       

        
        
        #https://stackoverflow.com/questions/43731784/tkinter-canvas-scrollbar-with-grid
        canvas = tkinter.Canvas(AP_frame, bg="#f0f0f0")
        canvas.grid(row=1, column=0, columnspan=4,rowspan=2,padx=30,pady=30,sticky=tkinter.N+tkinter.W+tkinter.E)

        table_frm=tkinter.Frame(AP_frame)
        table_frm.grid(row=0,column=0,columnspan=3,padx=0,pady=0,sticky=tkinter.N+tkinter.S+tkinter.W+tkinter.E)


        AP_data = [ ["2", "0","1","1"]]
              
        AP_tree = ttk.Treeview(table_frm, columns = (1,2,3,4), height = 1, show = "headings")
        AP_tree.pack(side = 'left',padx=45)
    

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview.Heading", font=(None, 20))

        AP_tree.heading(1, text="Total AP")
        AP_tree.heading(2, text="Connecting")
        AP_tree.heading(3, text="Connected")
        AP_tree.heading(4, text="Disconnected")




        AP_tree.column(1, anchor=CENTER, stretch=NO, width=220)
        AP_tree.column(2, anchor=CENTER, stretch=NO, width=260)
        AP_tree.column(3, anchor=CENTER, stretch=NO, width=200)
        AP_tree.column(4, anchor=CENTER, stretch=NO, width=200)
     


        

        for val in AP_data:
            AP_tree.insert('', 'end', values = (val[0], val[1], val[2], val[3]) )

        #Set frame quantity
        total_AP_quantiy=1
        #one AP#################################################
        if total_AP_quantiy==1:
          
          for rows in self.db.get_all_records():

            inside_frm1=tkinter.LabelFrame(canvas,text="",border=3,background='white')
            inside_frm1.pack(side=LEFT,anchor=NW)
 
            name_frm1=tkinter.Frame(inside_frm1,border=3,background='royalblue')
            name_frm1.pack(side=TOP,fill=X,expand=True)

            AP_name1=tkinter.Label(name_frm1,bg='royalblue',text="TK",font=('bold',30))
            AP_name1.grid(row=0,column=0,sticky=tkinter.W+tkinter.N)

            AP_SSID1=tkinter.Label(inside_frm1,bg='white',text=f"BSSID: {str(rows[0])} ",font=('bold',20))
            AP_SSID1.pack(side=TOP,anchor=NW,fill=NONE,expand=False)

            AP_MAC1=tkinter.Label(inside_frm1,bg='white',text=f"Encryption: {rows[3]}",font=('bold',20))
            AP_MAC1.pack(side=TOP,anchor=NW,fill=NONE,expand=False)

            AP_Status1=tkinter.Label(inside_frm1,bg='white',text=f"Signal: {rows[1]}",font=('bold',20))
            AP_Status1.pack(side=TOP,anchor=NW,fill=NONE,expand=False)

            AP_client1=tkinter.Label(inside_frm1,bg='white',text=f"Channel: {rows[2]}",font=('bold',20))
            AP_client1.pack(side=TOP,anchor=NW,fill=NONE,expand=False)

            detail_btn1=tkinter.Button(inside_frm1,border=3,text="More Details",command=self.detail)
            detail_btn1.pack(side=BOTTOM,anchor=SE,fill=NONE,expand=False)
        #two AP###############################################
        elif total_AP_quantiy==2:

           

            inside_frm1=tkinter.LabelFrame(canvas,text="",border=3,background='white')
            inside_frm1.pack(side=LEFT,anchor=NW)
 
            name_frm1=tkinter.Frame(inside_frm1,border=3,background='royalblue')
            name_frm1.pack(side=TOP,fill=X,expand=True)

            AP_name1=tkinter.Label(name_frm1,bg='royalblue',text="WiFi-PA",font=('bold',30))
            AP_name1.grid(row=0,column=0,sticky=tkinter.W+tkinter.N)

            AP_SSID1=tkinter.Label(inside_frm1,bg='white',text=f"BSSID: D8:2D:22:C1:11:21 "+" "*10,font=('bold',20))
            AP_SSID1.pack(side=TOP,anchor=NW,fill=NONE,expand=False)

            AP_MAC1=tkinter.Label(inside_frm1,bg='white',text=f"Encryption: WPA2",font=('bold',20))
            AP_MAC1.pack(side=TOP,anchor=NW,fill=NONE,expand=False)

            AP_Status1=tkinter.Label(inside_frm1,bg='white',text=f"Status: Connected",font=('bold',20))
            AP_Status1.pack(side=TOP,anchor=NW,fill=NONE,expand=False)

            AP_client1=tkinter.Label(inside_frm1,bg='white',text=f"Channel: 2",font=('bold',20))
            AP_client1.pack(side=TOP,anchor=NW,fill=NONE,expand=False)

            detail_btn1=tkinter.Button(inside_frm1,border=3,text="More Details",command=self.detail)
            detail_btn1.pack(side=BOTTOM,anchor=SE,fill=NONE,expand=False)

            #Second AP
            
            
            
            inside_frm2=tkinter.LabelFrame(canvas,text="",border=3,background='white')
            inside_frm2.pack(side=RIGHT,anchor=NE)
 
            name_frm2=tkinter.Frame(inside_frm2,border=3,background='royalblue')
            name_frm2.pack(side=TOP,fill=X,expand=True)
            
            AP_name2=tkinter.Label(name_frm2,bg='royalblue',text="TP-Link",font=('bold',30))
            AP_name2.grid(row=0,column=0,sticky=tkinter.W+tkinter.N)

            AP_SSID2=tkinter.Label(inside_frm2,bg='white',text=f"BSSID: E8:2C:12:E1:23:11 ",font=('bold',20))
            AP_SSID2.pack(side=TOP,anchor=NW,fill=NONE,expand=False)

            AP_MAC2=tkinter.Label(inside_frm2,bg='white',text=f"Encryption: WPA2",font=('bold',20))
            AP_MAC2.pack(side=TOP,anchor=NW,fill=NONE,expand=False)

            AP_Status2=tkinter.Label(inside_frm2,bg='white',text=f"Status: Disconnected",font=('bold',20))
            AP_Status2.pack(side=TOP,anchor=NW,fill=NONE,expand=False)

            AP_client2=tkinter.Label(inside_frm2,bg='white',text=f"Channel: Disconnected",font=('bold',20))
            AP_client2.pack(side=TOP,anchor=NW,fill=NONE,expand=False)

            detail_btn2=tkinter.Button(inside_frm2,border=3,text="More Details",command=self.disconnect)
            detail_btn2.pack(side=BOTTOM,anchor=SE,fill=NONE,expand=False)

        elif total_AP_quantiy==3:
            #three AP#############################################
            inside_frm1=tkinter.LabelFrame(canvas,text="",border=3,background='white')
            inside_frm1.pack(side=TOP,anchor=NW)
 
            name_frm1=tkinter.Frame(inside_frm1,border=3,background='royalblue')
            name_frm1.pack(side=TOP,fill=X,expand=True)

            AP_name1=tkinter.Label(name_frm1,bg='royalblue',text="WiFi-PA",font=('bold',30))
            AP_name1.grid(row=0,column=0,sticky=tkinter.W+tkinter.N)

            AP_SSID1=tkinter.Label(inside_frm1,bg='white',text=f"BSSID: D8:2D:22:C1:11:21 "+" "*10,font=('bold',20))
            AP_SSID1.pack(side=TOP,anchor=NW,fill=NONE,expand=False)

            AP_MAC1=tkinter.Label(inside_frm1,bg='white',text=f"Encryption: WPA2",font=('bold',20))
            AP_MAC1.pack(side=TOP,anchor=NW,fill=NONE,expand=False)

            AP_Status1=tkinter.Label(inside_frm1,bg='white',text=f"Status: Connected",font=('bold',20))
            AP_Status1.pack(side=TOP,anchor=NW,fill=NONE,expand=False)

            AP_client1=tkinter.Label(inside_frm1,bg='white',text=f"Channel: 2",font=('bold',20))
            AP_client1.pack(side=TOP,anchor=NW,fill=NONE,expand=False)

            detail_btn1=tkinter.Button(inside_frm1,border=3,text="More Details",command=self.detail)
            detail_btn1.pack(side=BOTTOM,anchor=SE,fill=NONE,expand=False)

            #Second AP

            inside_frm2=tkinter.LabelFrame(canvas,text="",border=3,background='white')
            inside_frm2.pack(side=RIGHT,anchor=NE)
 
            name_frm2=tkinter.Frame(inside_frm2,border=3,background='royalblue')
            name_frm2.pack(side=TOP,fill=X,expand=True)
            
            AP_name2=tkinter.Label(name_frm2,bg='royalblue',text="TP-Link",font=('bold',30))
            AP_name2.grid(row=0,column=0,sticky=tkinter.W+tkinter.N)

            AP_SSID2=tkinter.Label(inside_frm2,bg='white',text=f"BSSID: E8:2C:12:E1:23:11 "+" "*10,font=('bold',20))
            AP_SSID2.pack(side=TOP,anchor=NW,fill=NONE,expand=False)

            AP_MAC2=tkinter.Label(inside_frm2,bg='white',text=f"Encryption: WPA2",font=('bold',20))
            AP_MAC2.pack(side=TOP,anchor=NW,fill=NONE,expand=False)

            AP_Status2=tkinter.Label(inside_frm2,bg='white',text=f"Status:Disconnected",font=('bold',20))
            AP_Status2.pack(side=TOP,anchor=NW,fill=NONE,expand=False)

            AP_client2=tkinter.Label(inside_frm2,bg='white',text=f"Channel: Disconnected",font=('bold',20))
            AP_client2.pack(side=TOP,anchor=NW,fill=NONE,expand=False)

            detail_btn2=tkinter.Button(inside_frm2,border=3,text="More Details",command=self.disconnect)
            detail_btn2.pack(side=BOTTOM,anchor=SE,fill=NONE,expand=False)
        
            #third AP

            inside_frm3=tkinter.LabelFrame(canvas,text="",border=3,background='white')
            inside_frm3.pack(side=TOP,anchor=W)
 
            name_frm3=tkinter.Frame(inside_frm3,border=3,background='royalblue')
            name_frm3.pack(side=TOP,fill=X,expand=True)
            
            AP_name3=tkinter.Label(name_frm3,bg='royalblue',text="CW-SP",font=('bold',30))
            AP_name3.grid(row=0,column=0,sticky=tkinter.W+tkinter.N)

            AP_SSID3=tkinter.Label(inside_frm3,bg='white',text=f"BSSID: 12:E1:23:E1:23:11 "+" "*11,font=('bold',20))
            AP_SSID3.pack(side=TOP,anchor=NW,fill=NONE,expand=False)

            AP_MAC3=tkinter.Label(inside_frm3,bg='white',text=f"Encryption: WPA2",font=('bold',20))
            AP_MAC3.pack(side=TOP,anchor=NW,fill=NONE,expand=False)

            AP_Status3=tkinter.Label(inside_frm3,bg='white',text=f"Status:Disconnected",font=('bold',20))
            AP_Status3.pack(side=TOP,anchor=NW,fill=NONE,expand=False)

            AP_client3=tkinter.Label(inside_frm3,bg='white',text=f"Channel: Disconnected",font=('bold',20))
            AP_client3.pack(side=TOP,anchor=NW,fill=NONE,expand=False)

            detail_btn3=tkinter.Button(inside_frm3,border=3,text="More Details",command=self.disconnect)
            detail_btn3.pack(side=BOTTOM,anchor=SE,fill=NONE,expand=False)

        #self.timelab=tkinter.Label(lbf_time,font=("Arial",15))
        #self.timelab.grid(row=0,column=0)

        if total_AP_quantiy>4:

          scrollbar = tkinter.Scrollbar(canvas)              
          scrollbar.pack(side='right',anchor=E, fill='y')  
        
 
    

    

    def detail(self):
      newWindow = Toplevel(self)
      newWindow.title("Access Point")
      newWindow.geometry("800x600")

      name=tkinter.Label(master=newWindow, text="Wifi-PA",font=('bold',30),bg='royalblue')
      name.pack(fill=X)

      BSSID=tkinter.Label(master=newWindow, text="BSSID: D8:2D:22:C1:11:21",font=('bold',20))
      BSSID.pack(side=TOP,anchor=NW)

      Securitytype=tkinter.Label(master=newWindow, text="Security: WPA2",font=('bold',20))
      Securitytype.pack(side=TOP,anchor=NW)

      Status=tkinter.Label(master=newWindow, text="Status: Connected",font=('bold',20))
      Status.pack(side=TOP,anchor=NW)

      pwd=tkinter.Label(master=newWindow, text="Password: 12345678",font=('bold',20))
      pwd.pack(side=TOP,anchor=NW)

      signal=tkinter.Label(master=newWindow, text="Signal: 97",font=('bold',20))
      signal.pack(side=TOP,anchor=NW)

      channel=tkinter.Label(master=newWindow, text="Channel: 2",font=('bold',20))
      channel.pack(side=TOP,anchor=NW)

      destroy_btn=tkinter.Button(master=newWindow, text="Back",font=('bold',20),width=10,border=3,bg='#ADD8E6',command=newWindow.destroy)
      destroy_btn.pack(side=RIGHT,anchor=SE)

      client_table=tkinter.Frame(newWindow)
      client_table.pack(side=TOP,fill=X,anchor=SW)

      AP_data = [ ["Testing", "192.168.0.1"]]
      
      AP_tree = ttk.Treeview(client_table, columns = (1,2), height = 2, show = "headings")
      AP_tree.pack(side = 'left',padx=5)
    

      style = ttk.Style()
      style.theme_use('clam')
      style.configure("Treeview.Heading", font=(None, 10))

      AP_tree.heading(1, text="Client Name")
      AP_tree.heading(2, text="IP")
 



      AP_tree.column(1, anchor=CENTER, stretch=NO, width=300)
      AP_tree.column(2, anchor=CENTER, stretch=NO, width=300)
    
     


        

      for val in AP_data:
          AP_tree.insert('', 'end', values = (val[0], val[1]) )
      
    def disconnect(self):
        newWindow = Toplevel(self)
        newWindow.title("Access Point")
        newWindow.geometry("600x400")

        lbl=tkinter.Label(master=newWindow, text="Fail to connect!",font=('bold',30))
        lbl.pack(side=TOP)
      

    

if __name__=="__main__":
    app=Dashboard()
    #app.clock()
    app.mainloop()
