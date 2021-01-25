import { BinarySearchTree } from '@/algos/BinaryTree.js'

class Node {
    constructor(data, left = null, right = null) {
        this.key = data
        this.right = right
        this.left = left
    }
}

describe('Binary Tree', () => {
    it('sets root node correctly', () => {
        const tree = new BinarySearchTree()
        tree.insert(5)

        expect(tree.root).toEqual(new Node(5))
    })

    it('finds the correct node for a given key', () => {
        const tree = new BinarySearchTree()
        tree.create([5, 3, 7, 2, 5, 8])

        const node = new Node(7, new Node(5), new Node(8))

        expect(tree.search(7)).toEqual(node)
    })

    it('returns null if search is unsuccessful', () => {
        const tree = new BinarySearchTree()
        tree.create([5, 3, 7, 2, 5, 8])

        expect(tree.search(9)).toEqual(null)
    })
})
