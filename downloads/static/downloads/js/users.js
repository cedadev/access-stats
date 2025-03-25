$("#users-message").html(loadingHTML);
$.get(
{
    url: window.location.origin + window.location.pathname + "json/" + "users" + window.location.search,
    success: function (data) {
        renderUsersPage(data);
        $("#users-message").hide();
    }
})

function renderUsersPage(data)
{
    var dataList = [];

    for (var user in data.results)
    {
        var row = [];

        row.push(user);
        row.push(data.results[user].country);
        row.push(data.results[user].methods.toLocaleString());
        row.push(data.results[user].datasets.toLocaleString());
        row.push(data.results[user].accesses.toLocaleString());
        row.push(formatBytes(data.results[user].size));
        row.push(data.results[user].activitydays.toLocaleString());

        dataList.push(row);
    }

    totals = Mustache.render(templates.usersTableTotals, {totals:"Totals", country:"-", methods:data.totals.methods.toLocaleString(), datasets:data.totals.datasets.toLocaleString(), accesses:data.totals.accesses.toLocaleString(), size:formatBytes(data.totals.size), activitydays:data.totals.activitydays.toLocaleString()});
    
    table = $("#usersTable").DataTable({
        retrieve: true,
        columns: [
            { title: "User" },
            { title: "Country" },
            { title: "Methods" },
            { title: "Datasets" },
            { title: "Accesses"},
            { title: "Size"},
            { title: "Activity days"}
        ],
        columnDefs: [
            { type: "file-size", targets: 7 }
        ],
        "pageLength": 50,
        "lengthMenu": [ [10, 50, 200, -1], [10, 50, 200, "All"] ]
    })

    table.clear();
    table.rows.add(dataList);
    table.draw();
    
    $("#usersTableTotals").html(totals);
}
