
function toggleFields() {
    const userType = document.getElementById("userType").value;
    document.getElementById("individual-fields").style.display = userType === "individual" ? "block" : "none";
    document.getElementById("organization-fields").style.display = userType === "organization" ? "block" : "none";
}
