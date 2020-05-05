$(document).ready(() => {
    $("#files").DataTable({
        "columnDefs": [{
            "targets": 4,
            "orderable": false,
            "searchable": false,
        }],
        "lengthChange": false,
        "pagingType": "numbers",
        "pageLength": 10,
        "stripeClasses": ["stripe1", "stripe2"],
    });
});

$("#refresh-btn").click(() => {
    document.getElementById("rotating").beginElement();
    $.ajax("/files/all?update").always(() => {
        window.location.reload();
    });
    return false;
});

$(".rename-btn").click(function (event) {
    event.preventDefault();
    this.blur();
    let filename = $(this).data("filename");
    $("#modal-body")
        .append($(`<label for="filename" class="flex items-center font-semibold">${filename} <svg class="mx-2 h-6 w-6" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M10 7H2v6h8v5l8-8-8-8v5z"/></svg></label>`))
        .append($(`<input class="flex-grow" type="text" id="filename" name="filename" value="${filename}" required data-srcname="${filename}">`));
    $("#rename-modal").modal({
        fadeDuration: 100,
        showClose: false,
    });
    return false;
});

$("#rename-modal").on("modal:close", function () {
    $(this).hide();
    $("#modal-body").empty();
});

$(".remove-btn").click(function () {
    let filename = $(this).data("filename");
    $.ajax({
        url: `/files/${filename}`,
        type: "DELETE",
    }).always(() => {
        window.location.reload(true);
    });
});

$(document).on("input", "#filename", function (event) {
    let old_name = $(this).data("srcname");
    let new_name = $(this).val();
    let warning_class = "bg-red-600 text-gray-900 font-bold";
    let max_length = $("#max-length");
    let reserved_chars = $("#reserved-chars");

    max_length.removeClass(warning_class);
    reserved_chars.removeClass(warning_class);

    if (new_name.length > 256) {
        max_length.addClass(warning_class);
    }

    if (/.*?[\\|/|:|\*|\?|"|<|>|\|].*?/gm.test(new_name)) {
        reserved_chars.addClass(warning_class);
    }

    let submit = $("#submit-btn");
    let enabled_class = "btn-primary";
    let disabled_class = "btn-primary-disabled";
    if (!(max_length.hasClass(warning_class) || reserved_chars.hasClass(warning_class)) && new_name.length != 0 && new_name != old_name) {
        submit.hasClass(disabled_class) && submit.removeClass(disabled_class);
        submit.hasClass(enabled_class) || submit.addClass(enabled_class);
    } else {
        submit.hasClass(enabled_class) && submit.removeClass(enabled_class);
        submit.hasClass(disabled_class) || submit.addClass(disabled_class);
    }
});

$(document).on("submit", "#rename-form", function (event) {
    event.preventDefault(); // avoid to execute the actual submit of the form

    console.log($(this).serialize());
    $.post(
        `/files/${$("#filename").data("srcname")}`,
        $(this).serialize(),
    ).done(() => {
        $.modal.close();
        window.location.reload(true);
    }).fail(function (response) {
        let resp = JSON.parse(response.responseText);
        let message = $("#modal-head > h2");
        message.hasClass("text-red-600") || message.addClass("text-red-600");
        message.text(resp.reason);
    });
});