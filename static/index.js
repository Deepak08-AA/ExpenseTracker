const card = document.querySelector(".card-inner");

const signup = document.getElementById("signup-link");
const login = document.getElementById("login-link");

signup.addEventListener("click", function(e){
    e.preventDefault();
    card.classList.add("flip");
});

login.addEventListener("click", function(e){
    e.preventDefault();
    card.classList.remove("flip");
});

const params = new URLSearchParams(window.location.search);

if (params.get("form") === "signup") {
    card.classList.add("flip");
}