# pip install ttkbootstrap stiliaus biblioteka

import tkinter as tk
# import tkinter.ttk as ttk
import math
from abc import ABC, abstractmethod

class Components(ABC):
    @abstractmethod
    def __init__(self, window, canvas, x, y, color, value, name, width, height):
        # pradiniu verciu irasymas ir komponento bei jo atributu (kontaktu) piesimas (dar padidinus galima iskelti i kita metoda)

        #tempimo, paspaudimo ir dvigubo paspaudimo listeneriai
        pass

    @abstractmethod
    def on_click(self, event):
        # paspaudimo ant komponento handleris, pagrinde gauti esamom koordinatems.
        pass

    @abstractmethod
    def on_drag(self, event):
        # komponento perpiesimas tempiant
        pass

    @abstractmethod
    def on_double_click(self, event):
        # redagavimo meniu handlingas
        pass

    @abstractmethod
    def handle_mod_menu_close(self):
        # redagavimo meniu uzdarymas ir komponento vertes keitimas
        pass

    @abstractmethod
    def handle_component_delete(self):
        # redagavimo meniu uzdarymas ir komponento istrinimas
        pass

    @abstractmethod
    def handle_connected_wire_move(self):
        pass


class Geometry():
    pass
# asdasdasdd



class Screen_elements:
    def __init__(self, main_window, window, canvas):
        self.resistors = []
        self.evsources = []
        self.wires = []
        self.canvas = canvas
        self.window = window
        self.main_window = main_window
        # self.resistorCount Neaisku, ar reikes, ar tiesiog su listo dydziu apsieisiu

        self.popup = None # Palceholderis zinutes popupui, None dar del patikrinimo, ar jau atidarytas langas toks, kad nesikartotu.


    def add_resistor(self, value, name):
        if len(self.resistors) > 1:
            print("Max rezistoriu skaicius yra 2")
            self.display_short_message("Max rezistoriu skaicius yra 2")
            # Implementuoti toasta
        else:
            self.resistors.append(Resistor(self.window, self.canvas, 50, 50, 'black', value, name))
            print(f"Appended resistor {self.resistors[-1]}") # paskutini sarase parodau

    def add_wire(self):
        if len(self.wires) > 2:
            print("Max laidu skaicius yra 3")
            self.display_short_message("Max laidu skaicius yra 3")
            # Implementuoti toasta
        else:
            self.wires.append(Wire(self.window, self.canvas, self.resistors, self.evsources))
            print(f"Appended wire {self.wires[-1]}") # paskutini sarase parodau

    def add_ev_source(self, value, name):
        if len(self.evsources) > 0:
            print("Max EV saltiniu skaicius yra 1")
            self.display_short_message("Max EV saltiniu skaicius yra 1")
            # Implementuoti toasta
        else:
            self.evsources.append(EVS(self.window, self.canvas, 50, 100, 'black', value, name))
            print(f"Appended wire {self.evsources[-1]}") # paskutini sarase parodau

    def display_short_message(self, send_message, time=1800):
        # Metodas error zinutems

        if self.popup is None:
            # Mini lango objektas
            self.popup = tk.Toplevel(self.main_window)
            self.popup.title("asd")
            self.popup.geometry("280x140")

            # Teksto lauko objektas
            label = tk.Label(self.popup, text=send_message, font=("Arial", 12, 'bold'))
            label.pack(side="top", fill="both", expand=True, padx=20, pady=20)

            self.popup.after(time, self.display_short_message_destroy) # Paduodamas laikas, kiek laikyti ijungta ir tada ka iskviesti po laiko (istrinamas objektas)

    def display_short_message_destroy(self):
        self.popup.destroy()
        self.popup = None
            

