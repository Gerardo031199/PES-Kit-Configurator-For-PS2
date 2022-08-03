import os
import pymem
import pymem.process
import pymem.memory
import webbrowser
from tkinter import Listbox, StringVar, Tk, messagebox, ttk, Menu, Spinbox, IntVar, Button, TclError, filedialog
import psutil
from tkinter.colorchooser import askcolor
from config_kits.team_kit_data import TeamKitData

class Gui:
    filename = ""
    team_id =""
    def __init__(self, master):
        self.master= master
        self.appname='PES Kit Configurator For PS2'
        self.version= '1.0'
        self.author= 'Gerardo Contreras'
        self.master.title(self.appname+' '+self.version)
        self.master.resizable(False, False)

        self.master.bind("<Control-q>", lambda event: self.on_closing())
        self.master.bind("<Control-Q>", lambda event: self.on_closing())

        self.master.bind("<Control-s>", lambda event: self.get_by_process_name())
        self.master.bind("<Control-S>", lambda event: self.get_by_process_name())

        # Creating Menubar
        self.menubar = Menu(self.master)
        self.master.config(menu = self.menubar)
          
        # Adding File Menu and commands
        self.file = Menu(self.menubar, tearoff = 0)
        self.menubar.add_cascade(label ='File', menu = self.file)
        self.file.add_command(label='Open', command = None, accelerator="Ctrl+O",state='disable')
        self.file.add_command(label='Search process', command = self.get_by_process_name, accelerator="Ctrl+S")
        self.file.add_separator()
        self.file.add_command(label='Exit', command = self.on_closing, accelerator="Ctrl+Q")

        # Adding Edit Menu and commands
        self.edit = Menu(self.menubar, tearoff = 0)
        self.menubar.add_cascade(label='Edit', menu = self.edit)

        self.edit_submenu = Menu(self.menubar, tearoff = 0)
        # Dinamically loading game versions as sub menu

        self.gmv_var = IntVar()
        self.gmv_var.set(1)
        
        self.edit_submenu.add_radiobutton(label="PES 14 (SLES_556.76)", variable=self.gmv_var, value=1, command=None)
        self.edit_submenu.add_radiobutton(label="PES 13", variable=self.gmv_var, value=2, command=None, state="disable")
        self.edit_submenu.add_radiobutton(label="PES 12", variable=self.gmv_var, value=3, command=None, state="disable")
        self.edit_submenu.add_radiobutton(label="PES 11", variable=self.gmv_var, value=4, command=None, state="disable")

        self.edit.add_cascade(label='Game version', menu=self.edit_submenu)
        self.edit.add_separator()     
        self.edit.add_command(label ='Export nations kit config', command= lambda: self.export_kit_config(self.national_kits), state="disable")
        self.edit.add_command(label ='Export clubs kit config', command= lambda: self.export_kit_config(self.club_kits), state="disable")

        # Adding Help Menu
        self.help_ = Menu(self.menubar, tearoff = 0)
        self.menubar.add_cascade(label ='Help', menu = self.help_)
        self.help_.add_command(label ='Donate', command = self.donate)
        self.help_.add_command(label ='YouTube', command = self.youtube)
        self.help_.add_separator()
        self.help_.add_command(label ='About', command = self.about)

        self.lbox_teams = Listbox(master, exportselection=False, width=22, height=22)
        self.lbox_teams.grid(row=0, column=0, rowspan=2, padx=5, pady=5)
        
        frame_01 = ttk.LabelFrame(master, text="Menu")
        frame_01.grid(column=1, row=0, padx=5, pady=5)

        self.kit_combox = ttk.Combobox(frame_01,state="readonly", values=["GA","PA","GB","PB"], width=5)
        self.kit_combox.bind("<<ComboboxSelected>>", lambda event: self.set_kit_info(self.lbox_teams.get(0, "end").index(self.lbox_teams.get(self.lbox_teams.curselection()))))
        self.kit_combox.current(0)
        self.kit_combox.grid(column=0, row=0, padx=5, pady=5, sticky="W")  

        label_0 = ttk.Label(frame_01, text="Type")
        label_0.grid(column=1, row=0, padx=5, pady=5, sticky="N")

        label_1 = ttk.Label(frame_01, text="Size")
        label_1.grid(column=2, row=0, padx=5, pady=5, sticky="N")

        label_2 = ttk.Label(frame_01, text="X")
        label_2.grid(column=3, row=0, padx=5, pady=5, sticky="N")

        label_3 = ttk.Label(frame_01, text="Y")
        label_3.grid(column=4, row=0, padx=5, pady=5, sticky="N")

        label_4 = ttk.Label(frame_01, text="Curve")
        label_4.grid(column=5, row=0, padx=5, pady=5, sticky="N")

        label_001 = ttk.Label(frame_01, text="Shirt Font")
        label_001.grid(column=0, row=1, padx=5, pady=5,  sticky="WE")
        
        self.combox22 = ttk.Combobox(frame_01, values=["Off","On"],width=5,state="readonly")
        self.combox22.bind("<<ComboboxSelected>>",  lambda event: self.update_kit_info())
        self.combox22.grid(column=1, row=1, padx=10, pady=5, sticky="W")
        
        self.font_spb_size_var = IntVar()
        self.font_spb_size_var.set(0)

        self.font_spb_size = Spinbox(frame_01,textvariable=self.font_spb_size_var, from_=0, to=30, command=self.update_kit_info, width=5)
        self.font_spb_size.bind('<Return>', lambda event: self.update_kit_info())
        self.font_spb_size.grid(column=2, row=1, padx=10, pady=5, sticky="W")

        self.font_combobox_curve = ttk.Combobox(frame_01, values=["Linear","Light","Medium","Maximum"],width=7,state="readonly")
        self.font_combobox_curve.bind("<<ComboboxSelected>>",  lambda event: self.update_kit_info())
        self.font_combobox_curve.grid(column=5, row=1, padx=10, pady=5, sticky="W")

        label_04 = ttk.Label(frame_01, text="Front Number")
        label_04.grid(column=0, row=2, padx=5, pady=5, sticky="WE")

        self.combox3 = ttk.Combobox(frame_01, values=["Off","On"],width=5,state="readonly")
        self.combox3.bind("<<ComboboxSelected>>",  lambda event: self.update_kit_info())
        self.combox3.grid(column=1, row=2, padx=10, pady=5, sticky="W")

        self.front_number_spb_size_var = IntVar()
        self.front_number_spb_size_var.set(0)

        self.front_number_spb_size = Spinbox(frame_01, textvariable=self.front_number_spb_size_var,  from_=0, to=22,command=self.update_kit_info, width=5)
        self.front_number_spb_size.bind('<Return>', lambda event: self.update_kit_info())
        self.front_number_spb_size.grid(column=2, row=2, padx=10, pady=5, sticky="W")

        self.x_posc_front_num_spb_var = IntVar()
        self.x_posc_front_num_spb_var.set(0)

        self.x_posc_front_num_spb = Spinbox(frame_01, textvariable=self.x_posc_front_num_spb_var, from_=0, to=29, command=self.update_kit_info, width=5)
        self.x_posc_front_num_spb.bind('<Return>', lambda event: self.update_kit_info())
        self.x_posc_front_num_spb.grid(column=3, row=2, padx=10, pady=5, sticky="W")

        self.y_posc_front_num_spb_var = IntVar()
        self.y_posc_front_num_spb_var.set(0)

        self.y_posc_front_num_spb = Spinbox(frame_01, textvariable=self.y_posc_front_num_spb_var, from_=0, to=29,  command=self.update_kit_info, width=5)
        self.y_posc_front_num_spb.bind('<Return>', lambda event: self.update_kit_info())
        self.y_posc_front_num_spb.grid(column=4, row=2, padx=10, pady=5, sticky="W")

        label_05 = ttk.Label(frame_01, text="Back Number")
        label_05.grid(column=0, row=3, padx=5, pady=5, sticky="WE")

        self.b_number_spb_size_var = IntVar()
        self.b_number_spb_size_var.set(0)

        self.b_number_spb_size = Spinbox(frame_01, textvariable=self.b_number_spb_size_var, from_=0, to=31,  command=self.update_kit_info, width=5)
        self.b_number_spb_size.bind('<Return>', lambda event: self.update_kit_info())
        self.b_number_spb_size.grid(column=2, row=3, padx=10, pady=5, sticky="W")

        self.y_posc_num_back_spb_var = IntVar()
        self.y_posc_num_back_spb_var.set(0)

        self.y_posc_num_back_spb = Spinbox(frame_01, textvariable=self.y_posc_num_back_spb_var, from_=0, to=18,  command=self.update_kit_info, width=5)
        self.y_posc_num_back_spb.bind('<Return>', lambda event: self.update_kit_info())
        self.y_posc_num_back_spb.grid(column=4, row=3, padx=10, pady=5, sticky="W")

        label_06 = ttk.Label(frame_01, text="Short Number")
        label_06.grid(column=0, row=4, padx=5, pady=5, sticky="WE")

        self.combox4 = ttk.Combobox(frame_01, values=["Off","Left","Right"],width=5,state="readonly")
        self.combox4.bind("<<ComboboxSelected>>",  lambda event: self.update_kit_info())
        self.combox4.grid(column=1, row=4, padx=10, pady=5, sticky="W")

        self.short_number_spb_size_var = IntVar()
        self.short_number_spb_size_var.set(0)

        self.short_number_spb_size = Spinbox(frame_01, textvariable=self.short_number_spb_size_var, from_=0, to=28,  command=self.update_kit_info, width=5)
        self.short_number_spb_size.bind('<Return>', lambda event: self.update_kit_info())
        self.short_number_spb_size.grid(column=2, row=4, padx=10, pady=5, sticky="W")

        self.x_posc_short_num_spb_var = IntVar()
        self.x_posc_short_num_spb_var.set(0)

        self.x_posc_short_num_spb = Spinbox(frame_01, textvariable=self.x_posc_short_num_spb_var, from_=0, to=25,  command=self.update_kit_info, width=5)
        self.x_posc_short_num_spb.bind('<Return>', lambda event: self.update_kit_info())
        self.x_posc_short_num_spb.grid(column=3, row=4, padx=10, pady=5, sticky="W")

        self.y_posc_short_num_spb_var = IntVar()
        self.y_posc_short_num_spb_var.set(0)

        self.y_posc_short_num_spb = Spinbox(frame_01, textvariable=self.y_posc_short_num_spb_var, from_=0, to=19,  command=self.update_kit_info, width=5)
        self.y_posc_short_num_spb.bind('<Return>', lambda event: self.update_kit_info())
        self.y_posc_short_num_spb.grid(column=4, row=4, padx=10, pady=5, sticky="W")
        
        label_05 = ttk.Label(frame_01, text="Overlay")
        label_05.grid(column=0, row=5, padx=5, pady=5, sticky="WE")

        self.overlay_spb_var = IntVar()
        self.overlay_spb_var.set(0)

        self.overlay_spb = Spinbox(frame_01,textvariable=self.overlay_spb_var, from_=0, to=14,  command=self.update_kit_info, width=5)
        self.overlay_spb.bind('<Return>', lambda event: self.update_kit_info())
        self.overlay_spb.grid(column=1, row=5, padx=10, pady=5, sticky="W")

        self.posc_overlay_y_spb_var = IntVar()
        self.posc_overlay_y_spb_var.set(0)

        self.posc_overlay_y_spb = Spinbox(frame_01,textvariable=self.posc_overlay_y_spb_var, from_=0, to=10,  command=self.update_kit_info, width=5)
        self.posc_overlay_y_spb.bind('<Return>', lambda event: self.update_kit_info())
        self.posc_overlay_y_spb.grid(column=4, row=5, padx=10, pady=5, sticky="W")
        label_09 = ttk.Label(frame_01, text="Model")
        label_09.grid(column=0, row=6, padx=5, pady=5, sticky="WE")
        self.model_spb_var = IntVar()
        self.model_spb_var.set(0)

        self.model_tp_spb = Spinbox(frame_01, textvariable=self.model_spb_var, from_=0, to=154, command=self.update_kit_info, width=5)
        self.model_tp_spb.bind('<Return>', lambda event: self.update_kit_info())
        self.model_tp_spb.grid(column=1, row=6, padx=10, pady=5, sticky="W")

        label_10 = ttk.Label(frame_01, text="License")
        label_10.grid(column=0, row=7, padx=5, pady=5, sticky="WE")
    
        self.combox7 = ttk.Combobox(frame_01, values=["NL","LC"],width=5,state="readonly")
        self.combox7.bind('<<ComboboxSelected>>',  lambda event: self.update_kit_info())
        self.combox7.grid(column=1, row=7, padx=10, pady=5, sticky="W")

        label_11 = ttk.Label(frame_01, text="Radar Color")
        label_11.grid(column=0, row=8, padx=5, pady=5, sticky="WE")
        
        self.colors_rgb_int_var = StringVar()

        self.btn_radar = Button(frame_01,width=7, textvariable=self.colors_rgb_int_var,command=self.select_color)
        self.btn_radar.grid(column=1, row=8, padx=10, pady=5, sticky="W")

        frame_02 = ttk.LabelFrame(master, text="Macro for all teams")
        frame_02.grid(column=1, row=1, padx=5, pady=5, sticky="W")

        label_model = ttk.Label(frame_02, text="Model:")
        label_model.grid(column=0, row=0, padx=1, pady=5, sticky="W")

        self.model_combox = ttk.Combobox(frame_02, values=[x for x in range(155)], width=5, state="readonly")
        self.model_combox.grid(column=1, row=0, padx=9, pady=5, sticky="W")
        self.model_combox.set(0)

        btn = ttk.Button(frame_02, text="Apply", command=lambda : self.set_model_to_all_team(self.model_combox.current()))
        btn.grid(column=2, row=0, padx=9, pady=5)

        label_license = ttk.Label(frame_02, text="License:")
        label_license.grid(column=3, row=0, padx=1, pady=5, sticky="W")

        license_btn = ttk.Button(frame_02, text="Licensed", command=lambda : self.set_license_to_all_team("LC"))
        license_btn.grid(column=4, row=0, padx=10, pady=5)

        unlicense_btn = ttk.Button(frame_02, text="Unlicensed", command=lambda : self.set_license_to_all_team("NL"))
        unlicense_btn.grid(column=5, row=0, padx=10, pady=5)
        
        # aca colocar todos los grid

    def export_kit_config(self, bytes_list):
        if self.filename=="":
            messagebox.showerror(title=self.appname, message="You must first run the game before attempting to read or set any data")
            return 0

        file = filedialog.asksaveasfile(mode='wb', title = "Save file as", initialfile="", defaultextension=".bin" , filetypes=(("bin files","*.bin"),("all files","*.*")))
        if file:
            #with open('kit_config.bin','wb') as file:
            for item in bytes_list:
                file.write(item.data)
            messagebox.showinfo(title=self.appname, message="The kit configuration file has been exported")
        return 0
    
    def set_model_to_all_team(self, new_model):
        if self.filename=="":
            messagebox.showerror(title=self.appname, message="You must first run the game before attempting to read or set any data")
            return 0
        
        answer = messagebox.askyesno(title=self.appname,message=f"Are you sure you to assign the model number {new_model} to all teams?")
        
        if answer:
            for x in range(len(self.national_kits)):
                self.national_kits[x].GA.update_model(new_model)
                self.national_kits[x].PA.update_model(new_model)
                self.national_kits[x].GB.update_model(new_model)
                self.national_kits[x].PB.update_model(new_model)
                self.national_kits[x].update_data()
                self.memory.write_bytes(self.nation_start_address + (x * self.national_kit_length), bytes(self.national_kits[x].data), self.national_kit_length)

            for x in range(len(self.club_kits)):
                self.club_kits[x].GA.update_model(new_model)
                self.club_kits[x].PA.update_model(new_model)
                self.club_kits[x].GB.update_model(new_model)
                self.club_kits[x].PB.update_model(new_model)

                self.club_kits[x].update_data()
                self.memory.write_bytes(self.club_start_address + (x * self.clubes_kit_length), bytes(self.club_kits[x].data), self.clubes_kit_length)
            #"""
            messagebox.showinfo(title=self.appname,message=f"Model {new_model} set to all teams")
        else:
            return 0

    def set_license_to_all_team(self, new_value):
        if self.filename=="":
            messagebox.showerror(title=self.appname, message="You must first run the game before attempting to read or set any data")
            return 0
        
        answer = messagebox.askyesno(title=self.appname,message=f"Are you sure you to assign the license to {new_value} in all teams?")
        
        if answer:
            for x in range(len(self.national_kits)):
                self.national_kits[x].GA.update_license(new_value)
                self.national_kits[x].PA.update_license(new_value)
                self.national_kits[x].GB.update_license(new_value)
                self.national_kits[x].PB.update_license(new_value)
                self.national_kits[x].update_data()
                self.memory.write_bytes(self.nation_start_address + (x * self.national_kit_length), bytes(self.national_kits[x].data), self.national_kit_length)

            for x in range(len(self.club_kits)):
                self.club_kits[x].GA.update_license(new_value)
                self.club_kits[x].PA.update_license(new_value)
                self.club_kits[x].GB.update_license(new_value)
                self.club_kits[x].PB.update_license(new_value)

                self.club_kits[x].update_data()
                self.memory.write_bytes(self.club_start_address + (x * self.clubes_kit_length), bytes(self.club_kits[x].data), self.clubes_kit_length)
            #"""
            messagebox.showinfo(title=self.appname,message=f"License set to {new_value} in all teams")
        else:
            return 0
    
    def select_color(self):
        if self.filename=="" or self.team_id=="":
            messagebox.showerror(title=self.appname, message="You must first run the game before attempting to read or set any data")
            return 0

        colors = askcolor(title="Select a color")
        if colors[0] is not None :
            self.colors_rgb_int_var.set(colors[1])

            self.btn_radar.configure(bg=colors[1])

            self.update_kit_info()
        else:
            return 0

    def run_program(self):
        try:
            self.op_gmv = self.gmv_var.get()
            if self.op_gmv == 1:
                self.nation_start_address = 0x21944C38 
                self.national_kit_length = 456
                self.total_national = 67
                self.clubes_kit_length = 648
                self.total_clubes = 130

            elif self.op_gmv == 2:
                self.nation_start_address = None 
                self.national_kit_length = None
                self.total_national = None
                self.clubes_kit_length = None
                self.total_clubes = None

            elif self.op_gmv == 3:
                self.nation_start_address = None 
                self.national_kit_length = None
                self.total_national = None
                self.clubes_kit_length = None
                self.total_clubes = None

            elif self.op_gmv == 4:
                self.nation_start_address = None 
                self.national_kit_length = None
                self.total_national = None
                self.clubes_kit_length = None
                self.total_clubes = None

            self.memory = pymem.Pymem("pcsx2.exe")
            self.club_start_address = self.nation_start_address + (self.total_national* self.national_kit_length)
            self.total_teams = self.total_national + self.total_clubes

            self.national_kits = [TeamKitData(bytearray(self.memory.read_bytes(self.nation_start_address + (i *self.national_kit_length),self.national_kit_length))) for i in range(self.total_national)]
            self.club_kits = [TeamKitData(bytearray(self.memory.read_bytes(self.club_start_address + (i *self.clubes_kit_length),self.clubes_kit_length))) for i in range(self.total_clubes)]
            list_teams = []
            if os.path.exists('list_teams.txt'):
                with open('list_teams.txt', encoding="utf-8") as f:
                    list_teams = [line.rstrip() for line in f]

            if len(list_teams) != 197:
                messagebox.showerror(title=self.appname, message="Invalid list team file... loading default team list")
                
                list_teams = ['Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Czech Republic', 'Denmark', 'England', 'Finland', 'France', 'Germany', 
                'Greece', 'Hungary', 'Ireland', 'Israel', 'Italy', 'Netherlands', 'North Ireland', 'Norway', 'Poland', 'Portugal', 'Romania', 
                'Russia', 'Scotland', 'Serbia', 'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'Switzerland', 'Turkey', 'Ukraine', 'Wales', 'Algeria', 
                'Cameroon', "Côte d'Ivoire", 'Egypt', 'Ghana', 'Nigeria', 'South Africa', 'Zambia', 'Costa Rica', 'Honduras', 'Mexico', 'United States', 
                'Argentina', 'Brazil', 'Chile', 'Colombia', 'Ecuador', 'Paraguay', 'Peru', 'Uruguay', 'Australia', 'China', 'Japan', 'North Korea', 
                'Saudi Arabia', 'South Korea', 'United Arab Emirates', 'New Zealand', 'Classic England', 'Classic France', 'Classic Germany', 
                'Classic Italy', 'Classic Netherlands', 'Classic Argentina', 'Classic Brazil', 'Arsenal', 'Aston villa', 'Cardiff city', 'Chelsea', 
                'Crystal Palace', 'Everton', 'Fulham', 'Hull City', 'Liverpool', 'Man. City', 'Man. United', 'New Castle', 'Norwich', 'Southampton', 
                'Stoke City', 'Sunderland', 'Swansea', 'Tottenham', 'West Bromwich', 'West ham utd', 'AC Ajaccio', 'SC Bastia', 
                'FC Girondins de Bordeaux', 'Evian Thonon Gaillard FC', 'EA Guingamp', 'LOSC Lille Métropole', 'FC Lorient', 'Olympique Lyonnais', 
                'Olympique de Marseille', 'AS Monaco FC', 'Montpellier Hérault SC', 'FC Nantes', 'OGC Nice', 'Paris Saint-Germain FC', 'Stade De Reims', 
                'Stade Rennais FC', 'AS Saint-etienne', 'FC Sochaux-Montbéliard', 'Toulouse FC', 'Valenciennes FC', 'Atalanta BC', 'Bologna FC', 
                'Cagliari Calcio', 'Calcio Catania', 'AC Chievo Verona', 'ACF Fiorentina', 'Genoa CFC', 'Internazionale', 'Juventus', 'SS Lazio', 
                'AS Livorno Calcio', 'AC Milan', 'SSC Napoli', 'Parma FC', 'As Roma', 'UC Sampdoria', 'US Sassuolo Calcio', 'Torino FC', 
                'Udinese Calcio', 'Hellas Verona FC', 'ADO Den Haag', 'AFC Ajax', 'AZ Alkmaar', 'SC Cambuur', 'Feyenoord', 'Go Ahead Eagles', 
                'FC Groningen', 'SC Heerenveen', 'Heracles Almelo', 'NAC Breda', 'NEC Nijmegen', 'PSV Eindhoven', 'RKC Waalwijk', 'Roda JC', 
                'FC Twente', 'FC Ultrecht', 'Vitesse', 'PEC Zwolle', 'UD Almería', 'Athletic Club', 'Atlético Madrid', 'FC Barcelona', 'Real Betis', 
                'Celta de Vigo', 'Elche CF', 'RCD Espanyol', 'Getafe CF', 'Granada CF', 'Levante UD', 'Málaga CF', 'CA Osasuna', 'Rayo Vallecano', 
                'Real Madrid CF', 'Real Sociedad', 'Sevilla FC', 'Valencia CF', 'Real Valladolid', 'Villarreal CF', 'RSC Anderlecht', 'APOEL Nicosia', 
                'Sparta Praha', 'FC Copenhagen', 'Nordsjaelland', 'Bayer Leverkusen', 'FC Bayern München', 'Schalke', 'Olympiacos FC', 'Paok FC', 
                'Maccabi Tel Aviv', 'Legia Warsawa', 'SL Benfica', 'SC Braga', 'FC Pacos de Ferreira', 'FC Porto', 'PFC CSKA Moscow', 
                'FC Zenit St. Petersburg', 'Celtic FC', 'Motherwell FC', 'Galatasaray AS', 'Shakhtar Donetsk', 'Almchendolf', 'Ehrenhofstadt', 
                'Fineseeberg', 'Kriedbach', 'Lengerbiltz', 'Theeselvargen', 'PES United', 'We United', 'Babylania', 'Athletic Club Salsabie']
            
            self.lbox_teams.insert('end', *list_teams)
            self.lbox_teams.selectedindex = 0
            self.lbox_teams.select_set(0)
            self.lbox_teams.bind("<<ListboxSelect>>", lambda event: self.set_team_kit_info())

            self.edit.entryconfig('Export nations kit config', state="normal")
            self.edit.entryconfig('Export clubs kit config', state="normal")

        except pymem.exception.MemoryReadError as e:
            messagebox.showerror(title=self.appname, message=f"pymem error code {e}")
            return 0

    def get_by_process_name(self):
        PROCNAME = 'pcsx2.exe'
        for proc in psutil.process_iter():
            if proc.name() == PROCNAME:
                self.filename = proc.name()
                self.run_program()

    def set_team_kit_info(self):
            self.team_id = self.lbox_teams.get(0, "end").index(self.lbox_teams.get(self.lbox_teams.curselection()))
            
            self.kit_combox.current(0)            
            self.set_kit_info(self.team_id)

    def set_kit_info(self, team_id):
        if 0<=team_id < self.total_national:
            kit_list = self.national_kits
        elif self.total_national <= team_id < self.total_teams:
            team_id -= self.total_national
            kit_list = self.club_kits

        kit_type = self.kit_combox.current()
        if kit_type == 0:
            variable = kit_list[team_id].GA
            
        elif kit_type == 1:
            variable = kit_list[team_id].PA

        elif kit_type == 2:
            variable = kit_list[team_id].GB

        elif kit_type == 3:
            variable = kit_list[team_id].PB

        self.combox7.current(variable.license )
        self.model_spb_var.set(variable.model)

        self.combox22.current(variable.font_shirt)

        self.combox3.current(variable.front_number)

        self.combox4.current(variable.short_number)
        self.overlay_spb_var.set(variable.overlay)
        self.posc_overlay_y_spb_var.set(variable.posc_overlay_y)
        
        self.font_combobox_curve.current(variable.font_curve)
        self.font_spb_size_var.set(variable.font_size)
        
        self.b_number_spb_size_var.set(variable.number_size_back)

        self.short_number_spb_size_var.set(variable.short_number_size)
        self.front_number_spb_size_var.set(variable.front_number_size)
        self.y_posc_num_back_spb_var.set(variable.y_posc_num_back)
        self.x_posc_front_num_spb_var.set(variable.x_posc_front_num)
        self.y_posc_front_num_spb_var.set(variable.y_posc_front_num)
        
        self.x_posc_short_num_spb_var.set(variable.x_posc_short_number)
        self.y_posc_short_num_spb_var.set(variable.y_posc_short_number)
        
        self.btn_radar.configure(bg=variable.rgb_hex)
        self.colors_rgb_int_var.set(variable.rgb_hex)

    def update_kit_info(self):
        if self.filename=="":
            messagebox.showerror(title=self.appname, message="You must first run the game before attempting to read or set any data")
            return 0

        elif self.team_id=="":
            messagebox.showerror(title=self.appname, message="You must first select a team from the list box")
            return 0
        try:
            team_id = self.lbox_teams.get(0, "end").index(self.lbox_teams.get(self.lbox_teams.curselection()))
            if 0<=team_id < self.total_national:
                kit_list = self.national_kits
                kit_length = self.national_kit_length
                address_initial = self.nation_start_address
            elif self.total_national <= team_id < self.total_teams:
                team_id -= self.total_national
                kit_list = self.club_kits
                kit_length = self.clubes_kit_length
                address_initial = self.club_start_address
            kit_type = self.kit_combox.current()
            
            if kit_type == 0:
                variable = kit_list[team_id].GA

            elif kit_type == 1:
                variable = kit_list[team_id].PA

            elif kit_type == 2:
                variable = kit_list[team_id].GB
                
            elif kit_type == 3:
                variable = kit_list[team_id].PB

            variable.update_model(self.model_spb_var.get())
            variable.update_license(self.combox7.get())
            variable.update_font_shirt(self.combox22.current())

            variable.update_front_number(self.combox3.current())
            variable.update_short_number(self.combox4.current())

            variable.update_overlay(self.overlay_spb_var.get())
            variable.update_posc_overlay_y(self.posc_overlay_y_spb_var.get())
            
            variable.update_font_curve(self.font_combobox_curve.current())
            variable.update_font_size(self.font_spb_size_var.get())
            variable.update_number_size_back(self.b_number_spb_size_var.get())
            variable.update_short_number_size(self.short_number_spb_size_var.get())
            variable.update_front_number_size(self.front_number_spb_size_var.get())
            variable.update_y_posc_num_back(self.y_posc_num_back_spb_var.get())
            variable.update_x_posc_front_num(self.x_posc_front_num_spb_var.get())
            variable.update_y_posc_front_num(self.y_posc_front_num_spb_var.get())
            
            variable.update_x_posc_short_number(self.x_posc_short_num_spb_var.get())
            variable.update_y_posc_short_number(self.y_posc_short_num_spb_var.get())
            
            variable.update_color_radar(self.colors_rgb_int_var.get())
            self.btn_radar.configure(bg=self.colors_rgb_int_var.get())
        
            kit_list[team_id].update_data()
            self.memory.write_bytes(address_initial + (team_id * kit_length), bytes(kit_list[team_id].data), kit_length)

        except (TclError, ValueError) as e:
            messagebox.showerror(title=self.appname, message=e)
            
    def start(self):
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.master.mainloop()
        
    def youtube(self):     
        pag1 = 'https://www.youtube.com/channel/UCzHGN5DBIXVviZQypFH_ieg'
        webbrowser.open_new(pag1)
        
    def about(self):
        messagebox.showinfo(self.appname+' '+self.version, 'Developed by '+self.author+' and PES Indie')

    def donate(self):     
        webbrowser.open_new('https://www.paypal.com/paypalme/gerardocj11')
        
    def on_closing(self):
        if messagebox.askokcancel("Exit", "Do you want to exit the program?"):
            self.master.destroy()
def main():
    Gui(Tk()).start()

if __name__ == '__main__':
    main()
