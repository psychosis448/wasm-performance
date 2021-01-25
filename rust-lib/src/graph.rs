use rand::Rng;
use serde::{Deserialize, Serialize};
use std::cmp::Reverse;
use std::collections::BinaryHeap;
use std::collections::HashMap;
use std::collections::HashSet;
use std::iter::FromIterator;
use wasm_bindgen::prelude::*;

fn format_value(x: i32, y: i32) -> String {
    format!("{},{}", x, y)
}

#[derive(Debug, Deserialize, Serialize)]
struct Vertex {
    value: String,
    x: i32,
    y: i32,
}

// used for easier conversion
#[derive(Debug, Deserialize, Serialize)]
struct JsGraph {
    rows: i32,
    columns: i32,
    startVertex: String,
    endVertex: String,
    vertices: HashMap<String, Vertex>,
    edges: HashMap<String, Vec<String>>,
}

#[wasm_bindgen]
#[derive(Debug, Deserialize, Serialize)]
pub struct Graph {
    rows: i32,
    columns: i32,
    start_vertex: String,
    end_vertex: String,
    vertices: HashMap<String, Vertex>,
    edges: HashMap<String, Vec<String>>,
}

impl Vertex {
    pub fn new(x: i32, y: i32) -> Self {
        Vertex {
            value: format_value(x, y),
            x,
            y,
        }
    }

    pub fn get_neighbors(&self, columns: i32, rows: i32) -> Vec<String> {
        let mut neighbors = Vec::new();

        if self.y > 0 {
            neighbors.push(format_value(self.x, self.y - 1));
        }
        if self.y < rows - 1 {
            neighbors.push(format_value(self.x, self.y + 1));
        }
        if self.x > 0 {
            neighbors.push(format_value(self.x - 1, self.y));
        }
        if self.x < columns - 1 {
            neighbors.push(format_value(self.x + 1, self.y));
        }

        neighbors
    }
}

#[wasm_bindgen]
impl Graph {
    #[wasm_bindgen(constructor)]
    pub fn new(rows: i32, columns: i32) -> Self {
        let mut vertices = HashMap::new();

        for x in 0..rows {
            for y in 0..columns {
                let vertex = Vertex::new(x, y);
                vertices.insert(String::from(&vertex.value), vertex);
            }
        }

        Graph {
            rows,
            columns,
            start_vertex: format_value(0, 0),
            end_vertex: format_value(columns - 1, rows - 1),
            vertices,
            edges: HashMap::new(),
        }
    }

    pub fn get_start(&self) -> JsValue {
        JsValue::from_serde(&self.start_vertex).unwrap()
    }

    pub fn get_end(&self) -> JsValue {
        JsValue::from_serde(&self.end_vertex).unwrap()
    }

    pub fn set_maze_from_js(&mut self, maze: JsValue) {
        let js_maze: JsGraph = maze.into_serde().unwrap();
        self.rows = js_maze.rows;
        self.columns = js_maze.columns;
        self.start_vertex = js_maze.startVertex;
        self.end_vertex = js_maze.endVertex;
        self.vertices = js_maze.vertices;
        self.edges = js_maze.edges;
    }

    pub fn create_maze(&mut self) {
        self.edges = self.prim_maze();
    }

    pub fn get_maze(&self) -> JsValue {
        JsValue::from_serde(&self.edges).unwrap()
    }

    pub fn get_graph(&self) -> JsValue {
        JsValue::from_serde(&self).unwrap()
    }

    pub fn solve_maze(&self) -> JsValue {
        JsValue::from_serde(&self.a_star()).unwrap()
    }

    fn get_vertex(&self, value: &String) -> &Vertex {
        self.vertices.get(value).unwrap()
    }

    fn prim_maze(&self) -> HashMap<String, Vec<String>> {
        let mut rng = rand::thread_rng();

        let mut path_set = HashSet::new();
        let mut visited = HashSet::new();
        let mut edges = HashMap::new();

        for (key, _) in self.vertices.iter() {
            edges.insert(key.clone(), Vec::new());
        }

        let start_neighbors = self
            .get_vertex(&self.start_vertex)
            .get_neighbors(self.columns, self.rows);

        for neighbor in start_neighbors {
            path_set.insert(neighbor.clone());
        }

        visited.insert(self.start_vertex.clone());

        while !path_set.is_empty() {
            let paths = Vec::from_iter(path_set.iter());

            let rand_v = rng.gen_range(0, paths.len());
            let random_path = &paths[rand_v];
            let current_vertex = self.get_vertex(random_path);
            visited.insert(current_vertex.value.clone());

            let current_neighbors = current_vertex.get_neighbors(self.columns, self.rows);
            let mut available_neighbors = Vec::new();

            for neighbor in current_neighbors {
                if visited.get(&neighbor).is_some() {
                    available_neighbors.push(neighbor.clone());
                } else {
                    path_set.insert(neighbor.clone());
                }
            }

            if !available_neighbors.is_empty() {
                let rand_n = rng.gen_range(0, available_neighbors.len());
                let new_edge = &available_neighbors[rand_n];

                edges
                    .get_mut(&current_vertex.value)
                    .unwrap()
                    .push(new_edge.clone());

                edges
                    .get_mut(new_edge)
                    .unwrap()
                    .push(current_vertex.value.clone());
            }

            path_set.remove(&current_vertex.value);
        }

        edges
    }

    fn manhattan_distance(&self, vertex: &Vertex, destination: &Vertex) -> i32 {
        let d1 = (destination.x - vertex.x).abs();
        let d2 = (destination.y - vertex.y).abs();
        d1 + d2
    }

    fn a_star(&self) -> Option<Vec<String>> {
        let start = &self.start_vertex;
        let end = &self.end_vertex;
        let end_vertex = self.vertices.get(end).unwrap();

        // push(Reverse()) creates a min Heap -> pop() returns smallest element
        let mut open_queue = BinaryHeap::new();
        let mut closed_set = HashSet::new();
        let mut g_scores = HashMap::new();
        let mut parents: HashMap<&String, String> = HashMap::new();

        // init g_scores
        for edge in self.edges.iter() {
            if edge.0 != start {
                g_scores.insert(edge.0, i32::MAX);
            } else {
                g_scores.insert(edge.0, 0);
            }
        }

        // f score, vertex
        open_queue.push(Reverse((0, start)));

        while !open_queue.is_empty() {
            let current_vertex = open_queue.pop().unwrap().0;

            if current_vertex.1 == end {
                let mut path_to_freedom = Vec::new();
                let mut next = current_vertex.1;
                path_to_freedom.push(next.clone());

                while next != start {
                    let child = parents.get(&next).unwrap();
                    path_to_freedom.push(child.clone());
                    next = child;
                }

                path_to_freedom.reverse();

                return Some(path_to_freedom);
            }

            closed_set.insert(current_vertex.1);

            let g_score = g_scores.get(current_vertex.1).unwrap() + 1;
            let vertex_edges = self.edges.get(current_vertex.1).unwrap();

            for edge in vertex_edges {
                if closed_set.get(edge).is_none() {
                    let edge_g = g_scores.get_mut(edge).unwrap();

                    if &g_score < &edge_g {
                        let edge_vertex = self.vertices.get(edge).unwrap();
                        let edge_h = self.manhattan_distance(edge_vertex, end_vertex);
                        let edge_f = g_score + edge_h;

                        g_scores.insert(edge, g_score);
                        open_queue.push(Reverse((edge_f, edge)));
                        parents.insert(edge, current_vertex.1.to_string());
                    }
                }
            }
        }

        None
    }
}
