# Perfect Peach

Perfect Peach is a ReactJS front-end of project tab-gen which aims to compute the sheet music of a given music file using Deep Learning methods.

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `npm install`

Before you do anything else, you must install the dependencies, which are listed in _package.json_

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.

### `nodemon server.js`

Starts on **PORT:8000** a NodeJS server contained in _server.js_. This server will receive for now the POST request from Perfect Peach containing the audio files and will respond with the file 'example.atex', which is a text file containing a score in AlphaTex format.
