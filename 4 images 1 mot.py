import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Données du jeu (chemins des images et mots correspondants)
questions = [
    {"images": ["img1.jpg", "img2.jpg", "img3.jpg", "img4.jpg"], "mot": "soleil"},
    {"images": ["img5.jpg", "img6.jpg", "img7.jpg", "img8.jpg"], "mot": "plage"},
]


class GameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("4 Images 1 Mot")
        self.index = 0

        self.frame = tk.Frame(root)
        self.frame.pack()

        self.image_labels = []
        for i in range(4):
            label = tk.Label(self.frame)
            label.grid(row=i // 2, column=i % 2, padx=5, pady=5)
            self.image_labels.append(label)

        self.entry = tk.Entry(root, font=("Arial", 14))
        self.entry.pack(pady=10)

        self.button = tk.Button(root, text="Valider", command=self.check_answer)
        self.button.pack()

        self.load_question()

    def load_question(self):
        question = questions[self.index]
        for i, img_path in enumerate(question["images"]):
            image = Image.open(img_path).resize((100, 100))
            photo = ImageTk.PhotoImage(image)
            self.image_labels[i].config(image=photo)
            self.image_labels[i].image = photo

    def check_answer(self):
        answer = self.entry.get().strip().lower()
        if answer == questions[self.index]["mot"]:
            messagebox.showinfo("Bravo!", "Bonne réponse!")
            self.index += 1
            if self.index < len(questions):
                self.load_question()
                self.entry.delete(0, tk.END)
            else:
                messagebox.showinfo("Félicitations!", "Vous avez terminé le jeu!")
                self.root.quit()
        else:
            messagebox.showerror("Erreur", "Mauvaise réponse, essayez encore!")


if __name__ == "__main__":
    root = tk.Tk()
    app = GameApp(root)
    root.mainloop()
