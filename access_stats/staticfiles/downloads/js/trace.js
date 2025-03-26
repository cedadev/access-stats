$("#trace-message").html(loadingHTML);
$.get(
{
    url: window.location.origin + window.location.pathname + "json/" + "trace" + window.location.search,
    success: function (data) {
        renderTracePage(data);
        $("#trace-message").hide();
    }
})

function renderTracePage(data)
{
    var html = "";
    for (var i = 0; i < data.logs.length; i++)
    {
        html += Mustache.render(templates.traceTableBody, {log:data.logs[i]});
    }
    $("#traceTableBody").html(html);
}
