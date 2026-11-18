import random
import tkinter as tk
from tkinter import messagebox

# ---------------- SETTINGS ----------------
TOTAL_SECONDS = 60 * 60   # 1 hour
TIP_PENALTY = 60          # a tip costs 1 minute

# ---------------- QUESTIONS ----------------
# Format: (subject, question, [4 options], index of correct option, tip or None)
# Tips only for math. A tip helps, but never gives the answer.
QUESTIONS = [
    # ----- MATTE -----
    ("Matte", "Hva er 8 × 7?", ["54", "56", "63", "49"], 1,
     "Du kan dele opp: 8 × 7 = 8 × 5 + 8 × 2. Regn ut hver del, og legg sammen."),
    ("Matte", "Hva er 144 ÷ 12?", ["10", "11", "12", "14"], 2,
     "Tenk motsatt: hvilket tall ganget med 12 gir 144? Prøv deg frem med 10 × 12 først."),
    ("Matte", "Hva er 3/4 av 20?", ["12", "15", "16", "5"], 1,
     "Finn først hva 1/4 av 20 er (del på 4). Ta så det tallet 3 ganger."),
    ("Matte", "Et rektangel er 9 cm langt og 4 cm bredt. Hva er arealet?", ["13 cm²", "26 cm²", "36 cm²", "40 cm²"], 2,
     "Areal av rektangel = lengde × bredde. Pass på at du ikke regner omkretsen."),
    ("Matte", "Hva er 0,5 + 0,25?", ["0,30", "0,75", "0,70", "1,25"], 1,
     "Skriv 0,5 som 0,50. Da kan du legge sammen som vanlige tall: 50 + 25 hundredeler."),
    ("Matte", "Hva er 1000 − 457?", ["543", "553", "643", "447"], 0,
     "Regn i trinn: 1000 − 400, så − 50, så − 7. Eller tell opp fra 457 til 1000."),
    ("Matte", "Hva er omkretsen til et kvadrat med side 6 cm?", ["12 cm", "24 cm", "36 cm", "18 cm"], 1,
     "Omkrets er summen av alle sidene. Hvor mange like sider har et kvadrat?"),
    ("Matte", "Hvilken brøk er lik 1/2?", ["2/3", "3/6", "2/5", "1/4"], 1,
     "Hvis telleren er halvparten av nevneren, er brøken lik 1/2. Sjekk hvert alternativ."),
    ("Matte", "Ola har 250 kr og kjøper noe til 175 kr. Hvor mye har han igjen?", ["65 kr", "75 kr", "85 kr", "125 kr"], 1,
     "Dette er en minus-oppgave. Prøv: 175 + hvor mye = 250? Tell opp til 200 først."),
    ("Matte", "Hva er 15 % av 200?", ["15", "20", "30", "40"], 2,
     "Finn først 10 % (del på 10). Så 5 % er halvparten av det. Legg sammen."),
    # ----- NORSK -----
    ("Norsk", "Hvilket ord er et substantiv?", ["løpe", "stor", "bord", "raskt"], 2, None),
    ("Norsk", "Hvilket ord er et verb?", ["hund", "synge", "grønn", "under"], 1, None),
    ("Norsk", "Hva er flertall av «bok»?", ["boker", "bøker", "boks", "bøk"], 1, None),
    ("Norsk", "Hvilket ord er et adjektiv?", ["vakker", "sykkel", "spise", "i"], 0, None),
    ("Norsk", "Hvilken setning er riktig skrevet?", ["jeg liker is.", "Jeg liker is.", "jeg Liker Is", "Jeg liker is"], 1, None),
    ("Norsk", "Hva er det motsatte av «varm»?", ["lun", "kald", "het", "myk"], 1, None),
    ("Norsk", "Hvilket ord er skrevet riktig?", ["hvorfor", "forhvor", "hvofor", "hvorfør"], 0, None),
    ("Norsk", "Hva er preteritum (fortid) av «å gå»?", ["gikk", "gådde", "gått", "går"], 0, None),
    ("Norsk", "Hvilket tegn setter vi på slutten av et spørsmål?", [".", "!", "?", ","], 2, None),
    ("Norsk", "Hvilket ord rimer på «hus»?", ["bil", "mus", "tre", "bok"], 1, None),
    # ----- NATURFAG -----
    ("Naturfag", "Hvilken planet er nærmest sola?", ["Venus", "Jorden", "Merkur", "Mars"], 2, None),
    ("Naturfag", "Hva trenger planter for å lage mat (fotosyntese)?", ["Sollys", "Bare mørke", "Sukker", "Salt"], 0, None),
    ("Naturfag", "Hvilken gass puster vi inn for å leve?", ["Karbondioksid", "Nitrogen", "Oksygen", "Helium"], 2, None),
    ("Naturfag", "Ved hvilken temperatur fryser vann til is?", ["0 °C", "10 °C", "100 °C", "−10 °C"], 0, None),
    ("Naturfag", "Hvilket dyr er et pattedyr?", ["Hai", "Frosk", "Hval", "Ørret"], 2, None),
    ("Naturfag", "Hva kalles det når vann blir til damp?", ["Kondensering", "Fordamping", "Frysing", "Smelting"], 1, None),
    ("Naturfag", "Hvilken del av planten suger opp vann fra jorda?", ["Blad", "Blomst", "Rot", "Frukt"], 2, None),
    ("Naturfag", "Hvor mange ben har en edderkopp?", ["6", "8", "10", "4"], 1, None),
    ("Naturfag", "Hva kalles stedet der vi finner mange fossiler og bergarter?", ["Jordlag", "Skyer", "Hav", "Atmosfære"], 0, None),
    ("Naturfag", "Hva lager lyd når den vibrerer?", ["Ingenting", "Et trommeskinn", "Et speil", "Et vindu uten luft"], 1, None),
]

