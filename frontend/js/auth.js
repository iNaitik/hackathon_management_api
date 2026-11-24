import { BASE_URL } from "./config.js";

export async function registerUser() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try{
        const response = await fetch(`${BASE_URL}/register`, {
            method : "POST",
            headers : {
                "Content-Type" : "application/json"
            },
            body : JSON.stringify({ email, password })
    });
    const data = await response.json();
    console.log("Registration response:", data);
        if (response.ok) {
            alert("Registration successful! Please log in.");
            window.location.href = "./login.html";
        } else {
            alert("Registration failed. Please try again.");
        }
    } catch (error) {
        console.error("Error during registration:", error);
        alert("An error occurred. Please try again.");
    }
}
