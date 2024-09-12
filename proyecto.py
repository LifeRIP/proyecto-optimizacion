import tkinter as tk
from tkinter import scrolledtext

class ConcertApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Optimización de Concierto")

        self.label_input = tk.Label(root, text="Ingrese N, M y las ciudades (Nombre X Y):")
        self.label_input.grid(row=0, column=0, padx=5, pady=5)
        self.text_input = scrolledtext.ScrolledText(root, width=30, height=10)
        self.text_input.grid(row=0, column=1, padx=5, pady=5)

        self.button_generate = tk.Button(root, text="Generar Código MiniZinc", command=self.generate_minizinc)
        self.button_generate.grid(row=1, column=0, columnspan=2, pady=10)

        self.label_output = tk.Label(root, text="Código MiniZinc:")
        self.label_output.grid(row=2, column=0, padx=5, pady=5)
        self.text_output = scrolledtext.ScrolledText(root, width=30, height=10)
        self.text_output.grid(row=2, column=1, padx=5, pady=5)

    def generate_minizinc(self):
        input_lines = self.text_input.get("1.0", tk.END).strip().split('\n')
        N = int(input_lines[0])
        M = int(input_lines[1])
        cities = input_lines[2:]
        if M != len(cities):
            self.text_output.delete("1.0", tk.END)
            self.text_output.insert(tk.END, "El número de ciudades no coincide con M")
            return
        minizinc_code = self.create_minizinc_code(N, M, cities)
        self.text_output.delete("1.0", tk.END)
        self.text_output.insert(tk.END, minizinc_code)

    def create_minizinc_code(self, N, M, cities):
      code = f"int: N = {N};\n"
      code += f"int: M = {M};\n"
      code += "array[1..M, 1..2] of int: cities = [|\n"
      for i, city in enumerate(cities):
        name, x, y = city.split()
        code += f"  {x}, {y} "
        if i < len(cities) - 1:
          code += "|\n"
      code += "|];\n"
      
      code += """
var 0..N: x;
var 0..N: y;

constraint forall(i in 1..M) (x != cities[i, 1] \/ y != cities[i, 2]);

function var int: dist(var int: x1, var int: y1, int: x2, int: y2) = abs(x1 - x2) + abs(y1 - y2);

array[1..M] of var int: distances = [dist(x, y, cities[i, 1], cities[i, 2]) | i in 1..M];

constraint max(distances) - min(distances) <= 2;

var int: total_distance = sum(distances);

solve minimize total_distance;
      """
      return code

if __name__ == "__main__":
    root = tk.Tk()
    app = ConcertApp(root)
    root.mainloop()