class Wire:
    def __init__(self, window, canvas, resistors, evsources):
        self.window = window
        self.canvas = canvas
        self.resistors = resistors # Cia paduodamas esamu rezistoriu sarasas, kad butu galima tikrinti ju kontaktus
        self.evsources = evsources

        # Cia place holderis busimiems 2 laido kontaktams
        self.bound_contacts = []
        #

        self.wire_line = None # Place holderis, kad po to kur tureciau padeti laido piesinio kreipini

        self.x_start_line = None # Placeholderis pradinem laido koordinatems, del nupieisimo ir perpiesimo
        self.y_start_line = None 

        self.x_finish_line = None # Placeholderis galutinem laido koordinatems, del tik del perpiesimo
        self.y_finish_line = None

        # Listeneris paspaudimui - del laido piesimo pradzios ir pabaigos
        # Irasomas id, kad po to butu galima listeneri istrinti, kai laidas nupiesiamas
        self.mouse_click_listener = self.canvas.bind('<Button-1>', self.check_if_contact)
        # Listeneris peles pozicijai piesiant laida
        # Irasomas id, kad po to butu galima listeneri istrinti, kai laidas nupiesiamas
        self.mouse_motion_listener = self.canvas.bind('<Motion>', self.mouse_moved)

        self.cur_mouse_posx = 0
        self.cur_mouse_posy = 0
        self.wire_draw_enabled = False # Kad zinociau, ar patrigerinus mouse_moved reikia piesti laida ar, dar nepradetas
        # piesimas



    def check_if_contact(self, event):
        # Paimu koordinates, kur paspaudziau
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)

        
        # Patikrinu visus kontaktus
        for resistor in self.resistors:
            for index, contact in enumerate(resistor.contact_coords): # Labai svarbu index, nes jis po to nusiunciamas patikrinti, ar toje pozicijoje jau yra laidas.
                # Paskaiciuoju centra apskritimo
                cx = contact[0]+10 # is n nario listo, jis listas, jo pirmas narys x
                cy = contact[1]-15 # is n nario listo, jis listas, jo antras narys y
                distance = math.sqrt(((cx-x)**2)+((cy-y)**2)) # randu atstuma nuo centro iki peles paspaudimo
                print(f"distance 1: {distance}")
                if distance<=20: # Jeigu atstumas mazesnis/lygus 20, tada sakau, kad pataikiau paspausti, breakinu ir pradedu/baigiu piesti laida
                    if self.wire_draw_enabled == False:
                        self.start_wire_draw(resistor, contact, index) # Jeigu nepradetas piesti, tai pradedu piesti
                    else:
                        self.finish_wire_draw(resistor, contact, index) # Jeigu pradetas piesti, tai baigiu piesti
                    print(contact)
                    break
        for evsource in self.evsources:
            for index, contact in enumerate(evsource.contact_coords):  # Labai svarbu index, nes jis po to nusiunciamas patikrinti, ar toje pozicijoje jau yra laidas.
                # Paskaiciuoju centra apskritimo
                cx = contact[0]+10 # is n nario listo, jis listas, jo pirmas narys x
                cy = contact[1]-15 # is n nario listo, jis listas, jo antras narys y
                distance = math.sqrt(((cx-x)**2)+((cy-y)**2)) # randu atstuma nuo centro iki peles paspaudimo
                print(f"distance 1: {distance}")
                if distance<=20: # Jeigu atstumas mazesnis/lygus 20, tada sakau, kad pataikiau paspausti, breakinu ir pradedu/baigiu piesti laida
                    if self.wire_draw_enabled == False:
                        self.start_wire_draw(evsource, contact, index) # Jeigu nepradetas piesti, tai pradedu piesti
                    else:
                        self.finish_wire_draw(evsource, contact, index) # Jeigu pradetas piesti, tai baigiu piesti
                    print(contact)
                    break


    def link_contact_to_wire(self, component, s_f_state, contact_place):
        if all(element is not None for element in component.linked_wire_objects[contact_place]):
            print("Kontaktas uzimtas")
            return None
        else:
            print("Laidas prijungtas")
            component.linked_wire_objects[contact_place][0] = self # Perduodu laido objekta komponento objektui
            component.linked_wire_objects[contact_place][1] = s_f_state # Perduodu ar tai yra laido pradzia, ar pabaiga
            return 1 # success



    def start_wire_draw(self, component, contact_coords, contact_place):
        # Susiejam objekto (komponento - ev arba resisotriaus) kontakta su tam tikru laido objektu, svarbu, pasakyti, ar cia laido pradzia, ar pabaiga.
        wire_can_be_linked = self.link_contact_to_wire(component, 0, contact_place) # 0 startui, 1 finishui

        if wire_can_be_linked: # Jeigu laidas gali buti prijungtas - kontaktas neuzimtas
            self.wire_draw_enabled = True # Indikatorius update funkcijai, kad piesiu laida

            self.x_start_line = contact_coords[0]
            self.y_start_line = contact_coords[1]

            print(f"{self.x_start_line}, {self.y_start_line}, {self.cur_mouse_posx}, {self.cur_mouse_posy}")

            self.wire_line = self.canvas.create_line(self.x_start_line, self.y_start_line, self.cur_mouse_posx, self.cur_mouse_posy, fill="#4e4c70", width=5)

        

    def finish_wire_draw(self, component, contact_coords, contact_place):
        # Susiejam objekto (komponento - ev arba resisotriaus) kontakta su tam tikru laido objektu, svarbu, pasakyti, ar cia laido pradzia, ar pabaiga.
        wire_can_be_linked = self.link_contact_to_wire(component, 1, contact_place) # 0 startui, 1 finishui

        if wire_can_be_linked: # Jeigu laidas gali buti prijungtas - kontaktas neuzimtas
            self.wire_draw_enabled = False

            endx = contact_coords[0]
            endy = contact_coords[1]

            self.x_finish_line = endx # Placeholderis galutinem laido koordinatems, del tik del perpiesimo
            self.y_finish_line = endy

            self.canvas.coords(self.wire_line, self.x_start_line, self.y_start_line, endx, endy)

            #Istrinami listeneriai, kad nebebutu piesiami papildomi laidai.
            self.canvas.unbind('<Button-1>', self.mouse_click_listener)
            self.canvas.unbind('<Motion>', self.mouse_motion_listener)


    def mouse_moved(self, event):
        self.cur_mouse_posx = self.canvas.canvasx(event.x) # Paupdatinama peles pozicija, nepamirsti, kad perkonvertinu
        self.cur_mouse_posy = self.canvas.canvasy(event.y) # i canvas is karto koordinates

        if self.wire_draw_enabled == True:
            #Updatinami laido matmenys
            self.canvas.coords(self.wire_line, self.x_start_line, self.y_start_line, self.cur_mouse_posx, self.cur_mouse_posy)
        # self.wire_line = canvas.create_line()


