let reg_form = document.querySelector(".form-reg");
let reg = document.querySelector(".span-reg");
let login_form = document.querySelector(".form-login");
let login = document.querySelector(".login");

reg.onclick = () => {
    if(reg_form.style.top == "-17rem" && login_form.style.top == "-16rem") {
        reg_form.style.top = "3.2rem";
        reg.style.backgroundColor = "#1e3799";
        reg.style.boxShadow = "0px 8px 16px 0px rgba(0,0,0,0.2)";
        // reg.style.fontSize = "1.4rem";
    } else {
        reg_form.style.top = "-17rem";
        // reg.style.fontSize = "1rem";
    }
}

reg_form.onmouseleave = () => {
    reg_form.style.top = "-17rem";
    reg.style.fontSize = "1rem";
}

login.onclick = () => {
    if(login_form.style.top == "-16rem" && reg_form.style.top == "-17rem") {
        login_form.style.top = "3.2rem";
        login.style.backgroundColor = "#1e3799";
        login.style.boxShadow = "0px 8px 16px 0px rgba(0,0,0,0.2)";
        // login.style.fontSize = "1.4rem";
    } else {
        login_form.style.top = "-16rem";
        // login.style.fontSize = "1rem";
    }
}

login_form.onmouseleave = () => {
    login_form.style.top = "-16rem";
    // login.style.fontSize = "1rem";
}