$("#timeline-message").html(loadingHTML);
$.get(
{
    url: window.location.origin + window.location.pathname + "json/" + "timeline" + window.location.search,
    success: function(data) 
    {
        renderTimelinePage(data);
        $("#timeline-message").hide();
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

    var body;
    for (var day in data.results)
    {
        dataDict.days.push(formatDate(day));
        dataDict.size.push(data.results[day].size);
        dataDict.datasets.push(data.results[day].datasets);
        dataDict.deposits.push(data.results[day].deposits);
        dataDict.directories.push(data.results[day].mkdir);
        dataDict.symlinks.push(data.results[day].symlink);
        dataDict.removedDirs.push(data.results[day].rmdir);
        dataDict.removedFiles.push(data.results[day].remove);
        body += Mustache.render(templates.timelineTableBody, {day:formatDate(day), size:formatBytes(data.results[day].size), datasets:data.results[day].datasets, deposits:data.results[day].deposits, directories:data.results[day].mkdir, symlinks:data.results[day].symlink, removedDirs:data.results[day].rmdir, removedFiles:data.results[day].remove});
    }
    header = Mustache.render(templates.timelineTableTotals, {totals:"Totals", size:formatBytes(data.totals.size), datasets:data.totals.datasets, deposits:data.totals.deposits, directories:data.totals.mkdir, symlinks:data.totals.symlink, removedDirs:data.totals.rmdir, removedFiles:data.totals.remove});
    $("#timelineTableBody").html(header + body);
    $("#timelineTableTotals").html(header);

    timelineChart = makeTimelineChart(dataDict);
}

function makeTimelineChart(dataDict)
{
    var timelineChartElement = $("#timelineChart");
    var timelineChart = new Chart(timelineChartElement, {
        type: "line",
        data: {
            labels: dataDict.days,
            datasets: [{
                label: "size",
                yAxisID: "size",
                data: dataDict.size,
                fill: false,
                showLine: false,
                borderColor: "#00628d",
                backgroundColor: "#00628d",
                pointBackgroundColor: "#00628d",
                pointBorderColor: "#00628d",
                borderWidth: 1,
                hidden: false
            },
            {
                label: "# of deposits",
                yAxisID: "deposits",
                data: dataDict.deposits,
                fill: false,
                showLine: false,
                borderColor: "#E33C4F",
                backgroundColor: "#E33C4F",
                pointBackgroundColor: "#E33C4F",
                pointBorderColor: "#E33C4F",
                borderWidth: 1,
                hidden: false
            }
        ]
        },
        options: {
            responsive: true,
            legend: {
                display: true
            },
            scales: {
                yAxes: [{
                    id: "size",
                    type: "linear",
                    position: "left",
                    labelString: "Size",
                    ticks: {
                        beginAtZero: true
                    }
                },
                {
                    id: "deposits",
                    type: "linear",
                    position: "right",
                    labelString: "Deposits",
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
    return timelineChart
}
