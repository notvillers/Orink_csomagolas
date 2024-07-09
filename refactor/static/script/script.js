console.log("Octopy is ready to serve :)");

/* index.html */
function editPackage(id) {
    window.location.href = "/edit/" + id;
}

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