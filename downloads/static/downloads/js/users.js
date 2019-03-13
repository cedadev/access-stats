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
    var dataList = [];

    for (var user in data.results)
    {
        var row = [];

        row.push(user);
        row.push(data.results[user].country);
        row.push(data.results[user].institute_type);
        row.push(data.results[user].field);
        row.push(data.results[user].methods);
        row.push(data.results[user].datasets);
        row.push(data.results[user].accesses);
        row.push(formatBytes(data.results[user].size));
        row.push(data.results[user].activitydays);

        dataList.push(row);
         //institute:, field:, methods:, datasets:, accesses:, size:, activitydays:});
    }

    totals = Mustache.render(templates.usersTableTotals, {totals:"Totals", country:"-", institute:"-", field:"-", methods:data.totals.methods, datasets:data.totals.datasets, accesses:data.totals.accesses, size:formatBytes(data.totals.size), activitydays:data.totals.activitydays});
    
    $("#usersTable").DataTable({
        data: dataList,
        columns: [
            { title: "User" },
            { title: "Country" },
            { title: "Institute type" },
            { title: "Field" },
            { title: "Methods" },
            { title: "Datasets" },
            { title: "Accesses"},
            { title: "Size"},
            { title: "Activity days"}
        ],
        columnDefs: [
            { type: 'file-size', targets: 7 }
          ]
    })
    
    $("#usersTableTotals").html(totals);
}
