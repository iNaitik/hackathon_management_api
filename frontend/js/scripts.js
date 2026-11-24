import {registerUser} from "./auth.js";

const primaryButton = document.getElementsByClassName("primary-button");
primaryButton[0].addEventListener("click", async function(event) {
    console.log("Primary button clicked");
    event.preventDefault(); // Prevent the default form submission which would reload the page
    console.log("Calling registerUser function");
    await registerUser(); // Call the registerUser function
});