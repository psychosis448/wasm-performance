import { fmr } from '@/algos/fmr.js'

describe('Fmr', () => {
    it('filters even numbers, build digit sum of abs and sums them up', () => {
        const array = [5, 3, 7, 6, -2, 9, 12]
        const r = fmr(array)
        expect(r).toEqual(11)
    })
})
