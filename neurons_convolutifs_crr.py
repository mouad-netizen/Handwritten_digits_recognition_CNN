import tkinter as tk
from PIL import Image, ImageTk
from keras.models import load_model
import numpy as np
import PIL.Image
model = load_model('neurons_convolutifs.h5')

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.canvas_width = 300
        self.canvas_height = 300
        self.geometry('1120x820')
        self.configure(background='white')
        self.title("Reconnaissance des chiffres")
        self.resizable(0,0)

        self.im = PIL.Image.open('./meta/image-removebg-preview.png')
        self.im = self.im.resize((300,283), PIL.Image.ANTIALIAS)
        self.wp_img = ImageTk.PhotoImage(self.im)
        self.panel4 = tk.Label(self, image=self.wp_img,bg = 'white')
        self.panel4.pack()
        self.panel4.place(x=20, y=20)

        self.label = tk.Label(self, text="Resultats", font=("Helvetica", 24),fg = 'black',bg='yellow')
        self.label.place(x=1120/2-35,y=470)


        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height, bg='grey')
        self.canvas.place(x=1120/2-150,y=150)

        self.label = tk.Label(self, text="Les réseaux de neurons convolutifs", font=("Helvetica", 24),fg = 'black',bg='yellow')
        self.label.pack()
        

        self.canvas.bind("<B1-Motion>", self.draw)

       

        self.panel5 = tk.Button(self,text = 'Reconnâitre',command = self.predict_digit,width = 15,borderwidth=0,bg = 'midnightblue',fg = 'white',font = ('times',18,'bold'))
        self.panel5.place(x=60, y=305)

        self.panel6 = tk.Button(self,text = 'Sipprimer',width = 15,borderwidth=0,command = self.clear_canvas,bg ='yellow',fg = 'black',font = ('times',18,'bold'))
        self.panel6.place(x=60, y=355)

       

        self.digit_label = tk.Label(self, text="", font=("Helvetica", 48))
        self.digit_label.place(x=1120/2,y=520)

        self.image_data = np.zeros((self.canvas_height, self.canvas_width), dtype=np.uint8)

    def draw(self, event):
        x = event.x
        y = event.y
        r = 8
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill='black')
        self.image_data[y - r:y + r, x - r:x + r] = 255

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image_data = np.zeros((self.canvas_height, self.canvas_width), dtype=np.uint8)

    def predict_digit(self):
        img = Image.fromarray(self.image_data)
        img = img.resize((28, 28))
        img = img.convert('L')
        img = np.array(img)
        img = img.reshape(1, 28, 28, 1)
        img = img / 255.0
        prediction = model.predict(img)
        digit = np.argmax(prediction)
        self.digit_label.config(text=str(digit))

app = App()
app.mainloop()
