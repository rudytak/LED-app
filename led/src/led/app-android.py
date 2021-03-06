"""
UI for local LED server communication.
"""
import sys
import toga
from toga.style import Pack
from toga.style.pack import ALIGNMENT_CHOICES, COLUMN, ROW
from toga.widgets.base import Widget
from toga.widgets.canvas import Canvas
from travertino.colors import color
from .post import post

class LED(toga.App):

    def startup(self):
        # MAIN DIV
        main_box = toga.Box(style=Pack(direction=COLUMN))

        # ESP ID
        self.esp_ids = ["1","2"]
        self.esp_ids_real = [1,2]
        esp_id_label = toga.Label(
            'ESP ID: ',
            style=Pack(padding=(0, 10), width=100)
        )
        self.esp_id_select = toga.Selection(items=self.esp_ids, style=Pack(flex=1))

        esp_id = toga.Box(style=Pack(direction=ROW, padding=5))
        esp_id.add(esp_id_label)
        esp_id.add(self.esp_id_select) 
        main_box.add(esp_id)
    
        # MODE
        self.modes = ["OFF","Solid color", "Fill up", "Fill up reverse", "Fill and drain", "Fill and reverse", "Static rainbow", "Static rainbow reverse", "Propagating rainbow", "Propagating rainbow reverse", "Rainbow fill", "Rainbow fill reverse", "Rainbow fill and drain", "Rainbow fill and drain reverse", "Two color pulsing", "Color with black pulse", "Color with white pulsing", "Two color flashing", "Color with black flash", "Color with white flash", "Two color lerping", "Color with black lerp", "Points in", "Points in & out"]
        self.mode_ids = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,27,28]
        mode_label = toga.Label(
            'Mode: ',
            style=Pack(padding=(0, 10), width=100)
        )
        self.mode_select = toga.Selection(items=self.modes, style=Pack(flex=1))

        mode = toga.Box(style=Pack(direction=ROW, padding=5))
        mode.add(mode_label)
        mode.add(self.mode_select) 
        main_box.add(mode)

        # SPEED
        self.speed_label = toga.Label(
            'Speed (100): ',
            style=Pack(padding=(0, 10), width=100)
        )
        def updateSpeedLabel(caller):
            s = str(int(caller.value))
            #if(s=="0"): s = "min"
            #if(s=="100"): s="max"
            self.speed_label.text = "Speed ("+s+"): "
        self.speed_slider = toga.Slider(
                    range=(1,100),
                    on_change = updateSpeedLabel,
                    default=50,
                    style= Pack(width=200)
                )

        speed = toga.Box(style=Pack(direction=ROW, padding=0))
        speed.add(self.speed_label)
        speed.add(self.speed_slider) 
        main_box.add(speed)

        # INTENSITY
        self.intensity_label = toga.Label(
            'Intensity (100): ',
            style=Pack(padding=(0, 10), width=100)
        )
        def updateIntensityLabel(caller):
            s = str(int(caller.value))
            #if(s=="0"): s = "min"
            #if(s=="100"): s="max"
            self.intensity_label.text = "Intensity ("+s+"): "
        self.intensity_slider = toga.Slider(
                    range=(0,100),
                    on_change = updateIntensityLabel,
                    default=50,
                    style= Pack(width=200)
                )

        intensity = toga.Box(style=Pack(direction=ROW, padding=0))
        intensity.add(self.intensity_label)
        intensity.add(self.intensity_slider) 
        main_box.add(intensity)

        # HSV MODE
        self.hsv_modes = ["Regular HSV","Power-conscious HSV", "Sine wave"]
        self.hsv_mode_ids = [1,2,3]
        hsv_mode_label = toga.Label(
            'HSV Mode: ',
            style=Pack(padding=(0, 10), width=100)
        )
        self.hsv_mode_select = toga.Selection(items=self.hsv_modes, style=Pack(flex=1))

        hsv_mode = toga.Box(style=Pack(direction=ROW, padding=5))
        hsv_mode.add(hsv_mode_label)
        hsv_mode.add(self.hsv_mode_select) 
        main_box.add(hsv_mode)

        # WAVE COUNT
        wave_label = toga.Label(
            'Wave count: ',
            style=Pack(padding=(0, 10), width=100)
        )
        self.wave_num_input = toga.Selection(items=[1,2,3,4,5,6,7,8,9,10] ,style=Pack(flex=1))

        wave = toga.Box(style=Pack(direction=ROW, padding=5))
        wave.add(wave_label)
        wave.add(self.wave_num_input) 
        main_box.add(wave)
        
        # COLOUR PICKERS
        #picker_box = toga.Box(style=Pack(direction=ROW, padding=(0,5), alignment="center", flex=2))
        #self.picker1 = ColorPicker("Primary color")
        #self.picker2 = ColorPicker("Secondary color")
        #picker_box.add(self.picker1,toga.Divider(direction=1, style=Pack(height=120)), self.picker2)
        #main_box.add(picker_box)

        # COLOR 1        
        main_box.add(toga.Label(
            'Primary color',
            style=Pack(padding=(0,10), width=120)
        ))
        b_1r = toga.Box(style=Pack(direction=ROW, padding=5))
        b_1r.add(
            toga.Label(
                "R",
                style=Pack(padding=(0,10), color="#ff0000")
            )
        )
        s_1r = toga.Slider(
            range=(0,255),
            default=128,
            style= Pack(width=200)
        )
        b_1r.add(s_1r)

        b_1g = toga.Box(style=Pack(direction=ROW, padding=5))
        b_1g.add(
            toga.Label(
                "G",
                style=Pack(padding=(0,10), color="#00ff00")
            )
        )
        s_1g = toga.Slider(
            range=(0,255),
            default=128,
            style= Pack(width=200)
        )
        b_1g.add(s_1g)

        b_1b = toga.Box(style=Pack(direction=ROW, padding=5))
        b_1b.add(
            toga.Label(
                "B",
                style=Pack(padding=(0,10), color="#0000ff")
            )
        )
        s_1b = toga.Slider(
            range=(0,255),
            default=128,
            style= Pack(width=200)
        )
        b_1b.add(s_1b)

        main_box.add(b_1r)
        main_box.add(b_1g)
        main_box.add(b_1b)

        self.sliders1 = [s_1r, s_1g, s_1b]

        # COLOR 2
        main_box.add(toga.Label(
            'Secondary color',
            style=Pack(padding=(0,10), width=120)
        ))
        b_2r = toga.Box(style=Pack(direction=ROW, padding=5))
        b_2r.add(
            toga.Label(
                "R",
                style=Pack(padding=(0,10), color="#ff0000")
            )
        )
        s_2r = toga.Slider(
            range=(0,255),
            default=128,
            style= Pack(width=200)
        )
        b_2r.add(s_2r)

        b_2g = toga.Box(style=Pack(direction=ROW, padding=5))
        b_2g.add(
            toga.Label(
                "G",
                style=Pack(padding=(0,10), color="#00ff00")
            )
        )
        s_2g = toga.Slider(
            range=(0,255),
            default=128,
            style= Pack(width=200)
        )
        b_2g.add(s_2g)

        b_2b = toga.Box(style=Pack(direction=ROW, padding=5))
        b_2b.add(
            toga.Label(
                "B",
                style=Pack(padding=(0,10), color="#0000ff")
            )
        )
        s_2b = toga.Slider(
            range=(0,255),
            default=128,
            style= Pack(width=200)
        )
        b_2b.add(s_2b)

        main_box.add(b_2r)
        main_box.add(b_2g)
        main_box.add(b_2b)

        self.sliders2 = [s_2r, s_2g, s_2b]

        # Send button
        self.sen_btn = toga.Button("Send", style=Pack(padding=10), on_press=self.send)
        main_box.add(self.sen_btn)

        # DISPLAY
        self.main_window = toga.MainWindow(title=self.formal_name, size=(455,465))
        self.main_window.content = main_box
        self.main_window.show()
    
    def send(self,caller):
        esp_id = self.esp_ids_real[self.esp_ids.index(self.esp_id_select.value)]
        mode = self.mode_ids[self.modes.index(self.mode_select.value)]
        spd = 101 - int(self.speed_slider.value)
        wave = int(self.wave_num_input.value)
        inte = int(self.intensity_slider.value)
        hsv = self.hsv_mode_ids[self.hsv_modes.index(self.hsv_mode_select.value)]

        def getSliderVal(x):
            return int(x.value)
        c1 = list(map(getSliderVal, self.sliders1))
        c2 = list(map(getSliderVal, self.sliders2))
        post(esp_id,mode,spd,wave,inte,hsv,c1,c2)

    def main_loop(self):
        return super().main_loop()


