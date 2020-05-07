/* Upload modal */

$("#upload-btn").on("click", function (event) {
    event.preventDefault();
    this.blur();
    $("#upload-modal").modal({
        fadeDuration: 100,
        showClose: false,
    });
    return false;
});

$("#upload-modal").on("modal:close", function () {
    this.hide();
});