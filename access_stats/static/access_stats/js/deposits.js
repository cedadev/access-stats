$.get(
{
    url: window.location.origin + "/deposits/json/timeline?start=2019%2F01%2F01&end=2020%2F01%2F01&dataset=",
    success: function(data) 
    {
        renderTimelinePage(data);
    }
})

function renderTimelinePage(data)
{
    var dataDict = {
        days: [],
        size: [],
        datasets: [],
        deposits: [],
        directories: [],
        symlinks: [],
        removedDirs: [],
        removedFiles: []
    }

    var dataList = [];

    for (var day in data.results)
    {
        var row = [];

        dataDict.days.push(formatDepositsDate(day));
        row.push(formatDepositsDate(day));
        dataDict.size.push(data.results[day].size);
        row.push(formatBytes(data.results[day].size));
        dataDict.datasets.push(data.results[day].datasets);
        row.push(data.results[day].datasets.toLocaleString());
        dataDict.deposits.push(data.results[day].deposits);
        row.push(data.results[day].deposits.toLocaleString());
        dataDict.directories.push(data.results[day].mkdir);
        row.push(data.results[day].mkdir.toLocaleString());
        dataDict.symlinks.push(data.results[day].symlink);
        row.push(data.results[day].symlink.toLocaleString());
        dataDict.removedDirs.push(data.results[day].rmdir);
        row.push(data.results[day].rmdir.toLocaleString());
        dataDict.removedFiles.push(data.results[day].remove);
        row.push(data.results[day].remove.toLocaleString());

        dataList.push(row);
    }

    totals = Mustache.render(templates.depositsTableTotals, {totals:"Totals", size:formatBytes(data.totals.size), datasets:data.totals.datasets.toLocaleString(), deposits:data.totals.deposits.toLocaleString(), directories:data.totals.mkdir.toLocaleString(), symlinks:data.totals.symlink.toLocaleString(), removedDirs:data.totals.rmdir.toLocaleString(), removedFiles:data.totals.remove.toLocaleString()});
    
    $("#depositsTable").DataTable({
        data: dataList,
        columns: [
            { title: "Date" },
            { title: "Size" },
            { title: "Datasets" },
            { title: "Deposits" },
            { title: "Directories" },
            { title: "Symlinks" },
            { title: "Removed directories" },
            { title: "Removed files" }
        ],
        columnDefs: [
            { type: "file-size", targets: 1 }
        ],
        "pageLength": 7,
        "lengthMenu": [ [7, 30, -1], [7, 30, "All"] ],
        "order": [[0 , "desc"]]
    })
    
    $("#depositsTableTotals").html(totals);
}


function formatDepositsDate(a)
{
    var dated = new Date(a);
    return dated.toString("yyyy/MM/dd");
}
