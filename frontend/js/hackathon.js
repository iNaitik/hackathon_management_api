import {BASE_URL} from "./config.js";

export async function getHackathons(){

    const statusMessage = document.getElementById("statusMessage");
    const hackathonList = document.getElementById("hackathonList");

    if (!hackathonList) {
        return;
    }

    const token = localStorage.getItem("access_token");
    if (!token) {
        statusMessage.textContent = "Please log in to view hackathons.";
        return;
    }
    try{
        const response = await fetch(`${BASE_URL}/hackathons`, {
            method : "GET",
            headers : {
                "Authorization" : `Bearer ${token}`
            }
        });

        if (response.status === 401 || response.status === 403) {
            if (statusMessage) statusMessage.textContent = "Your session has expired. Please log in again.";
            return;
        }

        if (!response.ok) {
            if (statusMessage) statusMessage.textContent = "Failed to fetch hackathons. Please try again later.";
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const hackathons = await response.json();

        displayHackathons(hackathons);
    } catch (error) {
        console.error("Error fetching hackathons:", error);
        if (statusMessage) statusMessage.textContent = "An error occurred while fetching hackathons. Please try again later.";
    }
}

function displayHackathons(hackathons){
    const hackathonList = document.getElementById("hackathonList");
    if (!hackathonList) return;
    hackathonList.innerHTML = ""; // Clear existing content

    hackathons.forEach(hackathon => {
        const hackathonCard = document.createElement("article");
        hackathonCard.classList.add("hackathon-card");
        hackathonCard.innerHTML = `
            <div class="hackathon-card-header">
                <div>
                    <h2 href="">${hackathon.title}</h2>
                    <p>${hackathon.description}</p>
                </div>
                <span class="hackathon-card-id">Coming soon</span>
            </div>
            <div class="hackathon-card-meta">
                <span>Date: ${hackathon.created_at}</span>
            </div>
        `;
        hackathonCard.addEventListener("click", function() {
            const hackathonId = hackathon.id;
            window.location.href = `hackathon-details.html?id=${hackathonId}`;
        });
        
        document.getElementById("hackathonList").appendChild(hackathonCard);
        
    });
}

export async function getHackathonDetails() {
    const param = new URLSearchParams(window.location.search);
    const hackathonId = param.get("id");
    const statusMessage = document.getElementById("statusMessage");

    if (!hackathonId) {
        if (statusMessage) statusMessage.textContent = "Hackathon ID is missing in the URL.";
        return;
    }

    const token = localStorage.getItem("access_token");
    if (!token) {
        if (statusMessage) statusMessage.textContent = "Please log in to view hackathon details.";
        return;
    }

    try{
        const response = await fetch(`${BASE_URL}/hackathons/${hackathonId}`, {
            method : "GET",
            headers : {
                "Authorization" : `Bearer ${token}`
            }
        });

        if (response.status === 401 || response.status === 403) {
            alert("Your session has expired. Please log in again.");
            window.location.href = "./login.html";
            return;
        }

        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }

        const hackathon = await response.json();
        displayHackathonDetails(hackathon);
    } catch (error) {
        console.error("Error fetching hackathon details:", error);
        if (statusMessage) statusMessage.textContent = "An error occurred while fetching hackathon details. Please try again later.";
    }
}

function displayHackathonDetails(hackathon) {
    const title = hackathon.title || "Untitled hackathon";
    const description = hackathon.description || "No description has been provided.";
    const createdAt = hackathon.created_at ? new Date(hackathon.created_at) : null;
    const createdLabel = createdAt && !Number.isNaN(createdAt.getTime())
        ? createdAt.toLocaleDateString(undefined, { year: "numeric", month: "long", day: "numeric" })
        : "Not specified";

    document.title = `${title} - Hackathon Details`;
    document.getElementById("hackathonTitle").textContent = title;
    document.getElementById("hackathonDescription").textContent = description;
    document.getElementById("hackathonChallenge").textContent = description;
    document.getElementById("hackathonEyebrow").textContent =
        `HACKATHON · #${hackathon.id}`;
    document.getElementById("hackathonDates").textContent = createdLabel;
    document.getElementById("hackathonLocation").textContent =
        hackathon.location || "Not specified";
    document.getElementById("hackathonTeamSize").textContent =
        hackathon.team_size ? `${hackathon.team_size} people` : "Not specified";
    document.getElementById("hackathonCreatedBy").textContent =
        hackathon.created_by ? `User #${hackathon.created_by}` : "Not specified";

    const createdTime = document.getElementById("hackathonCreatedTime");
    if (createdTime) {
        createdTime.textContent = createdAt && !Number.isNaN(createdAt.getTime())
            ? createdAt.toLocaleDateString(undefined, { month: "short", day: "numeric" })
            : "--";
        if (createdAt && !Number.isNaN(createdAt.getTime())) {
            createdTime.dateTime = createdAt.toISOString();
        }
    }
}
