// ==============================
// Backend API URL
// ==============================

// IMPORTANT:
// Change this URL when deploying backend to Render

const API_URL = "http://127.0.0.1:5000/analyze";


// ==============================
// Get DOM Elements
// ==============================

const repoInput = document.getElementById("repoInput");

const analyzeBtn = document.getElementById("analyzeBtn");

const loading = document.getElementById("loading");

const resultsSection = document.getElementById("resultsSection");

const errorMessage = document.getElementById("errorMessage");


// ==============================
// Add Click Event
// ==============================

analyzeBtn.addEventListener(
    "click",
    analyzeRepository
);


// ==============================
// Analyze Repository Function
// ==============================

async function analyzeRepository() {

    // Get repository URL
    const repoUrl = repoInput.value.trim();

    // Validate input
    if (!repoUrl) {

        showError(
            "Please enter GitHub repository URL"
        );

        return;
    }

    // Reset UI
    hideError();

    hideResults();

    showLoading();

    try {

        // Send POST request to backend
        const response = await fetch(API_URL, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                repo_url: repoUrl
            })
        });

        // Convert response to JSON
        const data = await response.json();

        // Check success
        if (!data.success) {

            showError(
                data.message || "Something went wrong"
            );

            hideLoading();

            return;
        }

        // Display repository results
        displayResults(data);

    } catch (error) {

        showError(
            "Unable to connect to backend server"
        );

    } finally {

        hideLoading();
    }
}


// ==============================
// Display Results
// ==============================

function displayResults(data) {

    // Extract repository data
    const repository = data.repository;

    // Extract health report
    const healthReport = data.health_report;

    // Extract AI analysis
    const aiAnalysis = data.ai_analysis;


    // ==============================
    // Repository Metrics
    // ==============================

    document.getElementById("stars").textContent =
        repository.stars;

    document.getElementById("forks").textContent =
        repository.forks;

    document.getElementById("contributors").textContent =
        repository.contributors;

    document.getElementById("issues").textContent =
        repository.open_issues;

    document.getElementById("language").textContent =
        repository.language;

    document.getElementById("releases").textContent =
        repository.releases;
    document.getElementById("readme").textContent =
        repository.has_readme
        ? "Available"
        : "Not Available";

    // ==============================
    // Health Report
    // ==============================

    document.getElementById("activityStatus").textContent =
        healthReport.activity_status;

    document.getElementById("maintenanceStatus").textContent =
        healthReport.maintenance_status;

    document.getElementById("communityStrength").textContent =
        healthReport.community_strength;

    document.getElementById("healthScore").textContent =
        `${healthReport.health_score}/10`;


    // ==============================
    // AI Analysis Formatting
    // ==============================

    const formattedAnalysis = formatMarkdown(
        aiAnalysis.content
    );

    document.getElementById("aiAnalysis").innerHTML =
        formattedAnalysis;


    // Show results section
    resultsSection.classList.remove("hidden");
}


// ==============================
// Simple Markdown Formatter
// ==============================

function formatMarkdown(text) {

    // Convert ### headings
    text = text.replace(
        /^### (.*$)/gim,
        "<h3>$1</h3>"
    );

    // Convert **bold**
    text = text.replace(
        /\*\*(.*?)\*\*/g,
        "<strong>$1</strong>"
    );

    // Convert bullet points
    text = text.replace(
        /^\* (.*$)/gim,
        "<li>$1</li>"
    );

    // Wrap bullet points in ul
    text = text.replace(
        /(<li>.*<\/li>)/gs,
        "<ul>$1</ul>"
    );

    // Convert line breaks
    text = text.replace(/\n/g, "<br>");

    return text;
}


// ==============================
// Show Loading
// ==============================

function showLoading() {

    loading.classList.remove("hidden");
}


// ==============================
// Hide Loading
// ==============================

function hideLoading() {

    loading.classList.add("hidden");
}


// ==============================
// Show Error Message
// ==============================

function showError(message) {

    errorMessage.textContent = message;

    errorMessage.classList.remove("hidden");
}


// ==============================
// Hide Error Message
// ==============================

function hideError() {

    errorMessage.classList.add("hidden");
}


// ==============================
// Hide Results
// ==============================

function hideResults() {

    resultsSection.classList.add("hidden");
}