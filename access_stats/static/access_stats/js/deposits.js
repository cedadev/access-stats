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
        row.push(data.results[day].datasets);
        dataDict.deposits.push(data.results[day].deposits);
        row.push(data.results[day].deposits);
        dataDict.directories.push(data.results[day].mkdir);
        row.push(data.results[day].mkdir);
        dataDict.symlinks.push(data.results[day].symlink);
        row.push(data.results[day].symlink);
        dataDict.removedDirs.push(data.results[day].rmdir);
        row.push(data.results[day].rmdir);
        dataDict.removedFiles.push(data.results[day].remove);
        row.push(data.results[day].remove);

        dataList.push(row);
    }

    totals = Mustache.render(templates.depositsTableTotals, {totals:"Totals", size:formatBytes(data.totals.size), datasets:data.totals.datasets, deposits:data.totals.deposits, directories:data.totals.mkdir, symlinks:data.totals.symlink, removedDirs:data.totals.rmdir, removedFiles:data.totals.remove});
    
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
            { type: 'file-size', targets: 1 }
          ]
    })
    
    $("#depositsTableTotals").html(totals);
}


function formatDepositsDate(a)
{
    var dated = new Date("2019-01-02T00:00:00.000Z");
    console.log(dated);
    console.log(dated.toString("yyyy/MM/dd"));
    return dated.toString("yyyy/MM/dd");
}
