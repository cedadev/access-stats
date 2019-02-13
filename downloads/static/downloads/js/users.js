$("#users-message").html(loadingHTML);
$.get(
{
    url: window.location.origin + window.location.pathname + "json/" + "users-limited" + window.location.search,
    success: function (data) {
        renderUsersPage(data);
        if(data.totals.users > 500)
        {
            var html = Mustache.render(templates.warningMessage, {analysis_method:"Users", total:data.totals.users, allFunction:"usersGetAll()"});
            $("#users-message").html(html);
        }
        else
        {
            $("#users-message").hide();
        }
    }
})

function usersGetAll()
{
    $("#users-message").html(loadingHTML);
    $.get(
    {
        url: window.location.origin + window.location.pathname + "json/" + "users" + window.location.search,
        success: function (data) {
            renderUsersPage(data);
            $("#users-message").hide();
        },
        error: function () {
            var html = Mustache.render(templates.errorMessage);
            $("#users-message").html(html);
        }
    })
}

function renderUsersPage(data)
{
    var html;
    for (var user in data.results)
    {
        html += Mustache.render(templates.usersTableBody, {user:user, country:data.results[user].country, institute:data.results[user].institute_type, field:data.results[user].field, methods:data.results[user].methods, datasets:data.results[user].datasets, accesses:data.results[user].accesses, size:formatBytes(data.results[user].size), activitydays:data.results[user].activitydays});
    }
    $("#usersTableBody").html(html);
    html = Mustache.render(templates.usersTableFooter, {totals:"Totals", country:"-", institute:"-", field:"-", methods:data.totals.methods, datasets:data.totals.datasets, accesses:data.totals.accesses, size:formatBytes(data.totals.size), activitydays:data.totals.activitydays});
    $("#usersTableFooter").html(html);
}
