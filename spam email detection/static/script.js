
function setExample(message) {
    document.getElementById("emailText").value = message;
    document.getElementById("result").style.display = "none";
}

async function checkSpam() {
    const emailText = document.getElementById("emailText").value.trim();
    const result = document.getElementById("result");
    const button = document.getElementById("checkButton");

    if (!emailText) {
        result.className = "error";
        result.textContent = "Please enter an email message.";
        return;
    }

    button.disabled = true;
    button.textContent = "Analyzing...";
    result.className = "";
    result.style.display = "block";
    result.textContent = "Checking your message...";

    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: emailText
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Unable to analyze message.");
        }

        result.className =
            data.prediction === "Spam" ? "spam" : "safe";

        result.textContent =
            "Result: " + data.prediction + ". " + data.message;

    } catch (error) {
        result.className = "error";
        result.textContent = "Error: " + error.message;
    } finally {
        button.disabled = false;
        button.textContent = "Check Email";
    }
}
