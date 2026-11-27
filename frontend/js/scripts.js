import {registerUser, loginUser} from "./auth.js";
import {getHackathons, getHackathonDetails} from "./hackathon.js";

getHackathons(); // Fetch and display hackathons on page load
getHackathonDetails(); // Fetch and display hackathon details if on the details page

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

