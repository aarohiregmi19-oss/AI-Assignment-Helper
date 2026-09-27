async function generateAssignment() {
    const topic = document.getElementById("topic").value.trim();
    const subject = document.getElementById("subject").value.trim();
    const assignmentType = document.getElementById("assignment_type").value;
    const length = document.getElementById("length").value;

    const result = document.getElementById("result");
    const loading = document.getElementById("loading");
    const button = document.getElementById("generateBtn");

    // Check topic
    if (!topic) {
        result.textContent = "⚠️ Please enter an assignment topic.";
        return;
    }

    // Show loading
    loading.style.display = "block";
    result.textContent = "";
    button.disabled = true;
    button.textContent = "⏳ Generating...";

    try {
        const response = await fetch("/generate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                topic: topic,
                subject: subject,
                assignment_type: assignmentType,
                length: length
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Something went wrong.");
        }

        result.textContent = data.assignment;

    } catch (error) {
        console.error("Error:", error);

        result.textContent =
            "❌ Unable to generate the assignment.\n\n" +
            "Error: " + error.message;

    } finally {
        loading.style.display = "none";
        button.disabled = false;
        button.textContent = "✨ Generate Assignment";
    }
}