use serde::{Deserialize, Serialize};
use std::cmp::Ordering;
use wasm_bindgen::prelude::*;

type Tree = Option<Box<Node>>;

#[wasm_bindgen]
#[derive(Debug, PartialEq, Clone, Serialize, Deserialize)]
pub struct Node {
    pub key: i32,
    left: Tree,
    right: Tree,
}

impl Node {
    pub fn new(key: i32) -> Self {
        Node {
            key,
            left: None,
            right: None,
        }
    }
}
#[wasm_bindgen]
#[derive(Debug, PartialEq, Clone, Serialize)]
pub struct BinaryTree {
    root: Tree,
}

#[wasm_bindgen]
impl BinaryTree {
    #[wasm_bindgen(constructor)]
    pub fn new() -> Self {
        BinaryTree { root: None }
    }

    pub fn get(&self) -> JsValue {
        JsValue::from_serde(&self).unwrap()
    }

    pub fn insert(&mut self, key: i32) {
        let mut current_tree = &mut self.root;
        let new_node = Node::new(key);

        while let Some(current_node) = current_tree {
            match new_node.key.cmp(&current_node.key) {
                Ordering::Less => current_tree = &mut current_node.left,
                _ => current_tree = &mut current_node.right,
            };
        }

        *current_tree = Some(Box::new(new_node));
    }

    pub fn create(&mut self, vec: Vec<i32>) {
        for el in vec.iter() {
            self.insert(*el);
        }
    }

    pub fn search(&self, key: i32) -> JsValue {
        let mut current_tree = &self.root;

        while let Some(current_node) = current_tree {
            match key.cmp(&current_node.key) {
                Ordering::Equal => break,
                Ordering::Greater => current_tree = &current_node.right,
                Ordering::Less => current_tree = &current_node.left,
            };
        }

        JsValue::from_serde(&current_tree).unwrap()
    }

    pub fn exist(&self, key: i32) -> bool {
        let mut current_tree = &self.root;

        while let Some(current_node) = current_tree {
            match key.cmp(&current_node.key) {
                Ordering::Equal => break,
                Ordering::Greater => current_tree = &current_node.right,
                Ordering::Less => current_tree = &current_node.left,
            };
        }

        match current_tree {
            Some(_x) => true,
            None => false,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use wasm_bindgen_test::*;

    #[wasm_bindgen_test]
    fn creates_tree() {
        let mut bst = BinaryTree::new();
        bst.insert(5);
        bst.insert(3);
        bst.insert(7);

        let expect = Some(Box::new(Node {
            key: 5,
            left: Some(Box::new(Node {
                key: 3,
                left: None,
                right: None,
            })),
            right: Some(Box::new(Node {
                key: 7,
                left: None,
                right: None,
            })),
        }));

        assert_eq!(bst.root, expect);
    }

    #[wasm_bindgen_test]
    fn successful_search() {
        let mut bst = BinaryTree::new();
        bst.insert(5);
        bst.insert(3);
        bst.insert(7);

        let found_node: Node = bst.search(3).into_serde().unwrap();
        let expect = Node::new(3);

        assert_eq!(found_node, expect);
    }

    #[wasm_bindgen_test]
    fn unsuccessful_search() {
        let mut bst = BinaryTree::new();
        bst.insert(5);
        bst.insert(3);
        bst.insert(7);

        let res = bst.search(9);

        assert_eq!(res, JsValue::NULL);
    }
}
