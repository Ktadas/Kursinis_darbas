import tkinter as tk
from tkinter import messagebox

import os
import math
import matplotlib.pyplot as plt
from datetime import datetime

from abc import ABC, abstractmethod

from component_cls_constants import EVSConstants, ResistorConstants, ContactOffsets, TextOffset


class ComponentBuilder(ABC):
    @abstractmethod
    def pass_gui_elements():
        pass

    @abstractmethod
    def set_origin_coordinates(self):
        pass

    @abstractmethod
    def set_main_parameters(self):
        pass

    @abstractmethod
    def init_draw_component_objects(self):
        pass

    @abstractmethod
    def init_draw_component_text(self):
        pass

    @abstractmethod
    def add_tag_binds(self):
        pass

    @abstractmethod
    def get_component(self):
        pass


class EVSComponentBuilder(ComponentBuilder):
    _evs_id_system = 1 # id trackeris

    def __init__(self, window, canvas):
        self.component = Component() # Pagrindinio ojekto inicializacija
        self.window = window
        self.canvas = canvas

    # komponentui suteikiamas id
        self.component._id = EVSComponentBuilder._evs_id_system
        EVSComponentBuilder._evs_id_system += 1

    # INIT metodu implementacija
    def pass_gui_elements(self):
        self.component.canvas = self.canvas
        self.component.window = self. window

    def set_origin_coordinates(self):
        # Pagrindines komponento koordinates
        self.component.x = EVSConstants.ORIGIN_X
        x = EVSConstants.ORIGIN_X
        self.component.y = EVSConstants.ORIGIN_Y
        y = EVSConstants.ORIGIN_Y

        # Perkelimo offseto koordinaciu kintamieji

        self.component.offset_x = 0
        self.component.offset_y = 0

        # Pagrindines komponento kontaktu koordinates
        self.component.contact_coords = [
            [x+EVSConstants.CONTACT1_OFFSET.x1, y+EVSConstants.CONTACT1_OFFSET.y1, 
             x+EVSConstants.CONTACT1_OFFSET.x2, y+EVSConstants.CONTACT1_OFFSET.y2],
            [x+EVSConstants.CONTACT2_OFFSET.x1, y+EVSConstants.CONTACT2_OFFSET.y1, 
             x+EVSConstants.CONTACT2_OFFSET.x2, y+EVSConstants.CONTACT2_OFFSET.y2]]
        
        # Irasomi ofsetai, kad objektas galetu tai pasiekti, kai reikia perkelti komponenta ir ji perpiesti
        self.component.CONTACT1_OFFSET = EVSConstants.CONTACT1_OFFSET 
        self.component.CONTACT2_OFFSET = EVSConstants.CONTACT2_OFFSET

    def set_main_parameters(self):
        self.component.value = EVSConstants.DEFAULT_VALUE
        self.component.name = EVSConstants.DEFAULT_NAME
        self.component.symbol = EVSConstants.DEFAULT_SYMBOL
        name = EVSConstants.DEFAULT_NAME
        self.component.fullName = name + str(self.component._id) + " " + str(self.component.value) + " " + self.component.symbol
        self.component.width = EVSConstants.DEFAULT_WIDTH
        self.component.height = EVSConstants.DEFAULT_HEIGHT

    def init_draw_component_objects(self):
        self.component.contact_1_obj = self.canvas.create_oval(*(self.component.contact_coords[EVSConstants.CONTACT1_LIST_PLACE]), 
                                                          fill=EVSConstants.DEFAULT_FILL_COLOR, 
                                                          outline=EVSConstants.DEFAULT_OUTLINE_COLOR, 
                                                          width = EVSConstants.DEFAULT_CONTACT_OUTLINE_WIDTH)
        self.component.contact_2_obj = self.canvas.create_oval(*(self.component.contact_coords[EVSConstants.CONTACT2_LIST_PLACE]), 
                                                          fill=EVSConstants.DEFAULT_FILL_COLOR, 
                                                          outline=EVSConstants.DEFAULT_OUTLINE_COLOR, 
                                                          width = EVSConstants.DEFAULT_CONTACT_OUTLINE_WIDTH)
        x = EVSConstants.ORIGIN_X
        y = EVSConstants.ORIGIN_Y
        self.component.comp_body_obj = self.canvas.create_oval(x, y, x + self.component.width, y + self.component.height, 
                                                      fill=EVSConstants.DEFAULT_FILL_COLOR, 
                                                      outline=EVSConstants.DEFAULT_OUTLINE_COLOR, 
                                                      width = EVSConstants.DEFAULT_BODY_OUTLINE_WIDTH)

    def init_draw_component_text(self):
        x = EVSConstants.ORIGIN_X
        y = EVSConstants.ORIGIN_Y

        # Irasomi ofsetai, kad objektas galetu tai pasiekti, kai reikia perkelti komponenta ir ji perpiesti
        self.component.TEXT_OFFSET = EVSConstants.TEXT_OFFSET

        self.component.textBox = self.canvas.create_text(x+EVSConstants.TEXT_OFFSET.x,
                                                         y+EVSConstants.TEXT_OFFSET.y, 
                                                         text=self.component.fullName,
                                                         fill=EVSConstants.DEFAULT_FONT_COLOR,
                                                         font=EVSConstants.DEFAULT_COMPONENT_FONT)

    def add_tag_binds(self):
        self.canvas.tag_bind(self.component.comp_body_obj, '<Button-1>', self.component.on_click) # Paspaudimui
        self.canvas.tag_bind(self.component.comp_body_obj, '<B1-Motion>', self.component.on_drag) # Tempimui
        self.canvas.tag_bind(self.component.comp_body_obj, '<Double-Button-1>', self.component.on_double_click) # Dvigubam paspaudimui

    def get_component(self):
        return self.component


