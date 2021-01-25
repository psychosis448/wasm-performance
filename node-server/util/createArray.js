// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/random
const getRandomInt = (min, max) => {
    min = Math.ceil(min);
    max = Math.floor(max);

    return Math.floor(Math.random() * (max - min + 1)) + min;
}

// https://doc.rust-lang.org/std/primitive.i32.html
const getRandomI32 = () => {
    const i32MIN = -2147483648;
    const i32MAX = 2147483647;

    return getRandomInt(i32MIN, i32MAX)
}

// https://doi.org/10.1145/364520.364540
const durstenfeldShuffle = (array) => {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
}

const randomArray = (size) => {
    const randomSet = new Set()

    for (let i = 0; i < size; i++) {
        let r = getRandomI32()

        // make sure values are unique
        while (randomSet.has(r)) {
            r = getRandomI32()
        }

        randomSet.add(r)
    }

    const randomArray = Array.from(randomSet)

    // shuffle once
    durstenfeldShuffle(randomArray)

    return randomArray
}

module.exports = randomArray
