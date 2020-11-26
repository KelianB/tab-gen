var express = require('express');
var multer = require('multer')
var cors = require('cors');

var app = express();


const versions = require("./mock_back/versions.json");
const { version } = require('react');
const PORT = 8000;

app.use(cors())

var storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, 'public')
    },
    filename: function (req, file, cb) {
        cb(null, Date.now() + '-' + file.originalname)
    }
})

var upload = multer({ storage: storage }).single('file')



app.post('/upload', function (req, res) {
    upload(req, res, function (err) {
        if (err instanceof multer.MulterError) {
            return res.status(500).json(err)
        } else if (err) {
            return res.status(500).json(err)
        }
        return res.status(200).sendFile(__dirname + '/public/static/files/example.atex')
        //return res.status(200).send(req.file)
    })
})

.get('/api/versions', (req,res) => {

    res.status(200).json(versions);
})

.get('/api/version/:verion_id/:job_id/state', (req,res) => {

    // ADD A TIMER TO MOCK THE TAB PROCESSING TIME

    res.state(200).json({etat:false})
})

.get('/api/version/:version_id/:job_id/result', (req,res) => {

    // ADD A TIMER TO MOCK THE TAB PROCESSING TIME

    res.status(200).sendFile(__dirname + '/public/static/files/example.atex');
})


.post('/api/version/:version_id', (req,res) => {

    upload(req, res, (err) => {
        if (err instanceof multer.MulterError) {
            return res.status(500).json(err)
        } else if (err) {
            return res.status(500).json(err)
        }

        //ADD A TIMER TO MOCK THE TAB PROCESSING TIME
        
        const mock_job_id = 1;

        return res.status(200).json({job_id:mock_job_id});
    })



});



app.listen(PORT, function () {
    console.log('App runnning on port ' + PORT);
});