class ResistorComponentBuilder(ComponentBuilder):
    _resistor_id_system = 1 # id trackeris

    def __init__(self, window, canvas):
        self.component = Component() # Pagrindinio ojekto inicializacija
        self.window = window
        self.canvas = canvas

        # komponentui suteikiamas id
        self.component._id = ResistorComponentBuilder._resistor_id_system
        ResistorComponentBuilder._resistor_id_system += 1

    # INIT metodu implementacija
    def pass_gui_elements(self):
        self.component.canvas = self.canvas
        self.component.window = self. window

    def set_origin_coordinates(self):
        # Pagrindines komponento koordinates
        self.component.x = ResistorConstants.ORIGIN_X
        x = ResistorConstants.ORIGIN_X
        self.component.y = ResistorConstants.ORIGIN_Y
        y = ResistorConstants.ORIGIN_Y

        # Perkelimo offseto koordinaciu kintamieji

        self.component.offset_x = 0
        self.component.offset_y = 0

        # Pagrindines komponento kontaktu koordinates
        self.component.contact_coords = [
            [x+ResistorConstants.CONTACT1_OFFSET.x1, y+ResistorConstants.CONTACT1_OFFSET.y1, 
             x+ResistorConstants.CONTACT1_OFFSET.x2, y+ResistorConstants.CONTACT1_OFFSET.y2],
            [x+ResistorConstants.CONTACT2_OFFSET.x1, y+ResistorConstants.CONTACT2_OFFSET.y1, 
             x+ResistorConstants.CONTACT2_OFFSET.x2, y+ResistorConstants.CONTACT2_OFFSET.y2]]
        
        self.component.CONTACT1_OFFSET = ResistorConstants.CONTACT1_OFFSET 
        self.component.CONTACT2_OFFSET = ResistorConstants.CONTACT2_OFFSET

    def set_main_parameters(self):
        self.component.value = ResistorConstants.DEFAULT_VALUE
        self.component.symbol = ResistorConstants.DEFAULT_SYMBOL
        self.component.name = ResistorConstants.DEFAULT_NAME
        name = ResistorConstants.DEFAULT_NAME
        self.component.fullName = name + str(self.component._id) + " " + str(self.component.value) + " " + self.component.symbol
        self.component.width = ResistorConstants.DEFAULT_WIDTH
        self.component.height = ResistorConstants.DEFAULT_HEIGHT

    def init_draw_component_objects(self):
        self.component.contact_1_obj = self.canvas.create_oval(*(self.component.contact_coords[ResistorConstants.CONTACT1_LIST_PLACE]), 
                                                          fill=ResistorConstants.DEFAULT_FILL_COLOR, 
                                                          outline=ResistorConstants.DEFAULT_OUTLINE_COLOR, 
                                                          width = ResistorConstants.DEFAULT_CONTACT_OUTLINE_WIDTH)
        self.component.contact_2_obj = self.canvas.create_oval(*(self.component.contact_coords[ResistorConstants.CONTACT2_LIST_PLACE]), 
                                                          fill=ResistorConstants.DEFAULT_FILL_COLOR, 
                                                          outline=ResistorConstants.DEFAULT_OUTLINE_COLOR, 
                                                          width = ResistorConstants.DEFAULT_CONTACT_OUTLINE_WIDTH)
        x = ResistorConstants.ORIGIN_X
        y = ResistorConstants.ORIGIN_Y
        self.component.comp_body_obj = self.canvas.create_rectangle(x, y, x + self.component.width, y + self.component.height, 
                                                      fill=ResistorConstants.DEFAULT_FILL_COLOR, 
                                                      outline=ResistorConstants.DEFAULT_OUTLINE_COLOR, 
                                                      width = ResistorConstants.DEFAULT_BODY_OUTLINE_WIDTH)

    def init_draw_component_text(self):
        x = ResistorConstants.ORIGIN_X
        y = ResistorConstants.ORIGIN_Y

        self.component.TEXT_OFFSET = ResistorConstants.TEXT_OFFSET

        self.component.textBox = self.canvas.create_text(x+ResistorConstants.TEXT_OFFSET.x,
                                                         y+ResistorConstants.TEXT_OFFSET.y, 
                                                         text=self.component.fullName, 
                                                         fill=ResistorConstants.DEFAULT_FONT_COLOR, 
                                                         font=ResistorConstants.DEFAULT_COMPONENT_FONT)

    def add_tag_binds(self):
        self.canvas.tag_bind(self.component.comp_body_obj, '<Button-1>', self.component.on_click) # Paspaudimui
        self.canvas.tag_bind(self.component.comp_body_obj, '<B1-Motion>', self.component.on_drag) # Tempimui
        self.canvas.tag_bind(self.component.comp_body_obj, '<Double-Button-1>', self.component.on_double_click) # Dvigubam paspaudimui

    def get_component(self):
        return self.component


