class Node {
    constructor(data) {
        this.key = data
        this.right = null
        this.left = null
    }
}

export class BinarySearchTree {
    constructor() {
        this.root = null;
    }

    create(array) {
        array.forEach(x => this.insert(x))
    }

    insert(key) {
        let parent_node = null
        let current_tree = this.root
        const new_node = new Node(key)

        while (current_tree !== null) {
            parent_node = current_tree
            if (new_node.key < current_tree.key) {
                current_tree = current_tree.left
            } else {
                current_tree = current_tree.right
            }
        }

        if (parent_node === null) {
            this.root = new_node
        } else if (new_node.key < parent_node.key) {
            parent_node.left = new_node
        } else {
            parent_node.right = new_node
        }
    }

    search(key) {
        let current_node = this.root

        while (current_node !== null && key !== current_node.key) {
            if (key < current_node.key) {
                current_node = current_node.left
            } else {
                current_node = current_node.right
            }
        }

        return current_node
    }

    exist(key) {
        let current_node = this.root

        while (current_node !== null && key !== current_node.key) {
            if (key < current_node.key) {
                current_node = current_node.left
            } else {
                current_node = current_node.right
            }
        }

        return current_node === null ? false : true
    }

}
