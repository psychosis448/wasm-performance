use wasm_bindgen::prelude::*;

#[allow(dead_code)]
fn sum_digits (n: i32) -> i32 {
    let mut sum = 0;
    let mut c = n.abs();
    while c > 0 {
        sum += c % 10;
        c = c / 10;
    }
    sum
}

#[wasm_bindgen]
#[allow(dead_code)]
pub fn fmr_jsval (arr: &JsValue) -> i32 {
    let vec: Vec<i32> = arr.into_serde().unwrap();
    vec.iter()
        .filter(|&x| x % 2 == 0)
        .map(|&x| sum_digits(x))
        .fold(0, |acc, x| acc + x)
}

#[wasm_bindgen]
#[allow(dead_code)]
pub fn fmr (arr: Vec<i32>) -> i32 {
    arr.iter()
        .filter(|&x| x % 2 == 0)
        .map(|&x| sum_digits(x))
        .fold(0, |acc, x| acc + x)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn filter_map_fold() {
        let arr: Vec<i32> = vec![5, 3, 7, 6, -2, 9, 12];
        let res = fmr(arr);
        assert_eq!(res, 11);
    }
}