def RGB_to_hex(r,g,b):
    r = hex(int(r)).split("x")[-1]
    g = hex(int(g)).split("x")[-1]
    b = hex(int(b)).split("x")[-1]

    if(len(r)==1): r="0"+r
    if(len(g)==1): g="0"+g
    if(len(b)==1): b="0"+b
    return f"#{r}{g}{b}"

# class ColorPicker (toga.Box):
#     def __init__(self, label="Color picker"):
#         super().__init__(style=Pack(direction=ROW, flex=2))
#         # SLIDERS WITH LABELS
#         self.labels = ["R", "G", "B"]
#         self.label_colors = ["#ff0000","#00ff00","#0000ff"]
#         self.slider_boxes = []
#         self.sliders = []

#         for i in range(3):
#             self.slider_boxes.append(
#                 toga.Box(style=Pack(direction=ROW, padding=0))
#             )
#             self.slider_boxes[i].add(
#                 toga.Label(
#                     self.labels[i],
#                     style=Pack(padding=0, color=self.label_colors[i])
#                 )
#             )
#             self.sliders.append(
#                 toga.Slider(
#                     range=(0,255),
#                     on_change=self.updateCanvas,
#                     default=128
#                 )
#             )
#             self.slider_boxes[i].add(
#                 self.sliders[i]
#             )
        
#         self.sliders_box = toga.Box(style=Pack(direction=COLUMN, padding=2))
#         for i in range(3):
#             self.sliders_box.add(self.slider_boxes[i])

#         canv_div = toga.Box(style=Pack(flex=1,direction=COLUMN, padding=2, alignment="right"))
#         # self.canv = toga.Canvas(style=Pack(flex=1, width=80, height=80, padding=2))
#         canv_div.add(toga.Label(
#                     label,
#                     style=Pack(padding=1)
#                 ))
#         # canv_div.add(self.canv)

#         self.add(canv_div)
#         self.add(self.sliders_box)

#         #self.updateCanvas(self)
    
#     def updateCanvas(self, caller):
#         print("Updating color picker canvas", self, caller)
#         try:
#             c = self.getColor()
#             with self.canv.fill(c) as fill:
#                 fill.rect(0, 0, 100, 100)
#         except:
#             pass
    
#     def getColor(self):
#         return RGB_to_hex(
#                 (self.sliders[0].value),
#                 (self.sliders[1].value),
#                 (self.sliders[2].value)
#             )

def main():
    return LED()