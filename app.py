from flask import Flask, render_template, request, redirect, session, url_for
import csv

app = Flask(__name__)

YOGA_PATH = app.root_path + '/classes.csv'


YOGA_KEYS = ['slug','name', 'type', 'level', 'date', 'duration (min)', 'trainer', 'description']

def get_classes():
    with open(YOGA_PATH, 'r') as csvfile:
            data = csv.DictReader(csvfile)
            classes = {}
            for session in data:
                classes[session['slug']] = session
    return classes

#function to write out the classes data to csv
def set_classes(classes):
    with open(YOGA_PATH, mode ='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=YOGA_KEYS)
        writer.writeheader()
        for session in classes.values():
            writer.writerow(session)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/classes/')
@app.route('/classes/<session>')
def classes(session=None):
#fill in the logic for the 2 routes
    classes=get_classes()
    #if session exists and it is in the list of session names, render class.html and pass the specific session dictionary
    if session and session in classes.keys():
        classy = classes[session]
        return render_template('class.html', classy=classy)
    #else, render the classes.html template per normal
    else:
        return render_template('classes.html', classes=classes)

@app.route("/classes/create", methods=['GET', 'POST'])
def class_form():
    # if POST request received (form submitted)
   if request.method == 'POST':
       # get classes.csv data
       classes = get_classes()
       # create new dict to hold session data from form
       newClass={}
       # add form data to new dict
       newClass['slug'] = request.form['slug']
       newClass['date'] = request.form['date']
       newClass['name'] = request.form['name']
       newClass['type'] = request.form['type']
       newClass['duration (min)'] = request.form['duration (min)']
       newClass['level'] = request.form['level']
       newClass['trainer'] = request.form['trainer']
       newClass['description'] = request.form['description']
       # add new dict to csv data
       classes[request.form['name']] = newClass
       # write csv data back out to csv file
       set_classes(classes)
       # since POST request, redirect after save (we want the display to change so user knows form went through)
       return redirect(url_for('classes'))
   # if GET request received (display form)
   else:
       return render_template('class_form')

@app.route("/classes/<class_id>/edit", methods=['GET', 'POST'])
def edit(session=session):
    # if POST request received (form submitted)
    if request.method =='POST':
       # get classes.csv data
       classes = get_classes()

       del classes[session]
       # create new dict to hold session data from form
       row={session:classes[session]}
       # add form data to new dict
       row['slug'] = request.form['slug']
       row['date'] = request.form['date']
       row['name'] = request.form['name']
       row['type'] = request.form['type']
       row['duration (min)'] = request.form['duration (min)']
       row['level'] = request.form['level']
       row['trainer'] = request.form['trainer']
       row['description'] = request.form['description']
       # add new dict to csv data
       classes.update(row)
       # write csv data back out to csv file
       set_classes(classes)
       # since POST request, redirect after save (we want the display to change so user knows form went through)
       return redirect(url_for('classes'))
   # if GET request received (display form)
    else:
        return render_template('class_form')
      

