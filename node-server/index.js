const path = require('path');
const express = require('express')
const cors = require('cors')
const app = express()
// data
const unSorted = require('./data/unsorted.json')
const graphCreate = require('./data/graph-create.json')
const graphSolve = require('./data/graph-solve.json')

const port = process.env.PORT || 8081

app.use(express.static(path.join(__dirname, 'public')));
app.use(cors())

app.get('/', (req, res) => {
    res.sendFile(__dirname, '/public/index.html');
});

app.get('/unsorted', (req, res) => {
    res.status(200).json(unSorted)
})

app.get('/graph-create', (req, res) => {
    res.status(200).json(graphCreate)
})

app.get('/graph-solve', (req, res) => {
    res.status(200).json(graphSolve)
})

app.listen(port, () => console.log('server started on port', port))
