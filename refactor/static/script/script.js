console.log("Octopy is ready to serve :)");

/* index.html */
function changeUserRedirect() {
    window.location.href = "/change_user";
}

function uploadDataRedirect() {
    window.location.href = "/";
}

/* change_user.html */
function changeUser(usercode) {
    window.location.href = "/change_user/" + usercode;
}