class EVS(Components):
    def __init__(self, window, canvas, x, y, color, value, name, width = 70, height = 70):
        self.canvas = canvas
        self.window = window
        self.rect = canvas.create_oval(x, y, x + width, y + height, fill=color, outline="white", width = 5)


        # Dvieju kontaktu koordinates
        self.contact_coords = [[x-10, y+30, x-20, y+40], [x+80, y+30, x+90, y+40]]

        self.contact1 = canvas.create_oval(*(self.contact_coords[0]), fill=color, outline="white", width = 2)
        self.contact2 = canvas.create_oval(*(self.contact_coords[1]), fill=color, outline="white", width = 2)

        self.width = width
        self.height = height

        self.value = value
        self.name = name
        fullName = name + " " + str(value) + " V"
        # UZDETI CHEKA, AR IVEDZIAU SKAICIU!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.textBox = canvas.create_text(x+30, y+90, text=fullName, fill="white", font=("Helvetica", 12, 'bold'))

        self.x = x
        self.y = y

        self.offset_x = 0
        self.offset_y = 0

        self.canvas.tag_bind(self.rect, '<Button-1>', self.on_click) # Paspaudimui
        self.canvas.tag_bind(self.rect, '<B1-Motion>', self.on_drag) # Tempimui
        self.canvas.tag_bind(self.rect, '<Double-Button-1>', self.on_double_click) # Dvigubam paspaudimui


        self.linked_wire_objects = [[None, None], [None, None]] # max 2 # LABAI svarbu tai, kad pirmoje pozicijoje yra pirmas kontaktas, antroje - antras
        # Taip pat, cia issaugota, ar tas laidas nuo sio komponento prasideda, ar baigiasi, tai svarbu laido perpiesime
    
    # self.canvas.canvasx(event.x) # lango koordinates yra perverciamos i drobes koordinates

    def on_click(self, event):
        self.offset_x = self.canvas.canvasx(event.x)-self.x # apskaiciuojama ofesto pozicija, kad blokas butu tempiamas, nuo ten kur paspaudziau.
        self.offset_y = self.canvas.canvasy(event.y)-self.y # skaiciuojama nuo virsutinio kairiojo kampo
    
    def on_drag(self, event):
        x = self.canvas.canvasx(event.x) # Gaunu, kur tempiamas blokas 
        y = self.canvas.canvasy(event.y)

        x = x - self.offset_x # Pakoreguoju, kad blokas butu tempiamas, nuo ten, kur paspaude pele
        y = y - self.offset_y

        self.x = x # Irasau naujas koordinates
        self.y = y 

        # Keiciamios ir kontaktu koordinates
        self.contact_coords = [[x-10, y+30, x-20, y+40], [x+80, y+30, x+90, y+40]]
        # 

        self.canvas.coords(self.rect, x, y, x + self.width, y + self.height) # Tempiam rezistoriu
        self.canvas.coords(self.textBox, x+30, y+90) # Tempiam jo teksta, pridetas offestas, kad butu tekstas apacioj
        self.canvas.coords(self.contact1, *(self.contact_coords[0]))
        self.canvas.coords(self.contact2, *(self.contact_coords[1]))

        self.handle_connected_wire_move()

    def handle_connected_wire_move(self):
        [wire1, wire1_s_f] = self.linked_wire_objects[0]
        [wire2, wire_2_s_f] = self.linked_wire_objects[1]

        wires = [wire1, wire2] # Del for loopo ir kodo nekopinimo
        wire_positions = [wire1_s_f, wire_2_s_f] # Del for loopo ir kodo nekopinimo

        # Index del to, kad nereiktu kopijuoti kodo, tiesiog is eiles pereinama per listus ir koordinates atitinkamai pagal pozicija.
        for index, wire in enumerate(wires):
        # If del patikrinimo, ar ten yra laidas is viso
            if(wire is not None):
                if(wire_positions[index] == 0): # Jeigu, prie komponento kontakto laidas prasidejo, tai piesime ji nuo PABAIGOS KOORDIANCIU iki nauju kontakto koordinaciu
                    cx = self.contact_coords[index][0]
                    cy = self.contact_coords[index][1]
                    self.canvas.coords(wire.wire_line, wire.x_finish_line, wire.y_finish_line, cx, cy)
                    # Kita puse koordianciu turi buti perrasoma, nes ji pasikeis.
                    wire.x_start_line = cx
                    wire.y_start_line = cy
                else: # Jeigu, prie komponento kontakto laidas pasibaige, tai piesime ji nuo PRADZIOS KOORDIANCIU iki nauju kontakto koordinaciu
                    cx = self.contact_coords[index][0]
                    cy = self.contact_coords[index][1]
                    self.canvas.coords(wire.wire_line, wire.x_start_line, wire.y_start_line, cx, cy) 
                    # Kita puse koordianciu turi buti perrasoma, nes ji pasikeis.
                    wire.x_finish_line = cx
                    wire.y_finish_line = cy

            


    def on_double_click(self, event):
        self.mod_menu = tk.Toplevel(self.window)
        self.mod_menu.title("Modify EV source: ")
        self.mod_menu.geometry("500x500")

        self.entry = tk.Entry(self.mod_menu)
        self.entry.grid(column=1, row=0, sticky="nsew") # centruojam su nsew

        accept_button = tk.Button(self.mod_menu, text="OK", command=self.handle_mod_menu_close)
        accept_button.grid(column=1, row=1, sticky="nsew") # centruojam su nsew

        delete_button = tk.Button(self.mod_menu, text="Remove EV source", command=self.handle_component_delete)
        delete_button.grid(column=1, row=2, sticky="nsew") # centruojam su nsew


    def handle_mod_menu_close(self):
        # Pakeiciame teksta:
        modifiedText = self.entry.get()
        self.canvas.itemconfig(self.textBox, text=modifiedText)

        # Isnaikinam viska su mod_meniu
        self.mod_menu.destroy()
        del self.mod_menu, self.entry # Nzn ar cia butina

    def handle_component_delete(self):
        # Pakeiciame istrinam evs:
        
        ###
        # Isnaikinam viska su mod_meniu
        self.mod_menu.destroy()
        del self.mod_menu, self.entry # Nzn ar cia butina

    
        
            

