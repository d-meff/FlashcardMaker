import tkinter
from tkinter import *
import sqlite3
from sqlite3 import *
import random
from random import randint
import csv


conn = sqlite3.connect('my_decks.db')
c = conn.cursor()

# Menu Window
class MainWin:
    def __init__(self, master):
        self.master = master
        self.master.title("Make your own flashcard decks!")
        self.master.geometry("600x500")
        self.master.minsize(600, 500)
        self.master.maxsize(600, 500)

        self.testLabel = Label(master, text="Welcome to the Flash Card Maker!")
        self.testLabel.place(x=210, y=10)

        self.createDeckButton = Button(master, text="Create a Deck", command=self.go_to_create_deck, background="light blue")
        self.createDeckButton.place(x=259, y=40)

        self.editDeckButton = Button(master, text="Edit a Deck", command=self.go_to_edit_deck, background="yellow")
        self.editDeckButton.place(x=265, y=70)

        self.viewDeckButton = Button(master, text="View Decks", command=self.go_to_view_deck, background="light green")
        self.viewDeckButton.place(x=265, y=100)

    def go_to_edit_deck(self):
        self.testLabel.destroy()
        self.editDeckButton.destroy()
        self.viewDeckButton.destroy()
        self.createDeckButton.destroy()

        self.editDeckNav = EditDeck(root)
    
    def go_to_view_deck(self):
        self.testLabel.destroy()
        self.editDeckButton.destroy()
        self.viewDeckButton.destroy()
        self.createDeckButton.destroy()

        self.viewDeckNav = ViewDeckWin(root)
    
    def go_to_create_deck(self):
        self.testLabel.destroy()
        self.editDeckButton.destroy()
        self.viewDeckButton.destroy()
        self.createDeckButton.destroy()

        self.createDeckNav = CreateDeck(root)

# Editing Window
class EditDeck:
    def __init__(self, master):
        self.master = master
        self.master.title("Make your own flashcard decks!")
        self.master.geometry("600x500")
        self.master.minsize(600, 500)
        self.master.maxsize(600, 500)

        self.tableNameLabel = Label(master, text="Deck Name:")
        self.tableNameLabel.place(x=170, y=55)

        self.tableNameEntry = Entry(master, width=40)
        self.tableNameEntry.place(x=250, y=55)

        self.editLabel = Label(master, text="Add flashcards to deck:")
        self.editLabel.place(x=310, y=20)

        self.backButton = Button(master, text="Back to Main Menu", command=self.back_to_menu, background="yellow")
        self.backButton.place(x=10, y=10)

        self.questionEntryLabel = Label(master, text="Q:")
        self.questionEntryLabel.place(x=200, y=82)

        self.questionEntry = Entry(master, width=40)
        self.questionEntry.place(x=250, y=85)

        self.answerEntryLabel = Label(master, text="A:")
        self.answerEntryLabel.place(x=200, y=110)

        self.answerEntry = Entry(master, width=40)
        self.answerEntry.place(x=250, y=110)

        self.addButton = Button(master, text="Add to Deck", command=self.insert_card, background="yellow")
        self.addButton.place(x=335, y=145)

        self.dropTableEntry = Entry(master, width=40)
        self.dropTableEntry.place(x=245, y=260)

        self.dropTableLabel = Label(master, text="Deck to delete:")
        self.dropTableLabel.place(x=150, y=260)

        self.deleteDeckButton = Button(master, text="Delete Deck", command=self.delete_deck, background="yellow")
        self.deleteDeckButton.place(x=335, y=295)

        self.deckDeletedLabel = Label(master)
        self.deckDeletedLabel.place(x=280, y=330)

        self.tableNotExistLabel = Label(master)
        self.tableNotExistLabel.place(x=320, y=180)

        self.cardAddedLabel = Label(master)
        self.cardAddedLabel.place(x=320, y=195)

    def back_to_menu(self):
        self.tableNameEntry.destroy()
        self.tableNameLabel.destroy()
        self.backButton.destroy()
        self.editLabel.destroy()
        self.questionEntryLabel.destroy()
        self.questionEntry.destroy()
        self.answerEntryLabel.destroy()
        self.answerEntry.destroy()
        self.addButton.destroy()
        self.dropTableEntry.destroy()
        self.dropTableLabel.destroy()
        self.deleteDeckButton.destroy()
        self.deckDeletedLabel.destroy()
        self.tableNotExistLabel.destroy()
        self.cardAddedLabel.destroy()

        self.mainMenuNav = MainWin(root)
    
    def insert_card(self):
        try:
            self.tableNotExistLabel["text"] = ""
            table_name = self.tableNameEntry.get()

            c.execute(f"""SELECT * FROM {table_name}""")
            grabbing = c.fetchall()

            id_num = 0

            for row in grabbing:
                id_num += 1

            x = f'''{table_name + '_' + str(id_num)}'''
            y = self.questionEntry.get()
            z = self.answerEntry.get()

            c.execute(f"""INSERT INTO {table_name.lower()} VALUES("{x}", "{y}", "{z}")""")

            self.questionEntry.delete(0, END)
            self.answerEntry.delete(0, END)
            conn.commit()

            self.cardAddedLabel["text"] = f'Card added to {table_name}!'

        except:
            self.tableNotExistLabel["text"] = f'Deck {table_name} does not exist.'
            self.cardAddedLabel["text"] = ""
    
    def delete_deck(self):
        table_name = self.dropTableEntry.get()
        try:
            c.execute(f"""SELECT * FROM {table_name}""")
            c.execute(f"""DROP TABLE IF EXISTS {table_name}""")
            conn.commit()

            self.deckDeletedLabel["text"] = f'Deck {table_name} has been deleted!'
        except:
            self.deckDeletedLabel["text"] = f'Deck {table_name} does not exist.'


