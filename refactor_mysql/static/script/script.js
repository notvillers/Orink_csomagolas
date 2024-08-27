console.log("Octopy is ready to serve :)");

/* index.html */
function changeWorkState(workState) {
    window.location.href = "/work_state/" + workState;
}

function deletePackage(package_id) {
    window.location.href = "/delete/" + package_id;
}

/* delete.html */
function deletePackageConfirmed(package_id) {
    window.location.href = "/delete_confirm/" + package_id;
}

function goHome() {
    window.location.href = "/";
}

function goUsers() {
    window.location.href = "/users";
}

/* users.html */
function switchUser(id) {
    window.location.href = "/switch_user/" + id;
}