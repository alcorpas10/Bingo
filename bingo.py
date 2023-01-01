import random
import tkinter as tk
import pyttsx3

# Inicializa la síntesis de voz
engine = pyttsx3.init()
engine.setProperty('rate', 125)

engine.say("Comenzamos, primer número")
engine.runAndWait()

# Inicializa la GUI
root = tk.Tk()
root.title("Bingo")
root.geometry("800x800")

# Crea una etiqueta para mostrar el número actual
number_label = tk.Label(root, text="")
number_label.config(font=("Arial", 100))
number_label.grid(row=0, column=0, columnspan=5)

# Crea una lista de etiquetas para mostrar los últimos 5 números cantados
history_labels = []
for i in range(5):
    label = tk.Label(root, text="")
    label.config(font=("Arial", 50))
    label.grid(row=0, column=5+i)

    history_labels.append(label)

# Inicializa el flag de pausa
paused = tk.BooleanVar()
paused.set(False)

# Crea la lista de números del 1 al 80
numbers = list(range(1, 81))
random.shuffle(numbers)

# Función que se ejecuta cuando se pulsa un botón
def mark_number(number):
    # Cambia el color de fondo a rojo
    buttons[(number-1)//10][(number-1)%10].config(bg="red")

    # Actualiza la lista de números cantados
    history_labels.pop(0)

    if number < 10:
        numero = tk.Label(root, text=" "+str(number)+" ")
    else:
        numero = tk.Label(root, text=str(number))
    numero.config(font=("Arial", 25))
    history_labels.append(numero)
    for i in range(5):
        history_labels[i].grid(row=0, column=5+i)

    # Refresca la GUI
    root.update()

    # Canta el número con voz humana
    engine.say(str(number))    
    engine.runAndWait()

# Función que se ejecuta cada 3 segundos
def next_number():
    if not paused.get() and len(numbers) > 0:
        # Obtiene el siguiente número de la lista
        number = numbers.pop()

        # Actualiza la etiqueta con el número actual
        number_label.config(text=str(number))

        # Marca el número
        mark_number(number)
    
    # Programa la siguiente ejecución de la función
    root.after(2500, next_number)

# Función que se ejecuta al pulsar el botón de pausa
def pause_game():
    paused.set(not paused.get())

    if not paused.get():
        root.update()

        engine.say("Continuamos para bingo")
    else:
        engine.say("Partida pausada")
    engine.runAndWait()

# Función que se ejecuta al pulsar el botón de reiniciar
def restart_game():
    global numbers

    engine.say("Reiniciando")
    engine.say("Comenzamos, primer número")
    engine.runAndWait()

    # Reinicia la lista de números
    numbers = list(range(1, 81))
    random.shuffle(numbers)

    # Reinicia la etiqueta del número actual
    number_label.config(text="")

    paused.set(False)

    # Reinicia la lista de números cantados
    for i in range(5):
        history_labels[i].config(text="   ")

    # Reinicia los botones
    for i in range(8):
        for j in range(10):
            buttons[i][j].config(bg="SystemButtonFace")

    # Refresca la GUI
    root.update()

# Crea una matriz de botones para marcar los números que han salido
buttons = []
for i in range(8):
    row = []
    for j in range(10):
        if i == 0 and j < 9:
            button = tk.Button(root, text=" "+str((i * 10) + j + 1)+" ", command=lambda i=i, j=j: mark_number((i * 10) + j + 1))
        else:
            button = tk.Button(root, text=str((i * 10) + j + 1), command=lambda i=i, j=j: mark_number((i * 10) + j + 1))
        button.config(font=("Arial", 25))
        button.grid(row=i+1, column=j)
        row.append(button)
    buttons.append(row)

# Crea una lista con los últimos 5 números que han salido
last_numbers = []
for i in range(5):
    label = tk.Label(root, text="")
    label.config(font=("Arial", 50))
    label.grid(row=9, column=i)
    last_numbers.append(label)

# Crea los botones para pausar y reiniciar el juego
pause_button = tk.Button(root, text=" Pausar ", command=pause_game)
pause_button.config(font=("Arial", 25))
pause_button.grid(row=1, column=11)
restart_button = tk.Button(root, text="Reiniciar", command=restart_game)
restart_button.config(font=("Arial", 25))
restart_button.grid(row=2, column=11)

# Inicia el proceso automático
root.after(2500, next_number)

root.mainloop()
