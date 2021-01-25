import { quicksort } from '@/algos/quickSort.js'

describe('Quicksort', () => {
  it('sorts a given array of numbers', () => {
    const array = [5, 3, 7, 6, 2, 9]
    quicksort(array)
    expect(array).toEqual([2, 3, 5, 6, 7, 9])
  })
})
