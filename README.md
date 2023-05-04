# affec-asgn3

# How to Run

You need to have Emotiv downloaded on your local machine to simulate the brain data.

1. Start up Emotiv with one of the head device to simulate data from
2. Run `python3 backend.py` to start the Flask server
3. Open `asgn3.html`
4. On the HTML file, click the "Gather Eye + Brain Data" button. This will collect eye tracking data and brain data for the next 10 seconds and combine all this data into a CSV file.
5. Data will be saved to a file called `eye_and_brain_data.csv`

