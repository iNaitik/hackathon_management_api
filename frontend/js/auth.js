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

export async function loginUser() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const formData = new URLSearchParams();

    formData.append("username", email);
    formData.append("password", password);

    try {
        const response = await fetch(`${BASE_URL}/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            console.log("Login successful:", data);
            
            const token = data.access_token; // Assuming the token is returned in the response
            localStorage.setItem("access_token", token); // Store the token in localStorage
            window.location.href = "./index.html"; // Redirect to the dashboard or another page
        
        } else {
            alert("Login failed. Check your credentials.");
        }

    } catch (error) {
        console.error("Login error:", error);
    }
}