class Resistor(Components):
    def __init__(self, window, canvas, x, y, color, value, name, width = 100, height = 40):
        self.canvas = canvas
        self.window = window
        self.rect = canvas.create_rectangle(x, y, x + width, y + height, fill=color, outline="white", width = 5)


        # Dvieju kontaktu koordinates
        self.contact_coords = [[x-10, y+15, x-20, y+25], [x+110, y+15, x+120, y+25]]

        self.contact1 = canvas.create_oval(*(self.contact_coords[0]), fill=color, outline="white", width = 3)
        self.contact2 = canvas.create_oval(*(self.contact_coords[1]), fill=color, outline="white", width = 3)

        self.width = width
        self.height = height

        self.value = value
        self.name = name
        fullName = name + " " + str(value) + " omh"
        # UZDETI CHEKA, AR IVEDZIAU SKAICIU!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.textBox = canvas.create_text(x+50, y+50, text=fullName, fill="white", font=("Helvetica", 12, 'bold'))

        self.x = x
        self.y = y

        self.offset_x = 0
        self.offset_y = 0

        self.canvas.tag_bind(self.rect, '<Button-1>', self.on_click) # Paspaudimui
        self.canvas.tag_bind(self.rect, '<B1-Motion>', self.on_drag) # Tempimui
        self.canvas.tag_bind(self.rect, '<Double-Button-1>', self.on_double_click) # Dvigubam paspaudimui


        self.linked_wire_objects = [[None, None], [None, None]] # max 2 # LABAI svarbu tai, kad pirmoje pozicijoje yra pirmas kontaktas, antroje - antras
        # Taip pat, cia issaugota, ar tas laidas nuo sio komponento prasideda, ar baigiasi, tai svarbu laido perpiesime
    
    # self.canvas.canvasx(event.x) # lango koordinates yra perverciamos i drobes koordinates

    def on_click(self, event):
        self.offset_x = self.canvas.canvasx(event.x)-self.x # apskaiciuojama ofesto pozicija, kad blokas butu tempiamas, nuo ten kur paspaudziau.
        self.offset_y = self.canvas.canvasy(event.y)-self.y # skaiciuojama nuo virsutinio kairiojo kampo
    
    def on_drag(self, event):
        x = self.canvas.canvasx(event.x) # Gaunu, kur tempiamas blokas 
        y = self.canvas.canvasy(event.y)

        x = x - self.offset_x # Pakoreguoju, kad blokas butu tempiamas, nuo ten, kur paspaude pele
        y = y - self.offset_y

        self.x = x # Irasau naujas koordinates
        self.y = y 

        # Keiciamios ir kontaktu koordinates
        self.contact_coords = [[x-10, y+15, x-20, y+25], [x+110, y+15, x+120, y+25]]
        # 

        self.canvas.coords(self.rect, x, y, x + self.width, y + self.height) # Tempiam rezistoriu
        self.canvas.coords(self.textBox, x+50, y+50) # Tempiam jo teksta, pridetas offestas, kad butu tekstas apacioj
        self.canvas.coords(self.contact1, *(self.contact_coords[0]))
        self.canvas.coords(self.contact2, *(self.contact_coords[1]))

        self.handle_connected_wire_move()

    def handle_connected_wire_move(self):
        [wire1, wire1_s_f] = self.linked_wire_objects[0]
        [wire2, wire_2_s_f] = self.linked_wire_objects[1]

        wires = [wire1, wire2] # Del for loopo ir kodo nekopinimo
        wire_positions = [wire1_s_f, wire_2_s_f] # Del for loopo ir kodo nekopinimo

        # Index del to, kad nereiktu kopijuoti kodo, tiesiog is eiles pereinama per listus ir koordinates atitinkamai pagal pozicija.
        for index, wire in enumerate(wires):
        # If del patikrinimo, ar ten yra laidas is viso
            if(wire is not None):
                if(wire_positions[index] == 0): # Jeigu, prie komponento kontakto laidas prasidejo, tai piesime ji nuo PABAIGOS KOORDIANCIU iki nauju kontakto koordinaciu
                    cx = self.contact_coords[index][0]
                    cy = self.contact_coords[index][1]
                    self.canvas.coords(wire.wire_line, wire.x_finish_line, wire.y_finish_line, cx, cy)
                    # Kita puse koordianciu turi buti perrasoma, nes ji pasikeis.
                    wire.x_start_line = cx
                    wire.y_start_line = cy
                else: # Jeigu, prie komponento kontakto laidas pasibaige, tai piesime ji nuo PRADZIOS KOORDIANCIU iki nauju kontakto koordinaciu
                    cx = self.contact_coords[index][0]
                    cy = self.contact_coords[index][1]
                    self.canvas.coords(wire.wire_line, wire.x_start_line, wire.y_start_line, cx, cy)
                    # Kita puse koordianciu turi buti perrasoma, nes ji pasikeis.
                    wire.x_finish_line = cx
                    wire.y_finish_line = cy 


    

    def on_double_click(self, event):
        self.mod_menu = tk.Toplevel(self.window)
        self.mod_menu.title("Modify resistor: ")
        self.mod_menu.geometry("300x300")

        self.entry = tk.Entry(self.mod_menu)
        self.entry.grid(column=1, row=0, sticky="nsew") # centruojam su nsew

        accept_button = tk.Button(self.mod_menu, text="OK", command=self.handle_mod_menu_close)
        accept_button.grid(column=1, row=1, sticky="nsew") # centruojam su nsew

        delete_button = tk.Button(self.mod_menu, text="Remove resistor", command=self.handle_component_delete)
        delete_button.grid(column=1, row=2, sticky="nsew") # centruojam su nsew


    def handle_mod_menu_close(self):
        # Pakeiciame teksta:
        modifiedText = self.entry.get()
        self.canvas.itemconfig(self.textBox, text=modifiedText)

        # Isnaikinam viska su mod_meniu
        self.mod_menu.destroy()
        del self.mod_menu, self.entry # Nzn ar cia butina

    def handle_component_delete(self):
        pass


