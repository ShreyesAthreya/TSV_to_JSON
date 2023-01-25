let modal = document.getElementById("my-modal");
let closeButton = document.getElementsByClassName("close-button")[0];
let copyButton = document.getElementById("copy-button");

closeButton.addEventListener("click", function () {
    window.location.replace("http://localhost:8000/process_orders/");
});

copyButton.addEventListener("click", function () {
    let id = document.getElementById("record_id").value;
    let copyURL = "http://localhost:8000/get_orders/" + id
    navigator.clipboard.writeText(copyURL).then(function () {
        console.log('Copying to clipboard was successful!');
    }, function (err) {
        console.error('Failed to copy: ', err);
    });

    copyButton.innerHTML = "Copied";
    // Use setTimeout to switch the text back to "copy" after 3 seconds
    setTimeout(function () {
        copyButton.innerHTML = "Copy";
    }, 3000);
});

