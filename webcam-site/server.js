const express = require('express');
const path = require('path');
const app = express();
const PORT = 3000;

app.use(express.static(path.join(__dirname, 'public')));

app.get('/', (req, res) => {
  res.send(`
    <!DOCTYPE html>
    <html><head><title>Webcam</title></head>
    <body style="margin:0; background:#000;">
      <img id="webcam" src="latest.jpg" style="width:640px; height:480px; display:block; margin:auto;">
      <script>
        const img = document.getElementById('webcam');
        setInterval(() => {
          img.src = 'latest.jpg?t=' + new Date().getTime();
        }, 66);
      </script>
    </body>
    </html>
  `);
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
