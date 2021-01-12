var express = require("express");
var multer = require("multer");
var cors = require("cors");
const sleep = require("util").promisify(setTimeout);
var app = express();

// Ajout socket io
const server = require("http").Server(app);
const io = require("socket.io")(server)
const versions = require("./mock_back/versions.json");
const { STATUS_CODES } = require("http");
const PORT = 8000;
const URL =  "http://localhost:" + PORT
const PROCESSING_TIME = 4000; //Processing time
const TIMEOUT = 500; // Time between two emission of current-status message via socket.io
var etat = false;

var CURRENT_PROGRESS = {
  step: 1,
  max_step: 3,
  step_progress: 0.0,
  total_progress: 0.0,
  done: false,
};
var CURRENT_STATUS = {
    // Envoyé par le serveur, traité par les clients en théorie
    job_id: 1,
    version_id: 4,
    steps: ["Preprocessing", "Processing", "Saving"],
    result_url: null,
    progress: CURRENT_PROGRESS,
  };

app.use(cors());

var storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, "public");
  },
  filename: function (req, file, cb) {
    cb(null, Date.now() + "-" + file.originalname);
  },
});

// UPLOAD ONLY WORKS WITH a form-data BODY  with 'file' as key and the file as a value
var upload = multer({ storage: storage }).single("file");

var upload_without_saving = multer().single("file");

app

  // Ancienne route pour tester l'upload de fichier
  .post("/upload", function (req, res) {
    upload(req, res, function (err) {
      if (err instanceof multer.MulterError) {
        return res.status(500).json(err);
      } else if (err) {
        return res.status(500).json(err);
      }
      console.log("Received and saved file :");
      console.log(req.file);

      return res
        .status(200)
        .sendFile(__dirname + "/public/static/files/example.atex");
      //return res.status(200).send(req.file)
    });
  })

  // Réinitialise le mock (pratique pour les tests)
  .put("/restart", (req, res) => {
    
    etat = false;

    CURRENT_PROGRESS = {
      step: 1,
      max_step: 3,
      step_progress: 0.9,
      total_progress: 0.25,
      done: false,
    };
    CURRENT_STATUS = {
        // Envoyé par le serveur, traité par les clients en théorie
        job_id: 1,
        version_id: 4,
        steps: ["Preprocessing", "Processing", "Saving"],
        result_url: null,
        progress: CURRENT_PROGRESS,
      };


    res.status(200).send("Etat réinitalisé");
  })

  .get("/api/versions", (req, res) => {
    console.log("GET VERSIONS");

    res.status(200).json(versions);
  })

  .get("/api/job/:job_id/result", (req, res) => {
    if (etat) {
      console.log("GET RESULT - RESULTAT DISPONIBLE");
      res.status(200).sendFile(__dirname + "/public/static/files/example.atex");
    } else {
      console.log("GET RESULT - RESULTAT INDISPONIBLE");
      res.status(404).send("Le traitement n'existe pas ou n'est pas fini");
    }
  })

  .post("/api/job", (req, res) => {
    upload_without_saving(req, res, function (err) {
      if (err instanceof multer.MulterError) {
        return res.status(500).json(err);
      } else if (err) {
        return res.status(500).json(err);
      }

      console.log("POST- received file:");
      console.log(req.file);
      console.log("With version_id : " + req.query.version_id);

      if (!etat) {
        (async () => {
          console.log("POST - PROCESSING BEGINS");

          await sleep(PROCESSING_TIME);

          

          CURRENT_PROGRESS = {
            step: 3,
            max_step: 3,
            step_progress: 1,
            total_progress: 1,
            done: true,
          };
          CURRENT_STATUS = {
              job_id: 1,
              version_id: 4,
              steps: ["Preprocessing", "Processing", "Saving"],
              result_url: URL + "/api/job/" + CURRENT_STATUS.job_id + "/result",
              progress: CURRENT_PROGRESS,
            };
            etat = true;
          console.log("POST - PROCESSING ENDED");
        })();

        const mock_job_id = 1;
        //const mock_ws_url = `ws://localhost:${PORT}/job/`;

        return res.status(200).json({ job_ws: mock_job_id });
      } else {
        console.log("POST - TRAITEMENT DEJA EN COURS");
        // res.status(200).send("Traitement déjà en cours");
        const mock_job_id = 1;
        return res.status(200).json({ job_ws: mock_job_id });
      }
    });
  })

  .get("/", (req, res) => {
    res.status(200).send("Bienvenu");
  })

  .get("/io", (req, res) => {
    res.status(200).sendFile(__dirname + '/socket.html');
  });



/**
 * 
 * SOCKET IO STUFF
 * 
 */



const updateStatus = (x) => {
  CURRENT_PROGRESS = {...CURRENT_PROGRESS, step_progress:CURRENT_PROGRESS.step_progress+x, total_progress:CURRENT_PROGRESS.total_progress+x/3}
  if (CURRENT_PROGRESS.step_progress > 1.0 && CURRENT_PROGRESS.step < CURRENT_PROGRESS.max_step) {
    CURRENT_PROGRESS = {...CURRENT_PROGRESS, step_progress:x, step:CURRENT_PROGRESS.step+1}
  } 

  CURRENT_STATUS = {...CURRENT_STATUS, progress: CURRENT_PROGRESS}
}

let requestTrack = []

io.of('/api/job')

.on("connection", (socket) => {

// For tracking the time between each socket message
  const start = Date.now()

  const continuousEmission = () => {

    if (etat == false) {
      updateStatus(0.2)
      console.log("Sending current process status")
      socket.emit('current-status', CURRENT_STATUS)

      requestTrack.push(Date.now())

      setTimeout( continuousEmission, TIMEOUT)
  
    } else {
      console.log("Sending current process status - ENDED")
      socket.emit('current-status', CURRENT_STATUS)
      requestTrack.push(Date.now())
    }
  
  }

  console.log(`Connecté au client ${socket.id}`);

  continuousEmission();

  socket.on("request-progress", (data) => {
    //data = {"job_id":1}

    console.log("Progress requested for job : " + data.job_id);
    socket.emit('current-status', CURRENT_STATUS);
    socket.emit('current-progress', CURRENT_PROGRESS);
    requestTrack.push(Date.now())
  });

  socket.on('disconnect', () => {
    console.log('Client disconnect')
    console.log(requestTrack.map(x => x - start))
  });


});


server.listen(PORT, function () {
  console.log("App runnning on port " + PORT);
});
