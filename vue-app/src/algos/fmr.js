const sumDigits = n => {
    let sum = 0;
    let c = Math.abs(n)
    while (c > 0) {
        sum += c % 10
        c = Math.floor(c / 10)
    }
    return sum
}

export const fmr = arr => arr
    .filter(x => x % 2 === 0)
    .map(x => sumDigits(x))
    .reduce((acc, cur) => acc + cur, 0)
