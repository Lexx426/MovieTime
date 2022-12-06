var signup = document.querySelector(".signup");
var login = document.querySelector(".login");
var slider = document.querySelector(".slider");
var formSection = document.querySelector(".form-section");

login.addEventListener("click", () =>{
    slider.classList.add("moveslider");
    formSection.classList.add("form-section-move");
}
);


signup.addEventListener("click", () =>{
    slider.classList.remove("moveslider");
    formSection.classList.remove("form-section-move");
});