So far, this section is a proof-of-concept for the frontend consisting of just a dummy login page. To run this on your local machine, follow these instructions:

Run the following commands to clone our repository, navigate to the my-app directory, and install dependencies (React):

(note: you may have to install npm if you haven't already. This is the package manager for node)

'''
git clone git@github.com:smrhoades/CSPB-3308-Team-6.git
cd CSPB-3308-Team-6/my-app
npm install
'''

To run the app in dev mode, use the following command:

'''
npm run dev
'''

This starts running the server locally. In your CLI you will see the URL you should use. Something like:

Local: http://localhost:5173/

Copy+Paste this into your browser and the login page should be visible! It doesn't do anything yet, but the bones are there.

To shut the local server down, just hit q and enter inside the CLI.
