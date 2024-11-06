function showPreloader() {
    document.querySelector(".container-loader").style.display = "block";
    document.querySelector("#whiteScreen").style.display = "block";
}

function hidePreloader() {
    document.querySelector(".container-loader").style.display = "none";
    document.querySelector("#whiteScreen").style.display = "none";

}

function performOperation() {
    showPreloader();
    setTimeout(() => {
        hidePreloader();
    }, 500);
}

window.addEventListener("load", () => {
    performOperation();
});