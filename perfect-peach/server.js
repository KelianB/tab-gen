var express = require('express');
var multer = require('multer')
var cors = require('cors');
const sleep = require('util').promisify(setTimeout)

var app = express();



const versions = require("./mock_back/versions.json");
const PORT = 8000;
const TIMEOUT = 3000;
var etat = false;

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


    res.status(200).json({etat:etat})
})

.get('/api/version/:version_id/:job_id/result', (req,res) => {

    if (etat) {
        res.status(200).sendFile(__dirname + '/public/static/files/example.atex');

    } else {
        res.status(404).send("Le traitement n'existe pas ou n'est pas fini")
    }


})


.post('/api/version/:version_id', (req,res) => {

    if (!etat) {

        upload(req, res, (err) => {
            if (err instanceof multer.MulterError) {
                return res.status(500).json(err)
            } else if (err) {
                return res.status(500).json(err)
            }

            //ADD A TIMER TO MOCK THE TAB PROCESSING TIME

            if (!etat) {
                (async () => {
                    console.log("PROCESSING BEGINS")
                    await sleep(TIMEOUT)
                    etat = true
                    console.log("PROCESSING ENDED")
                })()
            }
            
            const mock_job_id = 1;

            return res.status(200).json({job_id:mock_job_id});
        })
    } else {
        res.status(200).send("Traitement déjà en cours")
    }
    
    





});



app.listen(PORT, function () {
    console.log('App runnning on port ' + PORT);
});
