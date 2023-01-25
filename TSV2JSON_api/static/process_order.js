var submitButton = document.getElementById("submit-button");
var modal = document.getElementById("my-modal");
var tsvData = document.getElementById("tsv_data");
let form = document.getElementById("tsv-form");


submitButton.addEventListener("click", function (event) {
    event.preventDefault();
    let textInput = document.getElementById("tsv-form").id_tsv_data;
    tsvData.value = textInput.value;

    let formData = new FormData();
    formData.append('tsv_data', 'Data');
    document.getElementById("tsv-form").submit();
});

form.addEventListener("input", () => {
    let textInput = document.getElementById("tsv-form").id_tsv_data;
    tsvData.value = textInput.value;

    if (tsvData.value !== "") {
        submitButton.innerText = "Submit"
        submitButton.disabled = false
    } else {
        submitButton.innerText = "Enter Valid Data"
    }
})


