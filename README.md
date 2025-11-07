# Auto-Anki-Generator

Auto-Anki-Generator is a Python-based tool that streamlines the process of creating Anki flashcards from study materials. By simply importing a PDF, the program intelligently extracts content and generates visually appealing and well-structured flashcards and notes, perfect for efficient exam preparation. This automation reduces manual effort, ensuring users can quickly convert class notes, lecture slides, or textbooks into ready-to-study material for spaced repetition with Anki.

Key Features:

* Automatic PDF parsing: Seamlessly import any study PDF and have key points extracted for flashcard creation.

* Aesthetic formatting: Outputs flashcards in a clean, organized format to maximize memorization and review efficiency.

* Custom prompt integration: Uses carefully designed prompts (with AI augmentation) to generate high-quality study notes.

* Designed for students: Ideal for anyone needing fast, reliable flashcard generation from complex documents.

## 🚀 How to Use AutoAnkiGenerator (macOS)

### Step One: Download and Unzip
1. Download the latest `.zip` from [GitHub Releases](https://github.com/KdotJo/Auto-Anki-Generator/releases/tag/v1.0.0).
2. Unzip the file so that `AutoAnkiGenerator.app` appears in your **Downloads** folder.

### Step Two: Allow the App to Run (macOS Security Step)
Macs block apps downloaded from the internet by default.  
To allow the app:

1. Open Terminal, run:
   
    `xattr -cr /path/to/AutoAnkiGenerator.app`

    Since you will be downloading the zip file and assuming you open the zip in your downloads folder your cmd will likely be 

    `xattr -cr ~/Downloads/AutoAnkiGenerator.app`

2. Now double-click the app—it will open normally!

This is required for new/unnotarized apps on recent Macs.

### Step Three: Now, double-click `AutoAnkiGenerator.app` in your Downloads folder.

### Step Four: Enter Your OpenAI API Key
- When you first run the app, you’ll be prompted to paste your [OpenAI API key](https://platform.openai.com/account/api-keys).
- Your key will be saved for future use, so you’ll only need to do this once.

### Step Five: Choose Your Lecture PDF
- When prompted, pick the PDF file you want to convert into Anki flashcards.

### Step Six: Save Your Anki Deck
- After processing, select where to save the generated `.apkg` file (e.g., Desktop or Documents).
- When complete, you’ll get a confirmation dialog.

### Step Seven: Import Into Anki
- Open the Anki app and import the `.apkg` flashcard deck.

## Yay you've completed the steps to set it up now you can open the app whenever you want and import your pdfs to make banger flashcards! I hope you enjoy your improvements in grades! Carpe Diem!