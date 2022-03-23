from flask import Flask, redirect, render_template, request
import pandas as pd
import numpy as np
from werkzeug import secure_filename

# configure 

app = Flask(__name__)


@app.route("/", methods = ["GET", "POST"])
def upload_file():
    if request.method == "GET":
       message_0 = "Ide told a cuccot."
       message_1 = "Itt látod majd az eredményt"
       
    else:
        f = request.files['file']
        guess_csv = secure_filename(f.filename)
        f.save(guess_csv)
        message_0 = 'File uploaded successfully as {file}'.format(file=guess_csv)
	
        # checking the file
        solutions = pd.read_csv('solutions.csv', index_col=0)
        guess = pd.read_csv(guess_csv, index_col=0)
 
        if guess.index[0] == solutions.index[0]:
            guess['Results']= np.where((guess.iloc[:,-1] == solutions['Transported']), 1, 0)
            message_1 = f"We have the same dataset, first data is: {solutions.iloc[0,:-1]}.\n Total correct predictions: {sum(guess.Results)}/ {len(guess.Results)}, accuracy: {np.mean(guess.Results)}"
        
    
        else: 
            message_1 = f"Error, different dataset, first data of guess is {guess.iloc[0,:-1]}, first data of solutions is {solutions.iloc[0]}"
        
    return render_template("index.html", message_0 = message_0, message_1 = message_1)
    
    
    	
if __name__ == '__main__':
   app.run(debug = True)