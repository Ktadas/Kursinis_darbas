import pytest
import unittest
from unittest.mock import Mock
from main import Wire
import tkinter as tk

class TestWire(unittest.TestCase):
    def setUp(self):
        # Tam kartui sukuriami pagrindiniai lango komponento wire klasei, kad nebutu inicializaciniu erroru
        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window)
        self.canvas.pack()


    def test_link_contact_to_wire_linkcompleted(self):
        # Sukuriama beveik tuscia wire klase
        wire = Wire(self.window, self.canvas, None, None)

        # Simuliuojami 2 pagrindiniai funkcijos objektai
        mock_component = Mock() # komponentas linkinamas prie laido
        # paimamas originalus listo apibrezimas
        mock_component.linked_wire_objects = [[None, None], [None, None]]

        # kintamasis issaugiantis, ar tai laido pradzia, ar pabaiga 1/0, tas pats ir su kontakto pozicija, atitinka listo nari, kur issaugotos koorinates
        s_f_state = True
        contact_place = 0

        # Iskvieciama funkcija
        result = wire.link_contact_to_wire(mock_component, s_f_state, contact_place)

        # Patestuojamas tiketinas rezultatas, kuris yra return 1

        self.assertEqual(result, 1)

        # Patestuojami ar parametrai pakeisti tinkamai:
        self.assertEqual(mock_component.linked_wire_objects[contact_place][0], wire)
        self.assertEqual(mock_component.linked_wire_objects[contact_place][1], s_f_state)


    def test_link_contact_to_wire_linkfailed(self):
        # Sukuriama beveik tuscia wire klase
        wire = Wire(self.window, self.canvas, None, None)

        # Simuliuojami 2 pagrindiniai funkcijos objektai
        mock_component = Mock() # komponentas linkinamas prie laido
        # Paimamas jau pilnas listas, nera svarbu, kas jame, tikrinamai funkcijai svarbu, kad bent kazkas butu
        mock_component.linked_wire_objects = [[123, 123], [123, 123]]

        # kintamasis issaugiantis, ar tai laido pradzia, ar pabaiga 1/0, tas pats ir su kontakto pozicija, atitinka listo nari, kur issaugotos koorinates
        s_f_state = True
        contact_place = 0

        # Iskvieciama funkcija
        result = wire.link_contact_to_wire(mock_component, s_f_state, contact_place)

        # Patestuojamas tiketinas rezultatas, kuris yra return None

        self.assertIsNone(result, "Result should be None")

        # Patestuojami ar parametrai nera lygus
        self.assertNotEqual(mock_component.linked_wire_objects[contact_place][0], wire)
        self.assertNotEqual(mock_component.linked_wire_objects[contact_place][1], s_f_state)

if __name__ == '__main__':
    unittest.main()