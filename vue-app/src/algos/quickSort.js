export const quicksort = arr => qs(arr, 0, arr.length - 1)

const qs = (arr, low, high) => {
    if (low < high) {
        const p = partition(arr, low, high)
        if (p > 0) {
            qs(arr, low, p - 1)
        }
        qs(arr, p + 1, high)
    }
}

const partition = (arr, low, high) => {
    let i = low
    const pivot = arr[high]

    for (let j = low; j < high; j++) {
        if (arr[j] < pivot) {
            const temp = arr[i]
            arr[i] = arr[j]
            arr[j] = temp
            i++
        }
    }

    const temp = arr[high]
    arr[high] = arr[i]
    arr[i] = temp

    return i
}
