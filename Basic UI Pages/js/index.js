function displayGender(gender) {
    document.getElementById("p-gender").innerText = gender + " is selected";
    document.getElementById("p-gender").style.color = "white";
    let backgroundColor = "#292b2c"
    if (gender === "Male") {
        backgroundColor = "#0275d8";
    } else if (gender === "Female") {
        backgroundColor = "#d9534f";
    }
    document.getElementById("p-gender").style.background = backgroundColor;
}

// reset the custom gender form-input
function resetForm() {
    document.getElementById("p-gender").innerText = "Select your gender";
    document.getElementById("p-gender").style.color = "black";
    document.getElementById("p-gender").style.background = "white";
}

// select course functionality
function selectCourse(id) {
    checkStatus = document.getElementById(id).checked
    id = "card-" + id;
    if (checkStatus) {
        document.getElementById(id).style.border = "3px solid purple";
        return;
    }
    document.getElementById(id).style.borderStyle = "none";
}

// at least 1 course should be selected to proceed
function submitCourses() {
    let res = $("input[type=checkbox]:checked").length;
    if (res == 0) {
        alert("No courses selected! Select at least one course to proceed");
        return;
    }
    alert(res + " course(s) successfully submitted!");
}

// check for gender validation
function submitForm() {
    let res = $("input[type=radio]:checked").length;
    if (res == 0) {
        alert("Gender not selected");
    }
}

// reset the selected courses
function resetCourses() {
    $(".card").css("border-style", "none");
    $('input[type=checkbox]').prop('checked', false);

}

// search box-functionalities will go here
function searchItem() {
    alert("Put search functionality here");
}