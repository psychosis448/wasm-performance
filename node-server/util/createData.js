const fs = require('fs');
const randomArray = require('./createArray')
const createMazes = require('./createMaze')

const dataDir = './data'

// mobile does not support bulkMemory yet -> max 10^6
// https://github.com/WebAssembly/bulk-memory-operations/blob/master/proposals/bulk-memory-operations/Overview.md

// UNSORTED DATA CREATION
const unsortedData = {}
const unsortedSizes = Array.from(new Array(6))
    .map((_, i) => Math.pow(10, i + 1))

unsortedSizes.forEach(size => (unsortedData[size] = randomArray(size)))

fs.writeFile(`${dataDir}/unsorted.json`, JSON.stringify(unsortedData), (err) => {
    if (err) {
        return console.log(err);
    }
    console.log("Unsorted data was saved.");
});

// MAZE CREATION
const mazeData = {
    "10x10": {
        "rows": 10,
        "columns": 10
    },
    "50x50": {
        "rows": 50,
        "columns": 50
    },
    "100x100": {
        "rows": 100,
        "columns": 100
    },
    "150x150": {
        "rows": 150,
        "columns": 150
    },
    "200x200": {
        "rows": 200,
        "columns": 200
    },
    "250x250": {
        "rows": 250,
        "columns": 250
    },
    "300x300": {
        "rows": 300,
        "columns": 300
    },
    // "350x350": {
    //     "rows": 350,
    //     "columns": 350
    // },
    // "400x400": {
    //     "rows": 400,
    //     "columns": 400
    // },
}

fs.writeFile(`${dataDir}/graph-create.json`, JSON.stringify(mazeData), err => {
    if (err) {
        return console.log(err)
    }
    console.log("Graph-Create data was saved.")
})

const mazes = createMazes(mazeData)

fs.writeFile(`${dataDir}/graph-solve.json`, JSON.stringify(mazes), err => {
    if (err) {
        return console.log(err)
    }
    console.log("Graph-Solve data was saved.")
})
