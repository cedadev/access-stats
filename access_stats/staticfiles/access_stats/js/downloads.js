var currentYear = new Date().getFullYear();
var nextYear = currentYear + 1;

$.get(
{
    url: window.location.origin + `/downloads/json/methods?start=${currentYear}%2F01%2F01&end=${nextYear}%2F01%2F01&user=&dataset=&method=&anon=all`,
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
        row.push(data.results[method].users.toLocaleString());
        dataDict.datasets.push(data.results[method].datasets);
        row.push(data.results[method].datasets.toLocaleString());
        dataDict.accesses.push(data.results[method].accesses);
        row.push(data.results[method].accesses.toLocaleString());
        dataDict.size.push(data.results[method].size);
        row.push(formatBytes(data.results[method].size));
        dataDict.activitydays.push(data.results[method].activitydays);
        row.push(data.results[method].activitydays.toLocaleString());

        dataList.push(row);
    }
    
    totals = Mustache.render(templates.downloadsTableTotals, {totals:"Totals", users:data.totals.users.toLocaleString(), datasets:data.totals.datasets.toLocaleString(), accesses:data.totals.accesses.toLocaleString(), size:formatBytes(data.totals.size), activitydays:data.totals.activitydays.toLocaleString()});
    
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
            { type: "file-size", targets: 4 }
        ],
        responsive: true,
        "paging": false,
        "info": false,
        "searching": false
    })
    
    $("#downloadsTableTotals").html(totals);
}

function formatDate(a)
{
    var dated = new Date(a);
    return dated.toString("yyyy/MM");
}