class ComponentDirector():
    def buildComponent(self, builder):
        # Init sekos implementacija
        builder.pass_gui_elements()
        builder.set_origin_coordinates()
        builder.set_main_parameters()
        builder.init_draw_component_objects()
        builder.init_draw_component_text()
        builder.add_tag_binds()

        return builder.get_component()
    

class ScreenElements:
    def __init__(self, main_window, window, canvas):
        self.resistors = []
        self.evsources = []
        self.wires = []
        self.canvas = canvas
        self.window = window
        self.main_window = main_window
        # self.resistorCount Neaisku, ar reikes, ar tiesiog su listo dydziu apsieisiu

        self.observers = [] # objektai, kuriem reikia atnaujinti dependacy injection, kol kas tik SimulatorEngine

        self.popup = None # Palceholderis zinutes popupui, None dar del patikrinimo, ar jau atidarytas langas toks, kad nesikartotu. *****LEGACY*****

        # Pagrindinis komponentu buildinimo objektas
        self.component_director = ComponentDirector()

    def add_resistor(self):
        if len(self.resistors) > 1:
            print("Max rezistoriu skaicius yra 2")
            # self.display_short_message("Max rezistoriu skaicius yra 2") LEGACY
            messagebox.showerror("Error", "Max number of resistors is 2")
        else:
            resistor = ResistorComponentBuilder(self.window, self.canvas) # Komponento builderis
            resistor_obj = self.component_director.buildComponent(resistor) # Inicializuojami parametrai, grazinamas paruostas objektas

            self.resistors.append(resistor_obj)
            self.observer_notify() # Atnaujinami listai, tiem, kas turi depnedancy injection
            print(f"Appended resistor {self.resistors[-1]}") # paskutini sarase parodau

    def add_ev_source(self):
        if len(self.evsources) > 0:
            print("Max EV saltiniu skaicius yra 1")
            # self.display_short_message("Max EV saltiniu skaicius yra 1")
            messagebox.showerror("Error", "Max number of EV sources is 1")
        else:
            evsource = EVSComponentBuilder(self.window, self.canvas)
            evsource_obj = self.component_director.buildComponent(evsource)

            self.evsources.append(evsource_obj)
            self.observer_notify() # Atnaujinami listai, tiem, kas turi depnedancy injection
            print(f"Appended wire {self.evsources[-1]}") # paskutini sarase parodau

    def add_wire(self):
        if len(self.wires) > 2:
            print("Max laidu skaicius yra 3")
            # self.display_short_message("Max laidu skaicius yra 3")
            messagebox.showerror("Error", "Max number of wires is 3")
        else:
            self.wires.append(Wire(self.window, self.canvas, self.resistors, self.evsources))
            print(f"Appended wire {self.wires[-1]}") # paskutini sarase parodau

    def add_observer(self, observer):
        # Jeigu nera dependacy injection sekimo, tai ji pridedame
        if observer not in self.observers:
            self.observers.append(observer)

    def observer_notify(self):
        # Paupdatinami nauji listai, jeigu prideti nauji komponentai.
        for observer in self.observers:
            observer.updateComponentLists(self.resistors, self.evsources)
        
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

    def open_delete_component_window(self):
        # atidaromas langas, kuris parodo visus komponentus, kuriuos galima trinti
        pass

    def delete_component(self):
        # component.handle_component_delete
        # wire.handle_component_delete
        pass
            

