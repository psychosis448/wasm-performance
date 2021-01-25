use wasm_bindgen::prelude::*;

#[wasm_bindgen]
#[allow(dead_code)]
pub fn quicksort_vec(arr: Vec<i32>) -> JsValue {
    let mut arr_vec = arr.clone();
    qs(&mut arr_vec, 0, arr.len() - 1);
    JsValue::from_serde(&arr_vec).unwrap()
}

fn qs(arr: &mut Vec<i32>, low: usize, high: usize) -> () {
    if low < high {
        let p = partition(arr, low, high);
        if p > 0 {
            qs(arr, low, p - 1);
        }
        qs(arr, p + 1, high);
    }
}

fn partition(arr: &mut Vec<i32>, low: usize, high: usize) -> usize {
    let mut i = low;
    let pivot = arr[high];

    for j in low..high {
        if arr[j] < pivot {
            let temp = arr[i];
            arr[i] = arr[j];
            arr[j] = temp;
            i = i + 1;
        }
    }

    let temp = arr[high];
    arr[high] = arr[i];
    arr[i] = temp;

    i
}

#[cfg(test)]
mod tests {
    use super::*;
    use wasm_bindgen_test::*;

    #[wasm_bindgen_test]
    fn sort_array() {
        let arr = vec![5, 3, 7, 6, 2, 9];
        let result = quicksort_vec(arr);
        let sorted: Vec<i32> = result.into_serde().unwrap();
        assert_eq!(sorted, [2, 3, 5, 6, 7, 9]);
    }
}
