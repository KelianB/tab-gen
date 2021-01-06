var express = require("express");
var multer = require("multer");
var cors = require("cors");
const sleep = require("util").promisify(setTimeout);
var app = express();

// Ajout socket io
const server = require("http").Server(app);
const io = require("socket.io")(server)
const versions = require("./mock_back/versions.json");
const PORT = 8000;
const TIMEOUT = 3000;
var etat = false;

const CURRENT_STATUS = {
  // Envoyé par le serveur, traité par les clients en théorie
  job_id: 1,
  version_id: 4,
  steps: ["Preprocessing", "Processing", "Saving"],
  result_url: null,
  progress: {
    step: 1,
    max_step: 3,
    step_progress: 0.9,
    total_progress: 0.25,
    done: false,
  },
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
    res.status(200).send("Etat réinitalisé");
  })

  .get("/api/versions", (req, res) => {
    console.log("GET VERSIONS");

    res.status(200).json(versions);
  })

  .get("/api/version/:verion_id/:job_id/state", (req, res) => {
    console.log("GET STATE - Etat actuel : " + etat);

    res.status(200).json({ etat: etat });
  })

  .get("/api/:job_id/result", (req, res) => {
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

      if (!etat) {
        (async () => {
          console.log("POST - PROCESSING BEGINS");
          await sleep(TIMEOUT);
          etat = true;
          console.log("POST - PROCESSING ENDED");
        })();

        const mock_job_id = 1;
        const mock_ws_url = `ws://localhost:${PORT}/job/`;

        return res.status(200).json({ job_ws: mock_ws_url });
      } else {
        console.log("POST - TRAITEMENT DEJA EN COURS");
        res.status(200).send("Traitement déjà en cours");
      }
    });
  })

  .get("/", (req, res) => {
    res.status(200).send("Bienvenu");
  })

  .get("/io", (req, res) => {
    res.status(200).sendFile(__dirname + '/socket.html');
  });

io.of('/admin')
.on("connection", (socket) => {





  console.log(`Connecté au client ${socket.id}`);
});

// io.on("current_status" ,(socket) => {
//     console.log('')
// })

// io.on('/api/job/:job_id', (socket) => {

//     // request-progress
//     socket.on("request-progress", () => {
//         console.log("Progress requested")
//         socket.emit('current-progress',CURRENT_STATUS)
//     })

//     // current-status
//     // current-progress
//     console.log('TODO')
// })

server.listen(PORT, function () {
  console.log("App runnning on port " + PORT);
});