class SimulatorEngine():
    def __init__(self, window):
        self.resistors = []
        self.evsources = []
        self.window = window

    def updateComponentLists(self, resistors, evsources):
        self.resistors = resistors
        self.evsources = evsources
    
    def basic_series_simulation_start(self):
        if len(self.evsources) == 0:
            messagebox.showerror("Error", "The circuit has no EV sources\n Not possible to complete simulation")
            return -1
        elif len(self.resistors) == 0:
            messagebox.showerror("Error", "The circuit has no resistors\n Not possible to complete simulation")
            return -1
        else:
            # Jeigu komponentu pakanka, simuliacija pradedama
            self.complete_basic_series_simulation()

    def complete_basic_series_simulation(self):
        # gaunama pagrindinio saltinio itampa
        # kadangi, simuliatorius kol kas leidzia tik viena saltini, tai paimamas tik pirmas ir vienintelis narys 
        mainvoltage = self.evsources[0].return_component_value()

        resistor_values = []

        for resistor in self.resistors:
            resistor_values.append((resistor.return_component_name(), resistor.return_component_value())) # Surasomi komponentai i ir ju vertes i lista

        # Pagal Omo desni apskaiciuojama visos grandines srove
        circuit_current = mainvoltage/sum(value for _, value in resistor_values) # ismetamas pirmas narys - vardas sumuojant

        # Pagal Omo desni U = RI (U = R_i*circuit_current) apskaiciuojamos rezistoriu itampos
        resistor_voltages = [(name, r_i*circuit_current) for name, r_i in resistor_values] # perrasomi rezistoriu vardai ir apskaiciuojamos ju itampos

        # Potencialu diagrama
        image_to_display = self.draw_potential_diagram(resistor_voltages)

        self.show_complete_basic_series_simulation_results(mainvoltage, circuit_current, resistor_voltages, image_to_display)

    def draw_potential_diagram(self, resistor_voltages):
        # Sukuriamos asiu vertes
        x = [name for name, _ in resistor_voltages]
        y = [value for _, value in resistor_voltages]

        print(x)
        print(y)

        # Sukuriama potencialu diagrama, interfacas kaip per matlab
        plt.close() # Uzdaromos praeitos diagramos, kad nebutu piesiama ant virsaus
        plt.plot(x, y, "-o")
        plt.title("Potential diagram")
        plt.xlabel("Components")
        plt.ylabel("Potentials, V")

        now = datetime.now()
        time_string = now.strftime("%Y%m%d_%H%M%S")

        # Sukuriamas failo vardas su path
        path_name = "Kursinis_darbas/Simulation_results/"
        image_name = f"{path_name}potential_diagram{time_string}.png"

        # Jeigu nera, sukuriamas path
        if not os.path.exists(path_name):
            os.makedirs(path_name)

        # Issaugoma diagrama
        plt.savefig(image_name)

        return image_name

    def show_complete_basic_series_simulation_results(self, mainvoltage, circuit_current, resistor_voltages, image_to_display):
        self.results_window = tk.Toplevel(self.window) # Naujas top lygio langas rezultatu atvaizdavimui
        self.results_window.title("Simulation results")
        self.results_window.geometry("640x800")

        listbox = tk.Listbox(self.results_window) # Elementas listams suvesti
        listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True) # Listo teksto komponento centravimas ir t.t.

        image = tk.PhotoImage(file=image_to_display)
        image_label = tk.Label(self.results_window, image=image)
        image_label.image = image # Kad neissitrintu diagrama
        image_label.pack(padx=10, pady=10)
        image_label.pack(expand=True)

        listbox.insert(tk.END, f"Circuit voltage: {mainvoltage:.7f} V") # Atvaizduojami grandines itampa ir srove
        listbox.insert(tk.END, f"Circuit current: {circuit_current:.7f} A")

        for name, voltage in resistor_voltages: # Atvaizduojamos rezistoriu itampos
            listbox.insert(tk.END, f"{name}: {voltage:.7f} V")

        # auto issaugojimas i faila
        self.save_results_txt(mainvoltage, circuit_current, resistor_voltages)

    def save_results_txt(self, mainvoltage, circuit_current, resistor_voltages):
        # Sukuriamas failo vardas su path
        path_name = "Kursinis_darbas/Simulation_results/"
        
        # Jeigu nera, sukuriamas path
        if not os.path.exists(path_name):
            os.makedirs(path_name)

        now = datetime.now()
        time_string = now.strftime("%Y%m%d_%H%M%S")

        with open(f"{path_name}Simulation_results.txt", 'a') as file: # Atidaromas failas, append rezimu
            # Irasomas simuliacijos laikas:
            file.write(f"Simulation time: {time_string}| ")

            # Irasomi grandines itampa ir srove
            file.write(f"Circuit voltage: {mainvoltage:.7f} V |")
            file.write(f"Circuit current: {circuit_current:.7f} A |")

            for name, voltage in resistor_voltages: # Atvaizduojamos rezistoriu itampos
                file.write(f"{name}: {voltage:.7f} V|")

            file.write("\n")

    def load_results_from_txt(self):
        path_name = "Kursinis_darbas/Simulation_results/"

        try:
            with open(f"{path_name}Simulation_results.txt", 'r') as file:
                file_read_text = file.read()
            
            results_window = tk.Toplevel(self.window)
            results_window.title("Past simulation results")
            results_window.geometry("600x400") 

            # Scrolinimo funkcija
            scrollbar = tk.Scrollbar(results_window)
            scrollbar.pack(side='right', fill='y')

            # Teksto laukas
            content_text = tk.Text(results_window, wrap='word', yscrollcommand=scrollbar.set)
            content_text.insert('1.0', file_read_text)
            content_text['state'] = 'disabled' # Negalima redaguoti teksto
            content_text.pack(expand=True, fill='both')

            # Scrolinimo konfiguracija papildoma
            scrollbar.config(command=content_text.yview)

        except FileNotFoundError:
            messagebox.showerror("Error", "File was not found")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


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
    
    def handle_wire_delete():
        # del wire tag binds
        # del wire line object
        pass


