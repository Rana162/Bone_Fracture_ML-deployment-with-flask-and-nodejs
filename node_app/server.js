const express = require('express');//http server
const multer = require('multer');//handle file uploaf
const fs = require('fs');//reading files
const FormData = require('form-data');
const axios = require('axios');// request server

const app = express();
const port = 4000;

// Multer configuration to handle file uploads
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, 'uploads/');
  },
  filename: function (req, file, cb) {
    cb(null, 'temp_image.jpg');
  }
});

const upload = multer({ storage: storage });

// HTML Form
const formHTML = `
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Fracture Detection</title>
</head>
<body>
  <h2>Upload an X-ray Image</h2>
  <form action="/upload" method="POST" enctype="multipart/form-data">
    <input type="file" name="image">
    <button type="submit">Upload</button>
  </form>
</body>
</html>
`;

// Serve the form
app.get('/', (req, res) => {
  res.send(formHTML);
});

// Handle file upload and send it to Flask server
app.post('/upload', upload.single('image'), async (req, res) => {
  try {
    const image = fs.readFileSync('uploads/temp_image.jpg');

    const formData = new FormData();
    formData.append('image', image, { filename: 'temp_image.jpg' });

    const response = await axios.post('http://localhost:3000/predict', formData, {
      headers: {
        ...formData.getHeaders()
      }
    });

    res.send(`<h2>Prediction: ${response.data.prediction}</h2>`);
  } catch (error) {
    console.error(error);
    res.status(500).send(`<h2>Error: ${error.message}</h2>`);
  }
});

app.listen(port, () => {
  console.log(`Node.js server listening at http://localhost:${port}`);
});

