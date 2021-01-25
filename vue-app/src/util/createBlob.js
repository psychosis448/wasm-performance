export const createBlob = (data) => {
    const json = JSON.stringify(data, null, 2);
    const blob = new Blob([json], { type: "application/json" });
    const fileURL = window.URL.createObjectURL(blob);
    const link = document.getElementById("download-button");
    link.href = fileURL;
}