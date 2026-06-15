$(document).ready(function () {

    var albums = $(".album");

    $("#search").keyup(function () {

        var searchTerm = $(this).val().toLowerCase();

        albums.each(function () {

            var text = $(this).text().toLowerCase();

            if (text.indexOf(searchTerm) === -1) {
                $(this).hide();
            } else {
                $(this).show();
            }

        });

    });

});