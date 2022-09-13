import os
import pymem
import webbrowser
from tkinter import Listbox, StringVar, Tk, messagebox, Menu, Spinbox, IntVar, Button, TclError, filedialog, Label, ttk, LabelFrame
import psutil
from tkinter.colorchooser import askcolor
from config_kits.team_kit_data import TeamKitData
import yaml
from pathlib import Path


class Config:
    config_dir = "config"
    def __init__(self):
        self.get_config_files()

    def get_config_files(self):
        self.filelist = []
        self.games_config = []
        for p in Path(self.config_dir).iterdir():
            if p.is_file():
                self.filelist.append(p.name)
                self.games_config.append(p.stem)

    def load_config(self, file):
        with open(self.config_dir + "/" + file) as stream:
            self.file = yaml.safe_load(stream)

        self.game_name = self.file["Gui"]["Game Name"]
        self.game_data = self.file["Game Data"]

class Gui(Tk):
    filename =""
    team_id =""
    def __init__(self):
        super().__init__()
        self.appname='PES Kit Configurator'
        self.version= '1.0.1'
        self.author= 'PES Indie Team'
        self.title(self.appname)
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)


        try:
            self.create_config()
        except FileNotFoundError as e:
            messagebox.showerror(title=self.appname, message=f"No config files found code error {e}")

    
        self.bind("<Control-q>", lambda event: self.on_closing())
        self.bind("<Control-Q>", lambda event: self.on_closing())


        #self.bind("<Control-s>", lambda event: self.get_by_process_name())
        #self.bind("<Control-S>", lambda event: self.get_by_process_name())

        # Creating Menubar
        self.menubar = Menu(self)
        self.config(menu = self.menubar)
          
        # Adding File Menu and commands
        self.file = Menu(self.menubar, tearoff = 0)
        self.menubar.add_cascade(label ='File', menu = self.file)
        self.file.add_command(label='Open', command = None, accelerator="Ctrl+O", state='disabled')
        self.file.add_command(label='Search process', command = self.get_by_process_name, accelerator="Ctrl+S", state='disabled')
        self.file.add_separator()
        self.file.add_command(label='Exit', command = self.on_closing, accelerator="Ctrl+Q")


        self.edit_menu = Menu(self.menubar, tearoff = 0)
        self.menubar.add_cascade(label='Edit', menu = self.edit_menu)

        self.edit_submenu = Menu(self.menubar, tearoff=0)
        self.edit_menu.add_cascade(label="Game Version", menu=self.edit_submenu)

        for i in range(len(self.my_config.games_config)):
            self.edit_submenu.add_radiobutton(label=self.my_config.games_config[i],command= lambda i=i: self.change_config(self.my_config.filelist[i]))

        self.edit_menu.add_separator()     
        self.edit_menu.add_command(label ='Export nations kit config', command= lambda: self.export_kit_config(self.national_kits), state="disabled")
        self.edit_menu.add_command(label ='Export clubs kit config', command= lambda: self.export_kit_config(self.club_kits), state="disabled")

        # Adding Help Menu
        self.help_ = Menu(self.menubar, tearoff = 0)
        self.menubar.add_cascade(label ='Help', menu = self.help_)
        self.help_.add_command(label ='Donate', command = self.donate)
        self.help_.add_command(label ='YouTube', command = self.youtube)
        self.help_.add_separator()
        self.help_.add_command(label ='About', command = self.about)

        self.frame1 = ttk.Frame(self)
        self.frame1.grid(row=0, column=0, rowspan=2, padx=5, pady=5)

        self.kit_combox = ttk.Combobox(self.frame1, state="disabled", values=["GA","PA","GB","PB"], )
        self.kit_combox.bind("<<ComboboxSelected>>", lambda event: self.set_kit_info(self.lbox_teams.get(0, "end").index(self.lbox_teams.get(self.lbox_teams.curselection()))))
        self.kit_combox.current(0)
        self.kit_combox.grid(row=0, column=0, sticky="NWE")  
        
        self.lbox_teams = Listbox(self.frame1, exportselection=False, width=22, height=22)
        self.lbox_teams.grid(row=1, column=0, pady=5, sticky="NWE")

        self.scrollbar = ttk.Scrollbar(self.frame1, orient="vertical", command=self.lbox_teams.yview)
        self.scrollbar.grid(row=1, column=1, pady=5, sticky="NS")
        self.lbox_teams.config(yscrollcommand=self.scrollbar.set)

        frame_01 = LabelFrame(self, text="Menu")
        frame_01.grid(column=1, row=0, padx=5, pady=5, sticky="NWE")

        Label(frame_01, text="Option").grid(column=1, row=0, padx=5, pady=5, sticky="N")

        Label(frame_01, text="Size").grid(column=2, row=0, padx=5, pady=5, sticky="N")

        Label(frame_01, text="X").grid(column=3, row=0, padx=5, pady=5, sticky="N")

        Label(frame_01, text="Y").grid(column=4, row=0, padx=5, pady=5, sticky="N")

        Label(frame_01, text="Type").grid(column=5, row=0, padx=5, pady=5, sticky="N")

        Label(frame_01, text="Shirt Font").grid(column=0, row=1, padx=5, pady=5,  sticky="WE")
        
        self.combox22 = ttk.Combobox(frame_01, values=["Off","On"],width=5,state="readonly")
        self.combox22.bind("<<ComboboxSelected>>",  lambda event: self.update_kit_info())
        self.combox22.grid(column=1, row=1, padx=10, pady=5, sticky="W")
        
        self.font_spb_size_var = IntVar()
        self.font_spb_size_var.set(0)

        self.font_spb_size = Spinbox(frame_01,textvariable=self.font_spb_size_var, from_=0, to=30, command=self.update_kit_info, width=5)
        self.font_spb_size.bind('<Return>', lambda event: self.update_kit_info())
        self.font_spb_size.grid(column=2, row=1, padx=10, pady=5, sticky="W")

        self.posc_font_x_var = IntVar()
        self.posc_font_x_var.set(0)
        self.posc_font_x = Spinbox(frame_01,textvariable=self.posc_font_x_var, from_=0, to=30, command=None, width=5)
        self.posc_font_x.bind('<Return>', lambda event: None)
        self.posc_font_x.grid(column=3, row=1, padx=10, pady=5, sticky="W")
        
        self.posc_font_y_var = IntVar()
        self.posc_font_y_var.set(0)
        self.posc_font_y = Spinbox(frame_01,textvariable=self.posc_font_x_var, from_=0, to=30, command=None, width=5)
        self.posc_font_y.bind('<Return>', lambda event: None)
        self.posc_font_y.grid(column=4, row=1, padx=10, pady=5, sticky="W")


        self.font_combobox_curve = ttk.Combobox(frame_01, values=["Linear","Light","Medium","Maximum"],width=7,state="readonly")
        self.font_combobox_curve.bind("<<ComboboxSelected>>",  lambda event: self.update_kit_info())
        self.font_combobox_curve.grid(column=5, row=1, padx=10, pady=5, sticky="W")

        Label(frame_01, text="Front Number").grid(column=0, row=2, padx=5, pady=5, sticky="WE")

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

        Label(frame_01, text="Back Number").grid(column=0, row=3, padx=5, pady=5, sticky="WE")

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

        Label(frame_01, text="Short Number").grid(column=0, row=4, padx=5, pady=5, sticky="WE")

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
        
        Label(frame_01, text="Overlay").grid(column=0, row=5, padx=5, pady=5, sticky="WE")

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
        Label(frame_01, text="Model").grid(column=0, row=6, padx=5, pady=5, sticky="WE")
        self.model_spb_var = IntVar()
        self.model_spb_var.set(0)

        self.model_tp_spb = Spinbox(frame_01, textvariable=self.model_spb_var, from_=0, to=154, command=self.update_kit_info, width=5)
        self.model_tp_spb.bind('<Return>', lambda event: self.update_kit_info())
        self.model_tp_spb.grid(column=1, row=6, padx=10, pady=5, sticky="W")

        Label(frame_01, text="License").grid(column=0, row=7, padx=5, pady=5, sticky="WE")
    
        self.combox7 = ttk.Combobox(frame_01, values=["NL","LC"],width=5,state="readonly")
        self.combox7.bind('<<ComboboxSelected>>',  lambda event: self.update_kit_info())
        self.combox7.grid(column=1, row=7, padx=10, pady=5, sticky="W")

        Label(frame_01, text="Radar Color").grid(column=0, row=8, padx=5, pady=5, sticky="WE")
        
        self.colors_rgb_int_var = StringVar()

        self.btn_radar = Button(frame_01,width=7, textvariable=self.colors_rgb_int_var,command=self.select_color)
        self.btn_radar.grid(column=1, row=8, padx=10, pady=5, sticky="W")

        frame_02 = LabelFrame(self, text="Macro for all teams")
        frame_02.grid(column=1, row=1, padx=5, pady=5, sticky="W")

        Label(frame_02, text="Model:").grid(column=0, row=0, padx=1, pady=5, sticky="W")

        self.model_combox = ttk.Combobox(frame_02, values=[x for x in range(155)], width=5, state="readonly")
        self.model_combox.grid(column=1, row=0, padx=9, pady=5, sticky="W")
        self.model_combox.set(0)

        btn = ttk.Button(frame_02, text="Apply", command=lambda : self.set_model_to_all_team(self.model_combox.current()))
        btn.grid(column=2, row=0, padx=9, pady=5)

        Label(frame_02, text="License:").grid(column=3, row=0, padx=1, pady=5, sticky="W")

        license_btn = ttk.Button(frame_02, text="Licensed", command=lambda : self.set_license_to_all_team("LC"))
        license_btn.grid(column=4, row=0, padx=10, pady=5)

        unlicense_btn = ttk.Button(frame_02, text="Unlicensed", command=lambda : self.set_license_to_all_team("NL"))
        unlicense_btn.grid(column=5, row=0, padx=10, pady=5)
        
        # aca colocar todos los grid

    def create_config(self):
        self.my_config = Config()
    
    def change_config(self, file):
        self.my_config.load_config(file)
        self.refresh_gui()

    def refresh_gui(self):
        self.lbox_teams.delete(0,'end')
        self.get_by_process_name()
        self.run_program()
        self.title(f'{self.appname} {self.my_config.file["Gui"]["Game Name"]}')
        
    def get_by_process_name(self):
        PROCNAME = 'pcsx2.exe'
        for proc in psutil.process_iter():
            if proc.name() == PROCNAME:
                self.filename = proc.name()
                self.run_program()

    def run_program(self):
        try:
            self.nation_start_address = self.my_config.game_data['Nation Start Address']
            self.national_kit_length = self.my_config.game_data['National Kit Length']
            self.total_national = self.my_config.game_data['Total National']
            self.clubes_kit_length = self.my_config.game_data['Clubes Kit Length']
            self.total_clubes = self.my_config.game_data['Total Clubes']
    
            self.memory = pymem.Pymem("pcsx2.exe")
            self.club_start_address = self.nation_start_address + (self.total_national* self.national_kit_length)
            self.total_teams = self.total_national + self.total_clubes

            self.national_kits = [TeamKitData(bytearray(self.memory.read_bytes(self.nation_start_address + (i *self.national_kit_length),self.national_kit_length))) for i in range(self.total_national)]
            self.club_kits = [TeamKitData(bytearray(self.memory.read_bytes(self.club_start_address + (i *self.clubes_kit_length),self.clubes_kit_length))) for i in range(self.total_clubes)]
            list_teams = []
            if os.path.exists('list_teams.txt'):
                with open('list_teams.txt', encoding="utf-8") as f:
                    list_teams = [line.rstrip() for line in f]
            else:
                messagebox.showerror(title=self.appname, message="No found list teams")

            self.lbox_teams.insert('end', *list_teams)
            self.lbox_teams.selectedindex = 0
            self.lbox_teams.select_set(0)
            self.lbox_teams.bind("<<ListboxSelect>>", lambda event: self.set_team_kit_info())

            #str(self.kit_combox['state']) == "readonly"

            self.kit_combox.configure(state='readonly')

            self.edit_menu.entryconfig('Export nations kit config', state="normal")
            self.edit_menu.entryconfig('Export clubs kit config', state="normal")

        except pymem.exception.MemoryReadError as e:
            messagebox.showerror(title=self.appname, message=f"pymem error code {e}")
            return 0

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

        colors = askcolor(title="Select a color", initialcolor=self.colors_rgb_int_var.get())
        if colors[0] is not None :
            self.colors_rgb_int_var.set(colors[1])

            self.btn_radar.configure(bg=colors[1])

            self.update_kit_info()
        else:
            return 0


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

    def youtube(self):     
        webbrowser.open_new('https://www.youtube.com/channel/UCzHGN5DBIXVviZQypFH_ieg')
        
    def about(self):
        messagebox.showinfo(f'{self.appname} {self.version}', f'Developed by {self.author}')

    def donate(self):     
        webbrowser.open_new('https://www.paypal.com/paypalme/gerardocj11')
        
    def on_closing(self):
        if messagebox.askokcancel("Exit", "Do you want to exit the program?"):
            self.destroy()

    def start(self):
        self.mainloop()
        
def main():
    Gui().start()

if __name__ == '__main__':
    main()
