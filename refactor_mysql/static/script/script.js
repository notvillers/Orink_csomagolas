console.log("Octopy is ready to serve :)");

/* index.html */
function changeWorkState(workState) {
    window.location.href = "/";
}

function editPackage(package_no) {
    window.location.href = "/edit/" + package_no;
}

function deletePackage(package_no) {
    window.location.href = "/delete/" + package_no;
}