# Viewing Window
class ViewDeckWin:
    def __init__(self, master):
        self.master = master
        self.master.title("Make your own flashcard decks!")
        self.master.geometry("600x500")
        self.master.minsize(600, 500)
        self.master.maxsize(600, 500)

        self.ViewDeckLabel = Label(master, text="View your decks!")
        self.ViewDeckLabel.place(x=255, y=10)

        self.backButton = Button(master, text="Back to Main Menu", command=self.back_to_menu, background="light green")
        self.backButton.place(x=10, y=10)

        self.tableLoadLabel = Label(master, text="Table to load:")
        self.tableLoadLabel.place(x=160, y=50)

        self.tableLoadEntry = Entry(master, width=40)
        self.tableLoadEntry.place(x=245, y=50)

        self.tableQuestionText = Label(master, wraplength=330)
        self.tableQuestionText.place(x=130, y=220)

        self.loadTableButton = Button(master, text="Load Table", command=self.load_table_questions, background="light green")
        self.loadTableButton.place(x=170, y=110)

        self.loadNextQuestionButton = Button(master, text="Next Question", command=self.load_next_question, background="light green")
        self.loadNextQuestionButton.place(x=320, y=148)

        self.loadNextQuestionButton["state"] = DISABLED

        self.loadPrevQuestion = Button(master, text="Prev Question", command=self.go_to_prevQ, background="light green")
        self.loadPrevQuestion.place(x=210, y=148)

        self.loadPrevQuestion["state"] = DISABLED

        self.rowAnswerLabel = Label(master, wraplength=330)
        self.rowAnswerLabel.place(x=130, y=280) 

        self.showAnswerButton = Button(master, text="Show Answer", command=self.show_answer, background="light green")
        self.showAnswerButton.place(x=370, y=110) 

        self.showAnswerButton["state"] = DISABLED

        self.resetDeckButton = Button(master, text="Reset Deck", command=self.reset_deck, background="light green")
        self.resetDeckButton.place(x=267, y=110)

        self.resetDeckButton["state"] = DISABLED

        self.cardNumberLabel = Label(master, text="Deck Card Count will be shown here", wraplength=85)
        self.cardNumberLabel.place(x=10, y=200)

        self.loadRandomQuestionButton = Button(master, text="Random Question", command=self.load_random_question, background="light green")
        self.loadRandomQuestionButton.place(x=15, y=390)

        self.exportDeckButton = Button(master, text="Export Deck as CSV", command=self.export_deck, background="light green")
        self.exportDeckButton.place(x=15, y=430)

        self.exportedDeckLabel = Label(master)
        self.exportedDeckLabel.place(x=15, y=470)

        self.tableDoesntExistLabel = Label(master)
        self.tableDoesntExistLabel.place(x=245, y=80)

        self.loadRandomQuestionButton["state"] = DISABLED
        self.exportDeckButton["state"] = DISABLED


    def back_to_menu(self):
        self.backButton.destroy()
        self.ViewDeckLabel.destroy()
        self.tableLoadEntry.destroy()
        self.tableLoadLabel.destroy()
        self.tableQuestionText.destroy()
        self.loadNextQuestionButton.destroy()
        self.loadTableButton.destroy()
        self.rowAnswerLabel.destroy()
        self.showAnswerButton.destroy()
        self.resetDeckButton.destroy()
        self.loadPrevQuestion.destroy()
        self.cardNumberLabel.destroy()
        self.loadRandomQuestionButton.destroy()
        self.exportDeckButton.destroy()
        self.exportedDeckLabel.destroy()
        self.tableDoesntExistLabel.destroy()
        
        self.mainMenuNav = MainWin(root)

    def load_table_questions(self):
        global data_rows
        global count_row
        global rows
        global card_val

        table_name = self.tableLoadEntry.get()

        try:
            card_val = 1

            self.rowAnswerLabel["text"] = ""

            rows = []
            count_row = 0

            c.execute(f'''SELECT * FROM {table_name}''')
            data_rows = c.fetchall()

            for row in data_rows:
                rows.append(row)

            self.tableQuestionText["text"] = rows[count_row][1]

            if len(rows) == 1:
                self.loadNextQuestionButton["state"] = DISABLED
            else:
                self.loadNextQuestionButton["state"] = NORMAL

            if card_val == 1:
                self.loadPrevQuestion["state"] = DISABLED
            else:
                self.loadPrevQuestion["state"] = NORMAL

            self.cardNumberLabel["text"] = f'Card Number: {card_val} / {len(data_rows)}'

            self.showAnswerButton["state"] = NORMAL
            self.resetDeckButton["state"] = NORMAL
            self.loadRandomQuestionButton["state"] = NORMAL
            self.exportDeckButton["state"] = NORMAL

            self.tableDoesntExistLabel["text"] = ""

        except:
            self.tableDoesntExistLabel["text"] = f"Deck '{table_name}' does not exist, please reload a valid deck"
            self.loadNextQuestionButton["state"] = DISABLED
            self.resetDeckButton["state"] = DISABLED
            self.loadPrevQuestion["state"] = DISABLED
            self.showAnswerButton["state"] = DISABLED
            self.loadRandomQuestionButton["state"] = DISABLED
            self.exportDeckButton["state"] = DISABLED

    def load_random_question(self):
        global data_rows
        global count_row
        global rows
        global card_val

        count_row = random.randint(0, len(data_rows) - 1)
        card_val = count_row + 1

        self.tableQuestionText["text"] =  rows[count_row][1]
        self.rowAnswerLabel["text"] = ""

        self.cardNumberLabel["text"] = f'Card Number: {card_val} / {len(data_rows)}'

        if card_val == len(data_rows):
            self.loadNextQuestionButton["state"] = DISABLED
        else:
            self.loadNextQuestionButton["state"] = NORMAL

        if card_val == 1:
            self.loadPrevQuestion["state"] = DISABLED
        else:
            self.loadPrevQuestion["state"] = NORMAL

    
    def load_next_question(self):
        global data_rows
        global count_row
        global rows
        global card_val

        count_row += 1

        self.tableQuestionText["text"] =  rows[count_row][1]
        self.rowAnswerLabel["text"] = ""

        if count_row + 1 == len(rows):
            self.loadNextQuestionButton["state"] = DISABLED
        
        if count_row > 0:
            self.loadPrevQuestion["state"] = NORMAL

        card_val += 1
        self.cardNumberLabel["text"] = f'Card Number: {card_val} / {len(data_rows)}'
    
    def show_answer(self):
        global data_rows
        global count_row
        global rows

        self.rowAnswerLabel["text"] = rows[count_row][2]
    
    def reset_deck(self):
        global data_rows
        global count_row
        global rows
        global card_val

        count_row = 0

        self.tableQuestionText["text"] =  rows[count_row][1]
        self.rowAnswerLabel["text"] = ""

        self.loadNextQuestionButton["state"] = NORMAL
        self.loadPrevQuestion["state"] = DISABLED

        if count_row + 1 == len(rows):
            self.loadNextQuestionButton["state"] = DISABLED
        else:
            self.loadNextQuestionButton["state"] = NORMAL
        
        card_val = 1
        self.cardNumberLabel["text"] = f'Card Number: {card_val} / {len(data_rows)}'

    def go_to_prevQ(self):
        global data_rows
        global count_row
        global rows
        global card_val

        count_row -= 1

        self.tableQuestionText["text"] =  rows[count_row][1]
        self.rowAnswerLabel["text"] = ""

        
        if count_row == 0:
            self.loadPrevQuestion["state"] = DISABLED
        
        if count_row + 1 == len(rows):
            self.loadNextQuestionButton["state"] = DISABLED
        else:
            self.loadNextQuestionButton["state"] = NORMAL
        
        card_val -= 1
        self.cardNumberLabel["text"] = f'Card Number: {card_val} / {len(data_rows)}'

    def export_deck(self):
        try:
            table_name = self.tableLoadEntry.get()

            table_rows = []
            c.execute(f"""SELECT * FROM {table_name}""")

            grabbed_rows = c.fetchall()
            for row in grabbed_rows:
                table_rows.append(row)

            with open(f'{table_name}.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(table_rows)

            self.exportedDeckLabel["text"] = f'{table_name}.csv has been created! (or updated)'
        except:
            self.exportedDeckLabel["text"] = "Error creating deck CSV. (Deck probably doesn't exist)"
        


# Creating Window
class CreateDeck:
    def __init__(self, master):
        self.master = master
        self.master.title("Make your own flashcard decks!")
        self.master.geometry("600x500")
        self.master.minsize(600, 500)
        self.master.maxsize(600, 500)
    
        self.backButton = Button(master, text="Back to Main Menu", command=self.back_to_menu, background="light blue")
        self.backButton.place(x=10, y=10)

        self.deckName = Entry(master, width=40)
        self.deckName.place(x=245, y=60)

        self.deckNameLabel = Label(master, text="New Deck Name:")
        self.deckNameLabel.place(x=140, y=60)

        self.createNewDeck = Button(master, text="Create New Deck", command=self.create_the_table, background="light blue")
        self.createNewDeck.place(x=245, y=105)

        self.deckCreatedLabel = Label(master, text="")
        self.deckCreatedLabel.place(x=235, y=150)

        self.seeTablesButton = Button(master, text="See created table names", command=self.see_deck_names, background="light blue")
        self.seeTablesButton.place(x=10, y=150)

        self.seeTableNamesLabel = Label(master, text="", wraplength=150)
        self.seeTableNamesLabel.place(x=245, y=250)

    def create_the_table(self):
        deck_title = self.deckName.get()
        try:
            c.execute(f'''CREATE TABLE IF NOT EXISTS {deck_title.lower()} (deck_name text, question text, answer text)''')
            self.deckCreatedLabel["text"] = f'Deck named {deck_title} created! (or already exists)'
        except:
            self.deckCreatedLabel["text"] = "This deck has already been created" # try will run regardless

        self.deckName.delete(0, END)
        conn.commit()

    def back_to_menu(self):
        self.backButton.destroy()
        self.deckName.destroy()
        self.deckNameLabel.destroy()
        self.createNewDeck.destroy()
        self.deckCreatedLabel.destroy()
        self.seeTablesButton.destroy()
        self.seeTableNamesLabel.destroy()

        self.mainMenuNav = MainWin(root)

    def see_deck_names(self):
        table_names = []
        table_names_cleaned = []

        c.execute("""SELECT name FROM sqlite_master WHERE TYPE = 'table'""")
        grabbed_table_names = c.fetchall()

        for name in grabbed_table_names:
            table_names.append(name)

        for name in table_names:
            table_names_cleaned.append(name[0])
            table_names_cleaned.append(",")

        self.seeTableNamesLabel["text"] = table_names_cleaned[:len(table_names_cleaned) - 1]
    

root = Tk()
main_win = MainWin(root)
root.mainloop()

conn.close()