class Component():
    def __init__(self):
        self.canvas = None
        self.window = None

        self._id = None
        
        self.x = None
        self.y = None
        self.offset_x = None
        self.offset_y = None
        self.contact_coords = None
        self.CONTACT1_OFFSET = None
        self.CONTACT2_OFFSET = None

        self.value = None
        self.symbol = None
        self.name = None
        self.fullName = None
        self.width = None
        self.height = None

        self.contact_1_obj = None
        self.contact_2_obj = None
        self.comp_body_obj = None

        self.textBox = None
        self.TEXT_OFFSET = None

        # canvas tag bindai
        # 
        # canvas tag bindai end


        self.linked_wire_objects = [[None, None], [None, None]] # max 2 # LABAI svarbu tai, kad pirmoje pozicijoje yra pirmas kontaktas, antroje - antras
        # Taip pat, cia issaugota, ar tas laidas nuo sio komponento prasideda, ar baigiasi, tai svarbu laido perpiesime
    
    def offset_coordinates(self, origin_x, origin_y, offsets):
        if isinstance(offsets, ContactOffsets): # Du offsetinimo varinatai, nes tekstui reikia tik vienu koordinaciu offsetintu
            return [
                origin_x + offsets.x1, 
                origin_y + offsets.y1, 
                origin_x + offsets.x2, 
                origin_y + offsets.y2
            ]
        elif isinstance(offsets, TextOffset):
            return [
                origin_x + offsets.x,
                origin_y + offsets.y
            ]

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
        self.contact_coords = [self.offset_coordinates(x, y, self.CONTACT1_OFFSET), self.offset_coordinates(x, y, self.CONTACT2_OFFSET)]
        # 

        self.canvas.coords(self.comp_body_obj, x, y, x + self.width, y + self.height) # Tempiam rezistoriu
        self.canvas.coords(self.textBox, *(self.offset_coordinates(x, y, self.TEXT_OFFSET))) # Tempiam jo teksta, pridetas offestas, kad butu tekstas apacioj
        
        self.canvas.coords(self.contact_1_obj, *(self.contact_coords[0]))
        self.canvas.coords(self.contact_2_obj, *(self.contact_coords[1]))

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
        self.mod_menu.title("Modifing " + self.fullName + " : ")
        self.mod_menu.geometry("500x500")

        # Centruojami komponentai
        self.mod_menu.grid_columnconfigure(0, weight=1)
        self.mod_menu.grid_columnconfigure(2, weight=1)
        self.mod_menu.grid_rowconfigure(0, weight=1)
        self.mod_menu.grid_rowconfigure(3, weight=1)

        label = tk.Label(self.mod_menu, text="Enter a new value: ")
        label.grid(column=1, row=0, sticky="nsew") # centruojam su nsew

        self.entry = tk.Entry(self.mod_menu)
        self.entry.grid(column=1, row=1, sticky="nsew") # centruojam su nsew

        accept_button = tk.Button(self.mod_menu, text="OK", command=self.handle_mod_menu_close)
        accept_button.grid(column=1, row=2, sticky="nsew") # centruojam su nsew

    def handle_mod_menu_close(self):
        # Pakeiciame teksta:
        modifiedValue = self.entry.get()

        if modifiedValue.isdigit() and int(modifiedValue) != 0:
            self.value = int(modifiedValue) # Irasoma nauja komponento verte

            # Suformatuojam nauja komponento varda ir irasome ji teksto lauka
            self.fullName = f"{self.name}{self._id} {modifiedValue} {self.symbol}"
            self.canvas.itemconfig(self.textBox, text=self.fullName)

            # Isnaikinam viska su mod_meniu
            self.mod_menu.destroy()
            del self.mod_menu, self.entry # Nzn ar cia butina
        else:
            messagebox.showerror("Invalid Input", "Please enter a valid number without spaces or zero.")

    def handle_component_delete(self):
        # del component tag binds
        # del component canvas body object
        # del component canvas text object

        # return wires to be deleted???
        pass

    def return_component_value(self):
        return self.value

    def return_component_name(self):
        return f"{self.name}{self._id}"




