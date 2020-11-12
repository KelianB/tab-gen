var express = require('express');
var multer = require('multer')
var cors = require('cors');

var app = express();

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
});

app.listen(PORT, function () {
    console.log('App runnning on port ' + PORT);
});
