$(function () {
    /* Upload modal */
    const modal = $("#upload-modal");
    const modal_btn = $("#upload-btn");
    const input = $("#file_uploads");
    const selected = $("div.selected");
    const upload_btn = $("#upload-upload-btn");
    const loading_btn = $("#upload-loading-btn");
    const placeholder = $("<p>No files currently selected for upload</p>");

    function reset() {
        selected.empty();
        selected.append(placeholder);

        upload_btn.removeClass("btn-primary");
        upload_btn.addClass("btn-primary-disabled");
        upload_btn.prop("disabled", true);
        upload_btn.show();

        loading_btn.hide();
        loading_btn.addClass("hidden");

        // enable the input during upload
        input.prop("disabled", false);
        input.closest("div").children("label").removeClass("cursor-not-allowed");
        input.val(null);
    }

    modal_btn.on("click", function (event) {
        event.preventDefault();
        this.blur();
        modal.modal({
            fadeDuration: 100,
            showClose: false,
        });
        return false;
    });

    input.fileupload({
        dataType: "json",
        autoUpload: false,
        add: function (event, data) {
            let file = data.files[0];
            if (!valid_file_type(file)) {
                data.context = $('<p class="file"></p>')
                    .text(`File name ${file.name}: Not a valid file type. Update your selection.`)
                    .appendTo(selected);
            } else if (!valid_file_size(file.size)) {
                data.context = $('<p class="file"></p>')
                    .text(`File name ${file.name}: File size exceeded maximum limit. Update your selection.`)
                    .appendTo(selected);
            } else {
                let that = $(`<div id="${file.name.replace('.swf', '').replace(' ', '-')}"></div>`)
                    .addClass("file flex w-full h-8 border border-gray-400");
                data.context = that.append($(`<p class="flex-grow"></p>`).text(`File name: ${file.name}, file size: ${format_size(file.size)}`))
                    .append($('<a class="start-upload opacity-0 h-0 w-0"></a>').on("click", () => {
                        document.cookie = `filesize=${file.size}`;
                        data.submit();
                    }))
                    .append($('<a class="float-right">&times;</a>').on("click", () => {
                        data.abort();
                        that.remove();
                        if (selected.children().length == 0) {
                            selected.empty();
                            selected.append(placeholder);
                        }
                    }))
                    .appendTo(selected);
            }
        },
        progress: function (event, data) {
            let progress = parseInt((data.loaded / data.total) * 100, 10);
            let file_id = data.files[0].name.replace(".swf", "").replace(" ", "-");
            $(`#${file_id}`).css("background-position-x", 100 - progress + "%");
        },
        done: function (event, data) {
            let file_id = data.files[0].name.replace(".swf", "").replace(" ", "-");
            $(`#${file_id}`).addClass("done");
        },
        fail: function (event, data) {
            if (data.errorThrown === 'abort') {
                console.log("File upload has been canceled");
            }
            data.context.addClass("fail");
        },
        change: function (event, data) {
            selected.empty();
            if (data.files.filter(file => !(valid_file_type(file) && valid_file_size(file.size))).length == 0) {
                upload_btn.prop("disabled", false);
                upload_btn.removeClass("btn-primary-disabled");
                upload_btn.addClass("btn-primary");
            } else {
                upload_btn.prop("disabled", true);
                upload_btn.removeClass("btn-primary");
                upload_btn.addClass("btn-primary-disabled");
            }
        },
        start: function (event) {
            // Disable the input during upload
            input.prop("disabled", true);
            input.closest("div").children("label").addClass("cursor-not-allowed");
            // Hide the upload button
            upload_btn.hide();
            // Display the loading button
            loading_btn.removeClass("hidden");
            loading_btn.show();
        },
        stop: function (event) {
            upload_btn.removeClass("btn-primary");
            upload_btn.addClass("btn-primary-disabled");
            upload_btn.prop("disabled", true);
            upload_btn.show();

            loading_btn.hide();
            loading_btn.addClass("hidden");

            // enable the input during upload
            input.prop("disabled", false);
            input.closest("div").children("label").removeClass("cursor-not-allowed");
            input.val(null);
        }
    });

    modal.on("modal:close", function () {
        $(this).hide();
        reset();
    });

    upload_btn.on("click", event => {
        event.preventDefault();
        $("a.start-upload").click();
    });

    const file_types = [
        "application/x-shockwave-flash"
    ];

    function valid_file_type(file) {
        return file_types.includes(file.type);
    }

    function valid_file_size(size) {
        return size <= (500 * 1024 * 1024) && size > 0;
    }

    function format_size(bytes) {
        const kilobyte = 1024;
        const megabyte = 1024 * 1024;
        if (bytes < kilobyte) {
            return bytes + 'bytes';
        } else if (bytes >= kilobyte && bytes < megabyte) {
            return (bytes / kilobyte).toFixed(1) + 'KB';
        } else if (bytes >= megabyte) {
            return (bytes / megabyte).toFixed(1) + 'MB';
        }
    }
});