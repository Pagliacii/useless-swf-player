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

$("#file_uploads").on("change", function () {
    const selected = $("div.selected");
    selected.empty();

    const curr_files = this.files;
    if (curr_files.length == 0) {
        selected.append($("<p>No files currently selected for upload</p>"));
    } else {
        const list = $("<ol></ol>");
        selected.append(list);

        for (const file of curr_files) {
            const item = $("<li></li>");
            const para = $(`<p class="border border-gray-400"></p>`);
            if (validate(file)) {
                para.text(`File name ${file.name}, file size ${get_size(file.size)}.`);
            } else {
                para.text(`File name ${file.name}: Not a valid file type. Update your selection.`);
            }
            item.append(para);
            list.append(item);
        }
    }
});

const file_types = [
    "application/x-shockwave-flash"
];

function validate(file) {
    return file_types.includes(file.type);
}

function get_size(bytes) {
    const kilobyte = 1024;
    const megabyte = 1024 * 1024;
    if (bytes < kilobyte) {
        return bytes + 'bytes';
    } else if (bytes >= kilobyte && bytes < megabyte) {
        return (bytes / kilobyte).toFixed(1) + 'KB';
    } else if (bytes >= megabyte && bytes < 500 * megabyte) {
        return (bytes / megabyte).toFixed(1) + 'MB';
    } else {
        return "Filesize exceeded maximum limit";
    }
}
