import tkinter
from tkinter import *
import sqlite3
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

        self.testGameButton = Button(master, text="Testing Game", command=self.go_to_test_game, background="pink")
        self.testGameButton.place(x=257, y=130)

    def destroy_elements(self):
        self.testLabel.destroy()
        self.editDeckButton.destroy()
        self.viewDeckButton.destroy()
        self.createDeckButton.destroy()
        self.testGameButton.destroy()

    def go_to_edit_deck(self):
        self.destroy_elements()
        self.editDeckNav = EditDeck(root)
    
    def go_to_view_deck(self):
        self.destroy_elements()
        self.viewDeckNav = ViewDeckWin(root)
    
    def go_to_create_deck(self):
        self.destroy_elements()
        self.createDeckNav = CreateDeck(root)

    def go_to_test_game(self):
        self.destroy_elements()
        self.testGameNav = TestGame(root)


# Editing Window --------------------------------------------------------
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
        self.cardAddedLabel.place(x=280, y=195)

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
        if len(self.questionEntry.get()) == 0 or len(self.answerEntry.get()) == 0:
            self.cardAddedLabel["text"] = "Question and Answer values cannot be blank"
        else:
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


# Viewing Window -----------------------------------------------------------------------------------------
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

# Make Testing Game --------------------------------------------------------------------------------------------------
class TestGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Test yourself!")
        self.master.geometry("600x500")
        self.master.minsize(600, 500)
        self.master.maxsize(600, 500)

        self.backButton = Button(master, text="Back to Main Menu", command=self.back_to_menu, background="pink")
        self.backButton.place(x=10, y=10)

        self.tableLoadLabel = Label(master, text="Table to load:")
        self.tableLoadLabel.place(x=160, y=50)

        self.tableLoadEntry = Entry(master, width=40)
        self.tableLoadEntry.place(x=245, y=50)

        self.tableQuestionText = Label(master)
        self.tableQuestionText.place(x=150, y=150)

        self.answerChoiceButtonOne = Button(master, text="1", command=self.one_clicked, padx=10, pady=10, wraplength=240)
        self.answerChoiceButtonTwo = Button(master, text="2", command=self.two_clicked, padx=10, pady=10, wraplength=240)
        self.answerChoiceButtonThree = Button(master, text="3", command=self.three_clicked, padx=10, pady=10, wraplength=240)
        self.answerChoiceButtonFour = Button(master, text="4", command=self.four_clicked, padx=10, pady=10, wraplength=240)

        self.answerChoiceButtonOne.place(x=35, y=205)
        self.answerChoiceButtonTwo.place(x=35, y=305)
        self.answerChoiceButtonThree.place(x=300, y=205)
        self.answerChoiceButtonFour.place(x=300, y=305)

        self.loadTableButton = Button(master, text="Load Table", command=self.load_table_questions, background="pink")
        self.loadTableButton.place(x=280, y=75)

        self.newQuestionButton = Button(master, text="New Question", command=self.load_random_question, background="pink")
        self.newQuestionButton.place(x=272, y=418)

    def load_random_question(self):
        global data_rows
        global count_row
        global rows
        global card_val

        if len(data_rows) < 5:
            self.tableQuestionText["text"] = "error, must have more than 5 cards to play the Testing Game"
        else:
            count_row = random.randint(0, len(data_rows) - 1)
            card_val = count_row + 1
            self.set_buttons()

    def set_buttons(self):
        self.tableQuestionText["text"] =  f'{rows[count_row][1]}'

        self.answerChoiceButtonOne["text"] = f'{rows[random.randint(0, len(data_rows) - 1)][2]}'
        self.answerChoiceButtonTwo["text"] = f'{rows[random.randint(0, len(data_rows) - 1)][2]}'
        self.answerChoiceButtonThree["text"] = f'{rows[random.randint(0, len(data_rows) - 1)][2]}'
        self.answerChoiceButtonFour["text"] = f'{rows[random.randint(0, len(data_rows) - 1)][2]}'

        self.duplicate_check()

        # resetting colors

        self.answerChoiceButtonOne["background"] = "gray"
        self.answerChoiceButtonTwo["background"] = "gray"
        self.answerChoiceButtonThree["background"] = "gray"
        self.answerChoiceButtonFour["background"] = "gray"

    def load_table_questions(self):
        global data_rows
        global count_row
        global rows
        global card_val

        global buttonOneClicked
        global buttonTwoClicked
        global buttonThreeClicked
        global buttonFourClicked

        buttonOneClicked = False
        buttonTwoClicked = False
        buttonThreeClicked = False
        buttonFourClicked = False

        table_name = self.tableLoadEntry.get()
        
        try:
            card_val = 1

            rows = []
            count_row = 0

            c.execute(f'''SELECT * FROM {table_name}''')
            data_rows = c.fetchall()

            if len(data_rows) < 5:
                self.tableQuestionText["text"] = "error, must have more than 5 cards to play the Testing game"
            else:


                for row in data_rows:
                    rows.append(row)

                self.set_buttons()
            
        except:
            print("error")
    
    def duplicate_check(self):
            comparisons = [self.answerChoiceButtonOne["text"] == self.answerChoiceButtonTwo["text"],
                           self.answerChoiceButtonOne["text"] == self.answerChoiceButtonThree["text"],
                           self.answerChoiceButtonOne["text"] == self.answerChoiceButtonFour["text"],
                           self.answerChoiceButtonTwo["text"] == self.answerChoiceButtonOne["text"],
                           self.answerChoiceButtonTwo["text"] == self.answerChoiceButtonThree["text"],
                           self.answerChoiceButtonTwo["text"] == self.answerChoiceButtonFour["text"],
                           self.answerChoiceButtonThree["text"] == self.answerChoiceButtonOne["text"],
                           self.answerChoiceButtonThree["text"] == self.answerChoiceButtonTwo["text"],
                           self.answerChoiceButtonThree["text"] == self.answerChoiceButtonFour["text"]]

            
            comparison_flag = comparisons.count(True)
            
            while comparison_flag != 0:
                self.answerChoiceButtonOne["text"] = f'{rows[random.randint(0, len(data_rows) - 1)][2]}'
                self.answerChoiceButtonTwo["text"] = f'{rows[random.randint(0, len(data_rows) - 1)][2]}'
                self.answerChoiceButtonThree["text"] = f'{rows[random.randint(0, len(data_rows) - 1)][2]}'
                self.answerChoiceButtonFour["text"] = f'{rows[random.randint(0, len(data_rows) - 1)][2]}'

                comparisons = [self.answerChoiceButtonOne["text"] == self.answerChoiceButtonTwo["text"],
                           self.answerChoiceButtonOne["text"] == self.answerChoiceButtonThree["text"],
                           self.answerChoiceButtonOne["text"] == self.answerChoiceButtonFour["text"],
                           self.answerChoiceButtonTwo["text"] == self.answerChoiceButtonOne["text"],
                           self.answerChoiceButtonTwo["text"] == self.answerChoiceButtonThree["text"],
                           self.answerChoiceButtonTwo["text"] == self.answerChoiceButtonFour["text"],
                           self.answerChoiceButtonThree["text"] == self.answerChoiceButtonOne["text"],
                           self.answerChoiceButtonThree["text"] == self.answerChoiceButtonTwo["text"],
                           self.answerChoiceButtonThree["text"] == self.answerChoiceButtonFour["text"]]

                comparison_flag = comparisons.count(True)

                
            buttons = [self.answerChoiceButtonOne, self.answerChoiceButtonTwo, 
                    self.answerChoiceButtonThree, self.answerChoiceButtonFour]
                
            buttons[random.randint(0, 3)]["text"] = f'{rows[count_row][2]}'

            comparisons = [self.answerChoiceButtonOne["text"] == self.answerChoiceButtonTwo["text"],
                           self.answerChoiceButtonOne["text"] == self.answerChoiceButtonThree["text"],
                           self.answerChoiceButtonOne["text"] == self.answerChoiceButtonFour["text"],
                           self.answerChoiceButtonTwo["text"] == self.answerChoiceButtonOne["text"],
                           self.answerChoiceButtonTwo["text"] == self.answerChoiceButtonThree["text"],
                           self.answerChoiceButtonTwo["text"] == self.answerChoiceButtonFour["text"],
                           self.answerChoiceButtonThree["text"] == self.answerChoiceButtonOne["text"],
                           self.answerChoiceButtonThree["text"] == self.answerChoiceButtonTwo["text"],
                           self.answerChoiceButtonThree["text"] == self.answerChoiceButtonFour["text"]]

            if comparisons.count(True) != 0:
                self.duplicate_check()
                

        
    def one_clicked(self):
        global buttonOneClicked
        buttonOneClicked = True
        self.check_answer()
    
    def two_clicked(self):
        global buttonTwoClicked
        buttonTwoClicked = True
        self.check_answer()

    def three_clicked(self):
        global buttonThreeClicked
        buttonThreeClicked = True
        self.check_answer()
    
    def four_clicked(self):
        global buttonFourClicked
        buttonFourClicked = True
        self.check_answer()

    def check_answer(self):
        global buttonOneClicked
        global buttonTwoClicked
        global buttonThreeClicked
        global buttonFourClicked

        vals = [[buttonOneClicked, self.answerChoiceButtonOne], 
                [buttonTwoClicked, self.answerChoiceButtonTwo],
                [buttonThreeClicked, self.answerChoiceButtonThree],
                [buttonFourClicked, self.answerChoiceButtonFour]]
        
        for button in vals:
            if button[1]["text"] == f'{rows[count_row][2]}':
                button[1]["background"] = "green"
            else:
                button[1]["background"] = "red"
                

        
    def back_to_menu(self):
        self.backButton.destroy()
        self.tableLoadEntry.destroy()
        self.tableLoadLabel.destroy()
        self.tableQuestionText.destroy()
        self.loadTableButton.destroy()
        self.answerChoiceButtonOne.destroy()
        self.answerChoiceButtonTwo.destroy()
        self.answerChoiceButtonThree.destroy()
        self.answerChoiceButtonFour.destroy()
        self.newQuestionButton.destroy()

        self.mainMenuNav = MainWin(root)


