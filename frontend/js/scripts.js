import {registerUser, loginUser} from "./auth.js";
import {getHackathons, getHackathonDetails, registerForHackathon, checkRegistration} from "./hackathon.js";


const registerForm = document.getElementById("registerForm");
if (registerForm) {
    registerForm.addEventListener("submit", async function(event) {
        event.preventDefault();
        await registerUser();
    });
}

const loginForm = document.getElementById("loginForm");
if (loginForm) {
    loginForm.addEventListener("submit", async function(event) {
        event.preventDefault();
        await loginUser();
    });
}


// Hackathon listing page
if (document.getElementById("hackathonList")) {
    getHackathons();
}

// Hackathon details page
if (document.getElementById("hackathonTitle")) {
    const hackathonId = new URLSearchParams(window.location.search).get("id");

    getHackathonDetails();

    if (hackathonId) {
        checkRegistration(hackathonId);
    }

    const registerButton = document.getElementById("registerButton");

    if (registerButton) {
        registerButton.addEventListener("click", async function() {
            await registerForHackathon(hackathonId);
        });
    }
}
