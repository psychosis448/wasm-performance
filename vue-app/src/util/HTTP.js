import axios from 'axios'

export default axios.create({
    // baseURL: "http://localhost:8081"
    baseURL: window.location.origin
    // baseURL: "https://benchmark-data.herokuapp.com"
})