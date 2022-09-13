from config_kits.utils import check_value, get_value, set_value, rgb_to_hex, hex_to_rgb

class Kit:
    def __init__(self, data:bytearray):
        """
        Se inicializa la clase recibiendo un bytearray y se inicializan los parametros para el kit
        """
        self.data = data
        self.set_license()
        self.set_model()
        self.set_font_shirt()
        self.set_front_number()
        self.set_short_number()
        self.set_overlay()
        self.set_posc_overlay_y()
        self.set_font_curve()
        self.set_font_size()
        self.set_number_size_back()
        self.set_short_number_size()
        self.set_front_number_size()
        self.set_y_posc_num_back()
        self.set_x_posc_front_num()
        self.set_y_posc_front_num()
        self.set_x_posc_short_number()
        self.set_y_posc_short_number()
        self.set_color_radar()

    def set_font_shirt(self):
        """
        Carga la configuracion de nombre en la camiseta que tiene por default el kit
        """
        self.font_shirt = self.data[54]

    def update_font_shirt(self, new_value:int):
        """
        Actualiza la configuracion de nombre en la camiseta en el kit
        """
        self.data[54] = new_value
        self.set_font_shirt()

    def set_font_curve(self):
        """
        Carga el font que tiene por default el kit
        """
        self.font_curve = self.data[56]

    def update_font_curve(self, new_value:int):
        """
        Actualiza el model en el kit
        """
        self.data[56] = new_value
        self.set_font_curve()

    def set_front_number(self):
        """
        """
        self.front_number = self.data[58]

    def update_front_number(self, new_value:int):
        """
        """
        self.data[58] = new_value
        self.set_front_number()

    def set_short_number(self):
        """
        """
        self.short_number = self.data[59]

    def update_short_number(self, new_value:int):
        """
        """
        self.data[59] = new_value
        self.set_short_number()

    def set_overlay(self):
        """
        Carga el overlay que tiene por default el kit
        """
        self.overlay = self.data[61]

    def update_overlay(self, new_value:int):
        """
        Actualiza el model en el kit
        """
        min_value = 0
        max_value = 14
        if check_value(min_value,new_value,max_value):
            self.data[61] = new_value
            self.set_overlay()
        else:
            raise ValueError(f"Overlay must be between {min_value} and {max_value}")

    def set_posc_overlay_y(self):
        self.posc_overlay_y = self.data[63]

    def update_posc_overlay_y(self, new_value:int):
        """
        """
        min_value = 0
        max_value = 10
        
        if check_value(min_value,new_value,max_value):
            self.data[63] = new_value
            self.set_posc_overlay_y()
        else:
            raise ValueError(f"Overlay y coordinate must be between {min_value} and {max_value}")

    def set_y_posc_num_back(self):
        """
        """
        self.y_posc_num_back = self.data[67]

    def update_y_posc_num_back(self, new_value:int):
        """
        """
        min_value = 0
        max_value = 18
        if check_value(min_value,new_value,max_value):
            self.data[67] = new_value
            self.set_y_posc_num_back()
        else:
            raise ValueError(f"Back number x coordinate must be between {min_value} and {max_value}")

    def set_number_size_back(self):
        """
        """
        self.number_size_back = self.data[68]

    def update_number_size_back(self, new_value:int):
        """
        """
        min_value = 0
        max_value = 31
        if check_value(min_value,new_value,max_value):
            self.data[68] = new_value
            self.set_number_size_back()
        else:
            raise ValueError(f"Number size must be between {min_value} and {max_value}")


    def set_y_posc_front_num(self):
        """
        """
        self.y_posc_front_num = self.data[69]

    def update_y_posc_front_num(self, new_value:int):
        """
        """
        min_value = 0
        max_value = 29
        if check_value(min_value,new_value,max_value):
            self.data[69] = new_value
            self.set_y_posc_front_num()
        else:
            raise ValueError(f"Front number y coordinate must be between {min_value} and {max_value}")

    def set_x_posc_front_num(self):
        """
        """
        self.x_posc_front_num = self.data[70]

    def update_x_posc_front_num(self, new_value:int):
        """
        """
        min_value = 0
        max_value = 29
        if check_value(min_value,new_value,max_value):
            self.data[70] = new_value
            self.set_x_posc_front_num()
        else:
            raise ValueError(f"Front number x coordinate must be between {min_value} and {max_value}")

    
    def set_front_number_size(self):
        """
        """
        self.front_number_size = self.data[71]

    def update_front_number_size(self, new_value:int):
        """
        """
        min_value = 0
        max_value = 22
        if check_value(min_value,new_value,max_value):
            self.data[71] = new_value
            self.set_front_number_size()
        else:
            raise ValueError(f"Front number size must be between {min_value} and {max_value}")

    def set_y_posc_short_number(self):
        """
        """
        self.y_posc_short_number = self.data[72]

    def update_y_posc_short_number(self, new_value:int):
        """
        """
        min_value = 0
        max_value = 19
        if check_value(min_value,new_value,max_value):
            self.data[72] = new_value
            self.set_y_posc_short_number()
        else:
            raise ValueError(f"Short number y coordinate must be between {min_value} and {max_value}")
    
    def set_x_posc_short_number(self):
        """
        """
        self.x_posc_short_number = self.data[73]

    def update_x_posc_short_number(self, new_value:int):
        """
        """
        min_value = 0
        max_value = 25
        if check_value(min_value,new_value,max_value):
            self.data[73] = new_value
            self.set_x_posc_short_number()
        else:
            raise ValueError(f"Short number x coordinate must be between {min_value} and {max_value}")

    def set_short_number_size(self):
        """
        """
        self.short_number_size = self.data[74]

    def update_short_number_size(self, new_value:int):
        """
        """
        min_value = 0
        max_value = 28 #18
        if check_value(min_value,new_value,max_value):
            self.data[74] = new_value
            self.set_short_number_size()
        else:
            raise ValueError(f"Short size must be between {min_value} and {max_value}")

    def set_font_size(self):
        """
        """
        self.font_size = self.data[76]

    def update_font_size(self, new_value:int):
        """
        """
        min_value =0
        max_value = 30
        if check_value(min_value,new_value,max_value):
            self.data[76] = new_value
            self.set_font_size()
        else:
            raise ValueError(f"font size must be between {min_value} and {max_value}")


    def set_license(self):
        """
        Lee y carga en la variable self.license el valor correcto
        """
        license = int.from_bytes(self.data[80:82],'little', signed=False)
        if license == 65535:
            license = 0
        elif license == 1:
            license = 1
        self.license = license

    def update_license(self, new_val:str):
        """
        Recibe un string que puede ser Licensed o Unlicensed y actualiza el valor,
        en los bytes del kit y en la clase
        """
        if new_val == "LC":
            new_val = 1
        elif new_val == "NL":
            new_val = 65535

        self.data[80:82] = new_val.to_bytes(2,'little', signed=False)
        self.set_license()

    def set_model(self):
        """
        Carga el numero de model que tiene por default el kit
        """
        self.model = self.data[82]

    def update_model(self, new_value:int):
        """
        Actualiza el model en el kit
        """
        min_value = 0
        max_value = 154
        if check_value(min_value,new_value,max_value):
            self.data[82] = new_value
            self.set_model()
        else:
            raise ValueError(f"Model must be between {min_value} and {max_value}")
            
    def set_color_radar(self):
        """
        Carga el color del radar que tiene el kit por default
        """
        color_radar_r = get_value(self.data,0,8,31) * 8
        color_radar_g = get_value(self.data,1,5,31) * 8
        color_radar_b = get_value(self.data,1,10,31) * 8
        
        colors_radar_rgb = color_radar_r,color_radar_g,color_radar_b

        self.rgb_hex = rgb_to_hex(colors_radar_rgb)

    def update_color_radar(self, new_value):
        """
        hacer una funcion para validar los valores a pasar que esten entre 0 y 31 y que sea int
        actualizo el valor de rojo a 5
        """
        hex_rgb = hex_to_rgb(new_value)

        r = int(hex_rgb[0] / 8)
        g = int(hex_rgb[1] / 8)
        b = int(hex_rgb[2] / 8)

        set_value(self.data, 0, 8, 31, r)
        set_value(self.data, 1, 5, 31, g)
        set_value(self.data, 1, 10, 31, b)
        
        self.set_color_radar()