class StyledButtonInit(tk.Button):
    # Pagrindines naudojamos spalvos
    main_back_c = '#020f12'
    button_bg_color1 = '#704c6a'
    button_abg_color1 = '#735d6f'
    button_bg_color2 = '#4c705b'
    button_abg_color2 = '#5b7d69'
    button_fg_c = 'BLACK'


    def __init__(self, parent, text, command = None, style='greenstyle', **kwargs):
        self.button_styles = {
            'greenstyle': {
                'background': StyledButtonInit.button_bg_color2,
                'foreground': StyledButtonInit.button_fg_c,
                'activebackground': StyledButtonInit.button_abg_color2,
                'activeforeground': StyledButtonInit.button_fg_c,
                'highlightthickness': 2,
                'highlightbackground': StyledButtonInit.button_bg_color2,
                'highlightcolor': 'WHITE',
                'width': 13, 
                'height': 2,
                'border': 0,
                'cursor': 'hand2',
                'font': ("Arial", 16, 'bold')
            },
            'purplestyle': {
                'background': StyledButtonInit.button_bg_color1,
                'foreground': StyledButtonInit.button_fg_c,
                'activebackground': StyledButtonInit.button_abg_color1,
                'activeforeground': StyledButtonInit.button_fg_c,
                'highlightthickness': 2,
                'highlightbackground': StyledButtonInit.button_bg_color1,
                'highlightcolor': 'WHITE',
                'width': 13, 
                'height': 2,
                'border': 0,
                'cursor': 'hand2',
                'font': ("Arial", 16, 'bold')
            }
        }
        # isrenkama is dictionary, reikiamas stilius, neradus default yra zalias mygtukas
        chosen_style = self.button_styles.get(style, self.button_styles['greenstyle'])
        chosen_style.update(**kwargs) # Pridedami ir papildomi parametrai paduoti, jeigu reikia
        super().__init__(parent, text=text, command=command, **chosen_style) # Inicializuojama tk.Button klase, perduodami tie patys parametrai