# Creating Window ------------------------------------------------------------------------------------
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

        self.uploadDeckFromCSVButton = Button(master, text="Create deck from CSV", background="light blue", command=self.go_to_upload_csv)
        self.uploadDeckFromCSVButton.place(x=10,y=180)

    def create_the_table(self):
        deck_title = self.deckName.get()
        if len(deck_title.split()) > 1:
            self.deckCreatedLabel["text"] = "Invalid Deck Name. No spaces allowed."
        else:
            c.execute(f'''CREATE TABLE IF NOT EXISTS {deck_title.lower()} (deck_name text, question text, answer text)''')
            self.deckCreatedLabel["text"] = f'Deck named {deck_title} created! (or already exists)'

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
        self.uploadDeckFromCSVButton.destroy()

        self.mainMenuNav = MainWin(root)

    def go_to_upload_csv(self):
        self.backButton.destroy()
        self.deckName.destroy()
        self.deckNameLabel.destroy()
        self.createNewDeck.destroy()
        self.deckCreatedLabel.destroy()
        self.seeTablesButton.destroy()
        self.seeTableNamesLabel.destroy()
        self.uploadDeckFromCSVButton.destroy()

        self.mainMenuNav = UploadFromCSVWin(root)

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

class UploadFromCSVWin:
    def __init__(self, master):
        self.master = master
        self.master.title("Create a deck from CSV!")
        self.master.geometry("600x500")
        self.master.minsize(600, 500)
        self.master.maxsize(600, 500)

        self.csvFileNameLabel = Label(master, text="CSV File name (exclude '.csv'): ")
        self.csvFileNameLabel.place(x=110, y=100)

        self.csvFileNameEntry = Entry(master)
        self.csvFileNameEntry.place(x=300, y=100)

        self.csvUploadFile = Button(master, text="Upload CSV", command=self.upload_deck, background="light blue")
        self.csvUploadFile.place(x=245, y=140)

        self.backButton = Button(master, text="Back to Main Menu", command=self.back_to_menu, background="light blue")
        self.backButton.place(x=10, y=10)

        self.confirmationLabel = Label(master, text="")
        self.confirmationLabel.place(x=215, y=190)

        self.deckCreatedLabel = Label(master, text="")
        self.deckCreatedLabel.place(x=215, y=210)

    def upload_deck(self):
        try:
            deck_title = self.csvFileNameEntry.get()
            file = open(f'{deck_title}.csv', 'r', newline='')
            reader = csv.reader(file)

            self.confirmationLabel["text"] = f'{deck_title} has been uploaded!' 
            if len(deck_title.split()) > 1:
                self.deckCreatedLabel["text"] = "Invalid Deck Name. No spaces allowed."
            else:
                c.execute(f'''CREATE TABLE IF NOT EXISTS {deck_title.lower()} (deck_name text, question text, answer text)''')
                self.deckCreatedLabel["text"] = f'Deck named {deck_title} created! (or already exists)'

            count = 1
            for row in reader:
                c.execute(f"""INSERT INTO {deck_title.lower()} VALUES("{deck_title + '_' + str(count)}", "{row[0]}", "{row[1]}")""")
                count += 1
        
            file.close()
        except:
            self.confirmationLabel["text"] = f'{deck_title}.csv does not exist, please enter the csv file name (exclude ".csv")'
            raise Exception

        self.csvFileNameEntry.delete(0, END)
        
        conn.commit()

    def back_to_menu(self):
        self.deckCreatedLabel.destroy()
        self.backButton.destroy()
        self.confirmationLabel.destroy()
        self.csvFileNameEntry.destroy()
        self.csvFileNameLabel.destroy()
        self.csvUploadFile.destroy()

        self.mainMenuNav = MainWin(root)


    

root = Tk()
main_win = MainWin(root)
root.mainloop()

conn.close()
