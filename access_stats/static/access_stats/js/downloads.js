$.get(
{
    url: window.location.origin + "/downloads/json/methods?start=2019%2F01%2F01&end=2020%2F01%2F01&user=&dataset=&method=&anon=all",
    success: function(data) 
    {
        renderMethodsPage(data);
    }
})

function renderMethodsPage(data)
{
    var dataDict = {
        users: [],
        methods: [],
        datasets: [],
        accesses: [],
        size: [],
        activitydays: []
    }

    var dataList = [];

    for (var method in data.results)
    {
        var row = [];

        dataDict.methods.push(method);
        row.push(method);
        dataDict.users.push(data.results[method].users);
        row.push(data.results[method].users);
        dataDict.datasets.push(data.results[method].datasets);
        row.push(data.results[method].datasets);
        dataDict.accesses.push(data.results[method].accesses);
        row.push(data.results[method].accesses);
        dataDict.size.push(data.results[method].size);
        row.push(formatBytes(data.results[method].size));
        dataDict.activitydays.push(data.results[method].activitydays);
        row.push(data.results[method].activitydays);

        dataList.push(row);
    }
    
    totals = Mustache.render(templates.downloadsTableTotals, {totals:"Totals", users:data.totals.users, datasets:data.totals.datasets, accesses:data.totals.accesses, size:formatBytes(data.totals.size), activitydays:data.totals.activitydays});
    
    $("#downloadsTable").DataTable({
        data: dataList,
        columns: [
            { title: "Method" },
            { title: "Users" },
            { title: "Datasets" },
            { title: "Number of accesses" },
            { title: "Size" },
            { title: "Activity days"}
        ],
        columnDefs: [
            { type: 'file-size', targets: 4 }
          ],
        responsive: true
          
    })
    
    $("#downloadsTableTotals").html(totals);
}

function formatDate(a)
{
    var dated = new Date(a);
    return dated.toString("yyyy/MM");
}
