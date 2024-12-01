async function getResponse() {
    const rfcNumber = document.getElementById("rfcNumber").value;
    const terminology = document.getElementById("terminology").value;
    const overview = document.getElementById("overview").value;
    const specification = document.getElementById("specification");
    const stateFileName = document.getElementById("stateDiagram1").files[0].name;
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
                terminology: terminology,
                overview: overview,
                specification: specification,
                stateDiagram: stateFileName,
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
