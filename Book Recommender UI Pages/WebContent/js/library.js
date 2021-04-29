function registerValidation() {
    var name = document.getElementById("name").value;
    var nameValidation = name.replaceAll(" ", "");
    var dob = document.getElementById("dob").value;
    var flag = true;
    if (/^[a-zA-Z][a-zA-Z\s]*$/.test(name) && nameValidation !== "") {
        document.getElementById("error-name").style.display = "none";
        flag=flag && true;
    }
    else if (nameValidation === "") {
        document.getElementById("error-name").style.display = "block";
        document.getElementById("error-name").innerHTML = "*Name should not be empty";
        flag=flag && false;
    }
    else {
        document.getElementById("error-name").style.display = "block";
        document.getElementById("error-name").innerHTML = "*Name should contain only alphabets and no extra spaces";
        flag=flag && false;
    }
    var myDate = new Date(dob);
    var today = new Date();
    if (myDate > today) {
        document.getElementById("error-dob").style.display = "block";
        document.getElementById("error-dob").innerHTML = "*You cannot enter a date in the future";
        flag=flag && false;
    }
    else {
        document.getElementById("error-dob").style.display = "none";
        flag= flag&& true;
    }

    return flag;
}