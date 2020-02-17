const express = require('express')
const path = require('path')
const PORT = process.env.PORT || 5000

app = express()

app.use(express.static(__dirname + '/dist/frontend'));

app.get('/*', function(req, res) {
  res.sendFile(path.join(__dirname + '/dist/frontend/index.html'));
});

app.listen(PORT, () => console.log(`Listening on ${ PORT }`))