# Lango framu isdestymas:
# window:
#    main_grid:
#       column0: subgrid1(addres, addwire, addevsource):
#       column1: canvas
#       column2: subgrid2(button, textbox)
# 

class ClsMainUI(StyledButtonInit):
    def __init__(self):
        self.window = None
        self.main_grid = None
        self.subgrid1 = None
        self.subgrid2 = None

        self.canvas = None

        self.screenElements = None # Pagrindinis teisingo komponentu pridejimo objektas
        self.simulatorEngine = None # Pagrindinis simuliavimo objektas

    # Inicializuojamas ir atidaromas pagrindinis programos exe langas
    def initMainWindow(self):
        self.window = tk.Tk() 
        self.window.title("Circuit simulator")

    # Inicializuojami layouto komponentai, pagrindinis lango grid'as ir jo subgrid'ai, taip pat canvas objektas, kuris talpins komponentus
    def setupMainWindowComponents(self):
        self.main_grid = tk.Frame(self.window, bg=ClsMainUI.main_back_c, pady=15)
        self.main_grid.pack(expand=True)

        self.subgrid1 = tk.Frame(self.main_grid, bg=ClsMainUI.main_back_c)
        self.subgrid1.grid(column=0, row=0)
        self.subgrid2 = tk.Frame(self.main_grid, bg=ClsMainUI.main_back_c)
        self.subgrid2.grid(column=2, row=0)

        self.canvas = tk.Canvas(self.main_grid, width=900, height=700, bg=ClsMainUI.main_back_c, highlightbackground='#4e4c70', highlightthickness=8)
        self.canvas.grid(column = 1, row = 0)

    # Inicializuojamos pagrindines dvi simuliatoriaus klases, pacio simuliatoriaus ir piestu elementu valdymo klase.
    def initMainSimulatorCls(self):
        self.screenElements = ScreenElements(self.window, self.main_grid, self.canvas) # window ir canvas perduodami, kad visi objektai zinotu, kur piesti viska reikia
        self.simulatorEngine = SimulatorEngine(self.window) 
        self.screenElements.add_observer(self.simulatorEngine)

    # Sukuriami mygtukai, ju listeneriai ir prisegamos funkcijos
    def setupButtonListeners(self):
        add_resistor_button = StyledButtonInit(
            self.subgrid1, 
            text="Add Resistor",
            style='purplestyle',
            command=self.screenElements.add_resistor)
        add_resistor_button.grid(column = 0, row = 0, padx = 10, pady = 10)

        add_wire_button = StyledButtonInit(
            self.subgrid1, 
            text="Add Wire",
            style='purplestyle',
            command=self.screenElements.add_wire)
        add_wire_button.grid(column = 0, row = 1, padx = 10, pady = 10)

        add_evs_button = StyledButtonInit(
            self.subgrid1, 
            text="Add EV source",
            style='purplestyle',
            command=self.screenElements.add_ev_source)
        add_evs_button.grid(column = 0, row = 2, padx = 10, pady = 10)
        
        delete_button = StyledButtonInit(
            self.subgrid1,
            text="Delete\ncomponent",
            style='greenstyle')
        delete_button.grid(column = 0, row = 3, padx = 10, pady = 10)

        simulate_button = StyledButtonInit(
            self.subgrid2,
            text="Simulate",
            style='greenstyle',
            command=self.simulatorEngine.basic_series_simulation_start)
        simulate_button.grid(column = 0, row = 0, padx = 10, pady = 10)

        results_button = StyledButtonInit(
            self.subgrid2,
            text="All\nresults",
            style='greenstyle',
            command=self.simulatorEngine.load_results_from_txt)
        results_button.grid(column = 0, row = 1, padx = 10, pady = 10)

    # Run:)
    def runUI(self):
        self.window.mainloop()


def main():
    mainProgram = ClsMainUI()
    mainProgram.initMainWindow()
    mainProgram.setupMainWindowComponents()
    mainProgram.initMainSimulatorCls()
    mainProgram.setupButtonListeners()
    mainProgram.runUI()    



if __name__ == "__main__":
    main()