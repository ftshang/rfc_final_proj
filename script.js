function generateFields() {
    const fieldCount = document.getElementById("fieldCount").value;
    const inputContainer = document.getElementById("inputContainer");

    // Clear existing fields
    inputContainer.innerHTML = "";

    // Validate the entered number
    if (fieldCount && fieldCount > 0 && !isNaN(fieldCount)) {
        for (let i = 0; i < fieldCount; i += 1) {
            const newLabel = document.createElement("label");
            newLabel.for = `section-${i + 1}`
            newLabel.innerText = `Section ${i + 1}:`
            const newInput = document.createElement("input");
            newInput.id = `section-${i + 1}`;
            newInput.type = "text";
            newInput.placeholder = `Enter text field for section ${i + 1}`;
            newInput.className = "dynamic-input";
            inputContainer.appendChild(newLabel);
            inputContainer.appendChild(newInput);
        }
    }
}

function generateFiles() {
    const fileCount = document.getElementById("fileCount").value;
    const fileContainer = document.getElementById("fileContainer");

    fileContainer.innerHTML = "";

    if (fileCount && fileCount > 0 && !isNaN(fileCount)) {
        for (let i = 0; i < fileCount; i += 1) {
            const newLabel = document.createElement("label");
            newLabel.innerText = `Image ${i + 1}:`
            newLabel.for = `file-${i + 1}`;
            const newFileInput = document.createElement("input");
            newFileInput.type = "file";
            newFileInput.id = `file-${i + 1}`;
            newFileInput.className = "dynamic-input";
            const newLine = document.createElement("br")
            fileContainer.appendChild(newLabel);
            fileContainer.appendChild(newFileInput);
            fileContainer.appendChild(newLine);
        }
    }
}

// Generate fields when input changes
document.getElementById("fieldCount").addEventListener("input", generateFields)
document.getElementById("fileCount").addEventListener("input", generateFiles)

async function getResponse() {
    const rfcNumber = document.getElementById("rfcNumber").value;

    const numSections = document.getElementById("fieldCount").value;
    const numFiles = document.getElementById("fileCount").value;

    const sectionList = []
    for (let i = 0; i < numSections; i += 1) {
        sectionList.push(document.getElementById(`section-${i + 1}`).value);
    }

    const fileList = []
    for (let i = 0; i < numFiles; i += 1) {
        fileList.push(document.getElementById(`file-${i + 1}`).files[0].name);
    }

    const responseDiv = document.getElementById("response");

    if (!prompt) {
        responseDiv.innerHTML = "Please enter a prompt.";
        return;
    }

    responseDiv.innerHTML = "Loading...";

    try {
        const response = await fetch("http://localhost:5000/generate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                rfcNumber: rfcNumber,
                sections: sectionList,
                files: fileList
            })
        });

        if (response.ok) {
            const data = await response.json();
            responseDiv.innerHTML = `<pre>${data.response}</pre>`;
        } else {
            responseDiv.innerHTML = "Error: Unable to fetch response.";
        }
    } catch (error) {
        responseDiv.innerHTML = "Error: " + error.message;
    }
}
