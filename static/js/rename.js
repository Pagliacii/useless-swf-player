$(function () {
    /* Rename modal */

    $(".rename-btn").click(function (event) {
        event.preventDefault();
        this.blur();
        let filename = $(this).data("filename");
        $("#rename-modal-body")
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
        $("#rename-submit-btn").removeClass("btn-primary").addClass("btn-primary-disabled");
        $("#rename-modal-body").empty();
    });

    $(document).on("input", "#filename", function (event) {
        let old_name = $(this).data("srcname");
        let new_name = $(this).val();
        let warning_class = "bg-red-600 text-gray-900 font-bold";
        let max_length = $("#max-length");
        let reserved_chars = $("#reserved-chars");
        let is_warning = false;

        max_length.removeClass(warning_class);
        reserved_chars.removeClass(warning_class);

        if (new_name.length > 256) {
            is_warning = true;
            max_length.addClass(warning_class);
        }

        if (/.*?[\\|/|:|\*|\?|"|<|>|\|].*?/gm.test(new_name)) {
            is_warning = false;
            reserved_chars.addClass(warning_class);
        }

        let submit = $("#rename-submit-btn");
        let enabled_class = "btn-primary";
        let disabled_class = "btn-primary-disabled";
        if (is_warning || !new_name.endsWith(".swf") || new_name.length == 0 || new_name == old_name) {
            submit.removeClass(enabled_class).addClass(disabled_class);
        } else {
            submit.removeClass(disabled_class).addClass(enabled_class);
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
            let message = $("#rename-modal-head > h2");
            message.hasClass("text-red-600") || message.addClass("text-red-600");
            message.text(resp.reason);
        });
    });
});