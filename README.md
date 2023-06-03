# FlashcardMaker
This project allows the user to create flashcard decks, view/add to decks, and export decks to CSV files

<h1> Technologies Used </h1>
<ul>
  <li> Python </li>
  <li> Tkinter Module </li>
  <li> SQLite3 </li>
  <li> Other modules such as "Random" and "CSV" </li>
  
<h1> Documentation </h1>
  
  How to use:
  - There are four sections to this application: Creating, Editing, Viewing, and a Multiple Choice Question game. <br>
  - Note: SQLite should automatically create the database to store tables/decks for you in the project folder.
  
<h5> Creating View </h5>
  - You can initialize a deck and view which decks have already been created.
  
<h5>Editing View </h5>
  - Add cards to existing decks, Delete unwanted decks.
  
<h5> Viewing </h5> 
  - Load a table, cycle through flash cards using "Next Question", "Previous Question", and "Random Question" buttons. <br>
  - Export the table to a CSV file (or updating it based on if the .csv is already created). <br>
  - A deck counter will be shown to track your navigation through the deck. <br>
  
<h5> Testing Game </h5>
  - Load a previously created deck and press "Load Table" <br>
  - A random question from the deck will be drawn <br>
  - You will be presented with four possible answers, one being correct <br>
  - Pick an answer, then press the "New Question" button to continue playing
