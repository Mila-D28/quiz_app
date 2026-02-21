import tkinter as tk
from tkinter import messagebox
import json

class QuizApp:
    """Classe principale pour l'application de quiz"""
    def __init__(self, root):
        """Initialise l'application de quiz"""
        self.root = root
        self.root.title("Application de Quiz Python")
        self.root.geometry("600x500")
        self.root.configure(bg="#2C3E50")
        # Variables pour le suivi du quiz
        self.score = 0
        self.question_actuelle = 0
        self.total_questions = 0
        self.reponses_correctes = 0
        self.reponses_incorrectes = 0
        self.questions_data = []
        self.reponse_selectionnee = tk.StringVar()
        # Charger les données du quiz
        self.charger_questions()
        # Créer l'interface utilisateur
        self.creer_interface()
        # Afficher la première question
        self.afficher_question()
    def charger_questions(self):
        """Charge les questions depuis le fichier JSON"""
        try:
            with open('questions.json', 'r', encoding='utf-8') as fichier:
                data = json.load(fichier)
                self.questions_data = data['questions']
                self.total_questions = len(self.questions_data)
        except FileNotFoundError:
            messagebox.showerror("Erreur", "Fichier questions.json introuvable!")
            self.root.destroy()
        except json.JSONDecodeError:
            messagebox.showerror("Erreur", "Erreur de lecture du fichier JSON!")
            self.root.destroy()
    def creer_interface(self):
        """Crée l'interface graphique du quiz"""
        # Titre de l'application
        titre_frame = tk.Frame(self.root, bg="#34495E", pady=20)
        titre_frame.pack(fill="x")
        
        titre_label = tk.Label(
            titre_frame,
            text="🎯 QUIZ PYTHON 🎯",
            font=("Helvetica", 24, "bold"),
            bg="#34495E",
            fg="white"
        )
        titre_label.pack()
        # Frame pour le numéro de question
        self.info_frame = tk.Frame(self.root, bg="#2C3E50", pady=10)
        self.info_frame.pack()
        
        self.question_num_label = tk.Label(
            self.info_frame,
            text=f"Question 1/{self.total_questions}",
            font=("Arial", 12),
            bg="#2C3E50",
            fg="#ECF0F1"
        )
        self.question_num_label.pack()
        # Frame pour la question
        self.question_frame = tk.Frame(self.root, bg="#2C3E50", pady=20, padx=30)
        self.question_frame.pack(fill="both", expand=True)
        self.question_label = tk.Label(
            self.question_frame,
            text="",
            font=("Arial", 14, "bold"),
            bg="#2C3E50",
            fg="white",
            wraplength=500,
            justify="center"
        )
        self.question_label.pack(pady=20)
        # Frame pour les options de réponse
        self.options_frame = tk.Frame(self.question_frame, bg="#2C3E50")
        self.options_frame.pack(pady=10)
        self.option_buttons = []
        # Frame pour les boutons de navigation
        self.navigation_frame = tk.Frame(self.root, bg="#2C3E50", pady=20)
        self.navigation_frame.pack()
        
        self.bouton_precedent = tk.Button(
            self.navigation_frame,
            text="◀ Précédent",
            font=("Arial", 12),
            bg="#95A5A6",
            fg="white",
            width=12,
            height=2,
            command=self.question_precedente,
            state="disabled"
        )
        self.bouton_precedent.pack(side="left", padx=10)
        
        self.bouton_suivant = tk.Button(
            self.navigation_frame,
            text="Suivant ▶",
            font=("Arial", 12),
            bg="#3498DB",
            fg="white",
            width=12,
            height=2,
            command=self.question_suivante
        )
        self.bouton_suivant.pack(side="left", padx=10)
        # Frame pour le score
        self.score_frame = tk.Frame(self.root, bg="#34495E", pady=10)
        self.score_frame.pack(fill="x")
        self.score_label = tk.Label(
            self.score_frame,
            text=f"Score: {self.score}/{self.total_questions}",
            font=("Arial", 12, "bold"),
            bg="#34495E",
            fg="#F39C12"
        )
        self.score_label.pack()
    def afficher_question(self):
        """Affiche la question actuelle et ses options"""
        # Nettoyer les anciens boutons
        for button in self.option_buttons:
            button.destroy()
        self.option_buttons = []
        # Réinitialiser la sélection
        self.reponse_selectionnee.set("")
        # Récupérer la question actuelle
        question_data = self.questions_data[self.question_actuelle]
        # Mettre à jour le numéro de question
        self.question_num_label.config(
            text=f"Question {self.question_actuelle + 1}/{self.total_questions}"
        )
        # Afficher la question
        self.question_label.config(text=question_data['question'])
        # Créer les boutons radio pour les options
        for option in question_data['options']:
            radio_button = tk.Radiobutton(
                self.options_frame,
                text=option,
                variable=self.reponse_selectionnee,
                value=option,
                font=("Arial", 11),
                bg="#2C3E50",
                fg="white",
                selectcolor="#34495E",
                activebackground="#2C3E50",
                activeforeground="white",
                anchor="w",
                width=40
            )
            radio_button.pack(pady=5, anchor="w")
            self.option_buttons.append(radio_button)
        # Gérer l'état des boutons de navigation
        if self.question_actuelle == 0:
            self.bouton_precedent.config(state="disabled")
        else:
            self.bouton_precedent.config(state="normal")
        
        if self.question_actuelle == self.total_questions - 1:
            self.bouton_suivant.config(text="Terminer ✓", bg="#27AE60")
        else:
            self.bouton_suivant.config(text="Suivant ▶", bg="#3498DB")
    def verifier_reponse(self):
        """Vérifie si la réponse sélectionnée est correcte"""
        reponse_utilisateur = self.reponse_selectionnee.get()
        
        if not reponse_utilisateur:
            messagebox.showwarning("Attention", "Veuillez sélectionner une réponse!")
            return False
        
        reponse_correcte = self.questions_data[self.question_actuelle]['answer']
        
        if reponse_utilisateur == reponse_correcte:
            self.score += 1
            self.reponses_correctes += 1
        else:
            self.reponses_incorrectes += 1
        
        # Mettre à jour l'affichage du score
        self.score_label.config(text=f"Score: {self.score}/{self.total_questions}")
        
        return True
    def question_suivante(self):
        """Passe à la question suivante"""
        # Vérifier la réponse
        if not self.verifier_reponse():
            return
        
        # Passer à la question suivante ou terminer le quiz
        if self.question_actuelle < self.total_questions - 1:
            self.question_actuelle += 1
            self.afficher_question()
        else:
            self.afficher_resultats()
    def question_precedente(self):
        """Retourne à la question précédente"""
        if self.question_actuelle > 0:
            self.question_actuelle -= 1
            self.afficher_question()
    def afficher_resultats(self):
        """Affiche les résultats finaux du quiz"""
        # Calculer le pourcentage
        pourcentage = (self.score / self.total_questions) * 100
        # Déterminer le message selon le score
        if pourcentage >= 80:
            message_titre = "🏆 Excellent !"
            message_evaluation = "Vous maîtrisez très bien Python !"
            couleur_bg = "#27AE60"
        elif pourcentage >= 60:
            message_titre = "👍 Bien joué !"
            message_evaluation = "Vous avez de bonnes bases en Python !"
            couleur_bg = "#3498DB"
        elif pourcentage >= 40:
            message_titre = "📚 Pas mal !"
            message_evaluation = "Continuez à pratiquer !"
            couleur_bg = "#F39C12"
        else:
            message_titre = "💪 Courage !"
            message_evaluation = "Révisez les bases de Python !"
            couleur_bg = "#E74C3C"
        # Créer une nouvelle fenêtre pour les résultats
        resultat_window = tk.Toplevel(self.root)
        resultat_window.title("Résultats du Quiz")
        resultat_window.geometry("500x400")
        resultat_window.configure(bg=couleur_bg)
        # Titre
        tk.Label(
            resultat_window,
            text=message_titre,
            font=("Helvetica", 24, "bold"),
            bg=couleur_bg,
            fg="white"
        ).pack(pady=20)
        # Score
        tk.Label(
            resultat_window,
            text=f"Score Final: {self.score}/{self.total_questions}",
            font=("Arial", 20, "bold"),
            bg=couleur_bg,
            fg="white"
        ).pack(pady=10)
        # Pourcentage
        tk.Label(
            resultat_window,
            text=f"Pourcentage: {pourcentage:.1f}%",
            font=("Arial", 16),
            bg=couleur_bg,
            fg="white"
        ).pack(pady=10)
        # Détails
        details_frame = tk.Frame(resultat_window, bg="white", padx=20, pady=20)
        details_frame.pack(pady=20)
        tk.Label(
            details_frame,
            text=f"✓ Réponses correctes: {self.reponses_correctes}",
            font=("Arial", 14),
            fg="#27AE60",
            bg="white"
        ).pack()
        tk.Label(
            details_frame,
            text=f"✗ Réponses incorrectes: {self.reponses_incorrectes}",
            font=("Arial", 14),
            fg="#E74C3C",
            bg="white"
        ).pack()
        # Évaluation
        tk.Label(
            resultat_window,
            text=message_evaluation,
            font=("Arial", 14, "italic"),
            bg=couleur_bg,
            fg="white"
        ).pack(pady=10)
        # Boutons
        boutons_frame = tk.Frame(resultat_window, bg=couleur_bg)
        boutons_frame.pack(pady=20)
        
        tk.Button(
            boutons_frame,
            text="Recommencer",
            font=("Arial", 12, "bold"),
            bg="white",
            fg=couleur_bg,
            width=15,
            height=2,
            command=lambda: self.recommencer_quiz(resultat_window)
        ).pack(side="left", padx=10)
        
        tk.Button(
            boutons_frame,
            text="Quitter",
            font=("Arial", 12, "bold"),
            bg="#34495E",
            fg="white",
            width=15,
            height=2,
            command=self.root.destroy
        ).pack(side="left", padx=10)
    
    def recommencer_quiz(self, resultat_window):
        """Recommence le quiz depuis le début"""
        resultat_window.destroy()
        self.score = 0
        self.question_actuelle = 0
        self.reponses_correctes = 0
        self.reponses_incorrectes = 0
        self.score_label.config(text=f"Score: {self.score}/{self.total_questions}")
        self.afficher_question()

def main():
    """Fonction principale pour lancer l'application"""
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()