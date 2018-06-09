$(function() {
    var button_pressed = 0;
    $("#search-query-button").click(function() {
        if (button_pressed === 1) {
            console.log("Query in progress, please wait!");
            return;
        }
        $("#search-output-message").html("Query in progress...");
        var endpoint = "tweet_search" + "/" + $("#search-query").val() + "/" + $("#search-number").val();
        button_pressed = 1;
        $.get(endpoint, function(data) {
            button_pressed = 0;
            $("#search-output-message").html("Done!");

            // write out in format
            html = "";
            for (var i = 0; i < data.length; i++) {
                entry = data[i];
                html += "<p>";
                html += entry["text"];
                html += "</p>";
                html += "<p>";
                html += entry["retweets"];
                html += "</p>";
            }
            $("#output-left").html(html);
        });
    });
});