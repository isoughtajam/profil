const nunjucks = require('nunjucks');
const express = require('express');
const app = express();

app.listen(3000);

nunjucks.configure('views', {
    autoescape: true,
    express: app
});

app.get('/', function(req, res) {
    res.render('index.html');
});
