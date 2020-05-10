$(function () {
    let table = null;
    $(document).ready(() => {
        table = $("#files").DataTable({
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
        $("#left-corner-btns").removeClass("hidden").insertBefore("#files_filter");
    });

    $("#refresh-btn").click(() => {
        document.getElementById("rotating").beginElement();
        $.ajax("/files/update").always(() => {
            window.location.reload();
        });
        return false;
    });

    $(".remove-btn").click(function () {
        let filename = $(this).data("filename");
        let that = $(this);
        $.ajax({
            url: `/files/${filename}`,
            type: "DELETE",
        }).done(function () {
            table
                .row(that.parents("tr"))
                .remove()
                .draw(false);  // false means not redirect to the first page
        });
    });
});