# Lango framu isdestymas:
# window:
#    main_grid:
#       column0: subgrid1(addres, addwire, addevsource):
#       column1: canvas
#       column2: subgrid2(button, textbox)
# 

main_back_c = '#020f12'

button_bg_color1 = '#704c6a'
button_abg_color1 = '#735d6f'

button_bg_color2 = '#4c705b'
button_abg_color2 = '#5b7d69'


button_fg_c = 'BLACK'


def main():
    window = tk.Tk()
    window.title("Circuit simulator")

    main_grid = tk.Frame(window, bg=main_back_c, pady=15)
    main_grid.pack(fill="both", expand=True)

    subgrid1 = tk.Frame(main_grid, bg=main_back_c)
    subgrid1.grid(column=0, row=0)
    subgrid2 = tk.Frame(main_grid, bg=main_back_c)
    subgrid2.grid(column=2, row=0)


    canvas = tk.Canvas(main_grid, width=700, height=700, bg=main_back_c, highlightbackground='#4e4c70', highlightthickness=8)
    canvas.grid(column = 1, row = 0)
    
    # Elementu klases instantizacija
    elements = Screen_elements(window, main_grid, canvas) # window ir canvas perduodami wire, ev ir resistor klasem, kad zinotu, kur piesti viska


    # lambda del to, kad funkcija turi nueiti su parametrais
    add_resistor_button = tk.Button(
        subgrid1, 
        text="Resistor", 
        background=button_bg_color1,
        foreground=button_fg_c,
        activebackground=button_abg_color1,
        activeforeground=button_fg_c,
        highlightthickness=2,
        highlightbackground=button_bg_color1,
        highlightcolor='WHITE',
        width=13, 
        height=2,
        border=0,
        cursor='hand2',
        font=("Arial", 16, 'bold'),
        command=lambda: elements.add_resistor(1000, "R1")).grid(column = 0, row = 0, padx = 10, pady = 10)

    add_wire_button = tk.Button(subgrid1, 
        text="Wire",
        background=button_bg_color1,
        foreground=button_fg_c,
        activebackground=button_abg_color1,
        activeforeground=button_fg_c,
        highlightthickness=2,
        highlightbackground=button_bg_color1,
        highlightcolor='WHITE',
        width=13, 
        height=2,
        border=0,
        cursor='hand2',
        font=("Arial", 16, 'bold'),
        command=elements.add_wire).grid(column = 0, row = 1, padx = 10, pady = 10)

    add_evs_button = tk.Button(subgrid1, 
        text="EV source",
        background=button_bg_color1,
        foreground=button_fg_c,
        activebackground=button_abg_color1,
        activeforeground=button_fg_c,
        highlightthickness=2,
        highlightbackground=button_bg_color1,
        highlightcolor='WHITE',
        width=13, 
        height=2,
        border=0,
        cursor='hand2',
        font=("Arial", 16, 'bold'),
        command=lambda: elements.add_ev_source(12, "EV1")).grid(column = 0, row = 2, padx = 10, pady = 10)

    simulate_button = tk.Button(subgrid2,
        text="Simulate",
        background=button_bg_color2,
        foreground=button_fg_c,
        activebackground=button_abg_color2,
        activeforeground=button_fg_c,
        highlightthickness=2,
        highlightbackground=button_bg_color2,
        highlightcolor='WHITE',
        width=13, 
        height=2,
        border=0,
        cursor='hand2',
        font=("Arial", 16, 'bold')).grid(column = 0, row = 0, padx = 10, pady = 10)

    window.mainloop()

if __name__ == "__main__":
    main()