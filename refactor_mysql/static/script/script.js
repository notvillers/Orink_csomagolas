console.log("Octopy is ready to serve :)");

/* index.html */
function checkPackage() {
    window.location.href = "/o8_check/";
}

function editPackage(package_no) {
    window.location.href = "/edit/" + package_no;
}

function deletePackage(package_no) {
    window.location.href = "/delete/" + package_no;
}