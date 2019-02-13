$("#dataset-message").html(loadingHTML);
$.get(
{
    url: window.location.origin + window.location.pathname + "json/" + "dataset-limited" + window.location.search,
    success: function (data) {
        renderDatasetPage(data);
        if(data.totals.datasets > 500)
        {
            var html = Mustache.render(templates.warningMessage, {analysis_method:"Datasets", total:data.totals.datasets, allFunction:"datasetsGetAll()"});
            $("#dataset-message").html(html);
        }
        else
        {
            $("#dataset-message").hide();
        }
    }
})

function datasetsGetAll()
{
    $("#dataset-message").html(loadingHTML);
    $.get(
    {
        url: window.location.origin + window.location.pathname + "json/" + "dataset" + window.location.search,
        success: function (data) {
            renderDatasetPage(data);
            $("#dataset-message").hide();
        },
        error: function () {
            var html = Mustache.render(templates.errorMessage);
            $("#dataset-message").html(html);
        }
    })
}

function renderDatasetPage(data)
{
    var html;

    var dataDict = {
        datasets: [],
        users: [],
        methods: [],
        accesses: [],
        size: [],
        activitydays: []
    }

    for (var dataset in data.results)
    {
        dataDict.datasets.push(dataset);
        dataDict.users.push(data.results[dataset].users);
        dataDict.methods.push(data.results[dataset].methods);
        dataDict.accesses.push(data.results[dataset].accesses);
        dataDict.size.push(data.results[dataset].size);
        dataDict.activitydays.push(data.results[dataset].activitydays);
        html += Mustache.render(templates.datasetTableBody, {dataset:dataset, users:data.results[dataset].users, methods:data.results[dataset].methods, accesses:data.results[dataset].accesses, size:formatBytes(data.results[dataset].size), activitydays:data.results[dataset].activitydays});
    }
    $("#datasetTableBody").html(html);
    html = Mustache.render(templates.datasetTableFooter, {totals:"Totals", users:data.totals.users, methods:data.totals.methods, accesses:data.totals.accesses, size:formatBytes(data.totals.size), activitydays:data.totals.activitydays});
    $("#datasetTableFooter").html(html);

    datasetChart = makeDatasetChart(dataDict);

    var activeTab = null;
    if (location.hash) 
    {
        if (location.hash.split(".")[0] != "#dataset")
        {
            activeTab = "datasetTabUsers";
        }
        else
        {
            activeTab = location.hash.split(".")[1];
        }
    }
    else
    {
        activeTab = "datasetTabUsers";
    }
    datasetChart = updateDatasetChart(datasetChart, activeTab, dataDict);

    datasetTabs = ["datasetTabUsers", "datasetTabAccesses", "datasetTabSize", "datasetTabActivitydays"]
    $('a[data-toggle="tab-sub"]').on('shown.bs.tab', function (e) {
        if (datasetTabs.includes(e.target.id))
        {
            activeTab = e.target.id;
        }
        datasetChart = updateDatasetChart(datasetChart, activeTab, dataDict);
    })
}

function updateDatasetChart(chart, activeTab, dataDict)
{
    chart.destroy();
    chart = makeDatasetChart(dataDict);
    if(activeTab == "datasetTabUsers")
    {
        chart.data.datasets[0].hidden = false;
    }
    if(activeTab == "datasetTabAccesses")
    {
        chart.data.datasets[1].hidden = false;
    }
    if(activeTab == "datasetTabSize")
    {
        chart.data.datasets[2].hidden = false;
    }
    if(activeTab == "datasetTabActivitydays")
    {
        chart.data.datasets[3].hidden = false;
    }
    chart.update();
    return chart;
}

function makeDatasetChart(dataDict)
{
    var html = Mustache.render(templates.canvas, {id:"datasetChart"})
    $("#datasetChartBox").html(html);
    var datasetChartElement = $("#datasetChart");
    var datasetChart = new Chart(datasetChartElement, {
        type: 'doughnut',
        data: {
            labels: dataDict.datasets,
            datasets: [{
                label: '# of users',
                data: dataDict.users,
                borderWidth: 0,
                hidden: true
            },
            {
                label: '# of accesses',
                data: dataDict.accesses,
                borderWidth: 0,
                hidden: true
            },
            {
                label: 'size',
                data: dataDict.size,
                borderWidth: 0,
                hidden: true
            },
            {
                label: '# of activity days',
                data: dataDict.activitydays,
                borderWidth: 0,
                hidden: true
            }
        ]
        },
        options: {
            responsive: true,
            legend: {
                display: false
            },
            plugins: {
                colorschemes: {
                    scheme: 'brewer.Paired12'
                }
            }
        }
    });
    return datasetChart
}
