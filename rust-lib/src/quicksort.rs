use wasm_bindgen::prelude::*;

#[wasm_bindgen]
#[allow(dead_code)]
pub fn quicksort(arr: &mut [i32]) -> () {
    qs(arr, 0, arr.len() - 1)
}

fn qs(arr: &mut [i32], low: usize, high: usize) -> () {
    if low < high {
        let p = partition(arr, low, high);
        if p > 0 {
            qs(arr, low, p - 1);
        }
        qs(arr, p + 1, high);
    }
}

fn partition(arr: &mut [i32], low: usize, high: usize) -> usize {
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
        let mut arr: [i32; 6] = [5, 3, 7, 6, 2, 9];
        quicksort(&mut arr);
        assert_eq!(arr, [2, 3, 5, 6, 7, 9]);
    }
}