COLORS = {
    "Matte": "#3b82f6",
    "Norsk": "#ef4444",
    "Naturfag": "#22c55e",
}


class QuizGame:
    def __init__(self, root):
        self.root = root
        root.title("Quiz-spillet – Matte, Norsk og Naturfag")
        root.geometry("820x600")
        root.configure(bg="#f5f5f5")

        self.questions = QUESTIONS[:]
        random.shuffle(self.questions)
        self.index = 0
        self.score = 0
        self.mistakes = 0
        self.tips_used = 0
        self.time_left = TOTAL_SECONDS
        self.running = False
        self.answered_wrong = set()

        self.build_start_screen()

    # ---------- Screens ----------
    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    def build_start_screen(self):
        self.clear()
        tk.Label(self.root, text="🎓 Quiz-spillet", font=("Arial", 36, "bold"),
                 bg="#f5f5f5").pack(pady=(70, 10))
        tk.Label(self.root,
                 text="Svar på spørsmål i matte, norsk og naturfag.\n"
                      "Du har 1 time. Klikk på riktig svar for å gå videre.\n\n"
                      "I matte kan du få et tips, men det koster 1 minutt!",
                 font=("Arial", 16), bg="#f5f5f5", justify="center").pack(pady=20)
        tk.Button(self.root, text="Start spillet", font=("Arial", 22, "bold"),
                  bg="#22c55e", fg="white", padx=30, pady=10,
                  command=self.start_game).pack(pady=30)

    def start_game(self):
        self.clear()
        self.running = True

        top = tk.Frame(self.root, bg="#f5f5f5")
        top.pack(fill="x", padx=20, pady=10)
        self.progress_label = tk.Label(top, font=("Arial", 14), bg="#f5f5f5")
        self.progress_label.pack(side="left")
        self.timer_label = tk.Label(top, font=("Arial", 20, "bold"), bg="#f5f5f5")
        self.timer_label.pack(side="right")

        self.subject_label = tk.Label(self.root, font=("Arial", 16, "bold"),
                                      fg="white", pady=6)
        self.subject_label.pack(fill="x", padx=20)

        self.question_label = tk.Label(self.root, font=("Arial", 22), bg="#f5f5f5",
                                       wraplength=740, justify="center")
        self.question_label.pack(pady=25)

        self.btn_frame = tk.Frame(self.root, bg="#f5f5f5")
        self.btn_frame.pack()
        self.option_buttons = []
        for i in range(4):
            b = tk.Button(self.btn_frame, font=("Arial", 18), width=28, pady=8,
                          command=lambda i=i: self.check_answer(i))
            b.grid(row=i // 2, column=i % 2, padx=10, pady=10)
            self.option_buttons.append(b)

        self.feedback_label = tk.Label(self.root, font=("Arial", 15), bg="#f5f5f5")
        self.feedback_label.pack(pady=5)

        self.tip_button = tk.Button(self.root, text="💡 Få et tips (−1 minutt)",
                                    font=("Arial", 14), bg="#facc15",
                                    command=self.show_tip)
        self.tip_button.pack(pady=5)
        self.tip_label = tk.Label(self.root, font=("Arial", 14, "italic"),
                                  bg="#f5f5f5", fg="#92400e", wraplength=740)
        self.tip_label.pack(pady=5)

        self.show_question()
        self.tick()

    # ---------- Game logic ----------
    def show_question(self):
        subject, q, options, correct, tip = self.questions[self.index]
        self.answered_wrong = set()
        self.progress_label.config(
            text=f"Spørsmål {self.index + 1} av {len(self.questions)}   |   Poeng: {self.score}")
        self.subject_label.config(text=subject, bg=COLORS[subject])
        self.question_label.config(text=q)
        self.feedback_label.config(text="")
        self.tip_label.config(text="")

        # Shuffle the options so the right answer is not always in the same place
        order = list(range(4))
        random.shuffle(order)
        self.current_order = order
        self.current_correct = order.index(correct)
        for btn, original in zip(self.option_buttons, order):
            btn.config(text=options[original], state="normal", bg="#e5e7eb")

        # Tip button only for math
        if tip:
            self.tip_button.config(state="normal")
            self.tip_button.pack(pady=5)
        else:
            self.tip_button.pack_forget()

    def check_answer(self, i):
        if i == self.current_correct:
            self.score += 1
            self.option_buttons[i].config(bg="#86efac")
            self.feedback_label.config(text="✅ Riktig!", fg="#15803d")
            for b in self.option_buttons:
                b.config(state="disabled")
            self.root.after(700, self.next_question)
        else:
            self.mistakes += 1
            self.option_buttons[i].config(bg="#fca5a5", state="disabled")
            self.feedback_label.config(text="❌ Feil, prøv igjen!", fg="#b91c1c")

    def next_question(self):
        if not self.running:
            return
        self.index += 1
        if self.index >= len(self.questions):
            self.end_game(finished=True)
        else:
            self.show_question()

    def show_tip(self):
        tip = self.questions[self.index][4]
        if not tip:
            return
        if self.time_left <= TIP_PENALTY:
            messagebox.showinfo("For lite tid", "Du har ikke nok tid igjen til et tips.")
            return
        if messagebox.askyesno("Vil du ha et tips?",
                               "Et tips koster 1 minutt av tiden din. Vil du ha det?"):
            self.time_left -= TIP_PENALTY
            self.tips_used += 1
            self.tip_label.config(text="💡 " + tip)
            self.update_timer_label()

    # ---------- Timer ----------
    def update_timer_label(self):
        m, s = divmod(max(self.time_left, 0), 60)
        color = "#dc2626" if self.time_left <= 300 else "black"
        self.timer_label.config(text=f"⏱ {m:02d}:{s:02d}", fg=color)

    def tick(self):
        if not self.running:
            return
        self.update_timer_label()
        if self.time_left <= 0:
            self.end_game(finished=False)
            return
        self.time_left -= 1
        self.root.after(1000, self.tick)

    # ---------- End ----------
    def end_game(self, finished):
        self.running = False
        self.clear()
        title = "🎉 Bra jobba! Du er ferdig!" if finished else "⏰ Tiden er ute!"
        used = TOTAL_SECONDS - max(self.time_left, 0)
        tk.Label(self.root, text=title, font=("Arial", 32, "bold"),
                 bg="#f5f5f5").pack(pady=(80, 20))
        tk.Label(self.root,
                 text=f"Riktige svar: {self.score} av {len(self.questions)}\n"
                      f"Feil forsøk: {self.mistakes}\n"
                      f"Tips brukt: {self.tips_used}\n"
                      f"Tid brukt: {used // 60} min {used % 60} sek",
                 font=("Arial", 20), bg="#f5f5f5", justify="center").pack(pady=20)
        tk.Button(self.root, text="Spill igjen", font=("Arial", 20, "bold"),
                  bg="#3b82f6", fg="white", padx=20, pady=8,
                  command=self.restart).pack(pady=20)

    def restart(self):
        self.questions = QUESTIONS[:]
        random.shuffle(self.questions)
        self.index = self.score = self.mistakes = self.tips_used = 0
        self.time_left = TOTAL_SECONDS
        self.start_game()


if __name__ == "__main__":
    root = tk.Tk()
    QuizGame(root)
    root.mainloop()
