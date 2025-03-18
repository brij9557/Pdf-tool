function uploadFile(action) {
    let fileInput = document.getElementById("fileInput");
    fileInput.click();

    fileInput.onchange = function () {
        let files = fileInput.files;
        if (files.length === 0) return;

        let formData = new FormData();

        if (action === "merge") {
            for (let i = 0; i < files.length; i++) {
                formData.append("files", files[i]);
            }
        } else {
            formData.append("file", files[0]);
        }

        let endpoint = "";
        if (action === "excel") {
            endpoint = "/pdf-to-excel";
        } else if (action === "word") {
            endpoint = "/pdf-to-word";
        } else if (action === "merge") {
            endpoint = "/merge-pdf";
        }

        fetch(endpoint, {
            method: "POST",
            body: formData,
        })
        .then(response => response.blob())
        .then(blob => {
            let url = window.URL.createObjectURL(blob);
            let a = document.createElement("a");
            a.href = url;
            a.download = action === "merge" ? "merged.pdf" : files[0].name.replace(".pdf", action === "word" ? ".docx" : ".xlsx");
            a.click();
        })
        .catch(error => console.error("Error:", error));
    };
}
