

if (window.location.pathname == "/downloads/")
{
    var start = $("#id_start").val()
    var end = $("#id_end").val()
    window.history.replaceState('default', 'Title', window.location.pathname + "?start=" + start + "&end=" + end + "&user=&dataset=&method=&anon=all");
}


var loadingHTML = Mustache.render(templates.loadingMessage)
$("#methods-message").html(loadingHTML);
$.get(
{
    url: window.location.origin + window.location.pathname + "json/" + "methods" + window.location.search,
    success: function(data) 
    {
        renderMethodsPage(data);
        $("#methods-message").hide();
    }
})

$("#timeline-message").html(loadingHTML);
$.get(
{
    url: window.location.origin + window.location.pathname + "json/" + "timeline" + window.location.search,
    success: function (data) {
        renderTimelinePage(data);
        $("#timeline-message").hide();
    }
})


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

$("#trace-message").html(loadingHTML);
$.get(
{
    url: window.location.origin + window.location.pathname + "json/" + "trace" + window.location.search,
    success: function (data) {
        renderTracePage(data);
        $("#trace-message").hide();
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

    var html;
    for (var method in data.results)
    {
        dataDict.methods.push(method);
        dataDict.users.push(data.results[method].users);
        dataDict.datasets.push(data.results[method].datasets);
        dataDict.accesses.push(data.results[method].accesses);
        dataDict.size.push(data.results[method].size);
        //dataDict.activitydays.push(data.results[method].activitydays);
        html += Mustache.render(templates.methodsTableBody, {method:method,users:data.results[method].users,datasets:data.results[method].datasets,accesses:data.results[method].accesses,size:formatBytes(data.results[method].size),activitydays:data.results[method].activitydays});
    }
    $("#methodsTableBody").html(html);
    html = Mustache.render(templates.methodsTableFooter, {totals:"Totals",users:data.totals.users,datasets:data.totals.datasets,accesses:data.totals.accesses,size:formatBytes(data.totals.size),activitydays:data.totals.activitydays});
    $("#methodsTableFooter").html(html);

    methodsChart = makeMethodsChart(dataDict);

    var activeTab = null;
    if (location.hash)
    {
        if (location.hash.split(".")[0] != "#methods")
        {
            activeTab = "methodsTabUsers";
        }
        else
        {
            activeTab = location.hash.split(".")[1];
        }
    }
    else
    {
        activeTab = "methodsTabUsers";
    }
    methodsChart = updateMethodsChart(methodsChart, activeTab, dataDict);

    methodsTabs = ["methodsTabUsers","methodsTabMethods","methodsTabDatasets","methodsTabAccesses","methodsTabSize","methodsTabActivitydays"]
    $('a[data-toggle="tab-sub"]').on('shown.bs.tab', function (e) {
        if (methodsTabs.includes(e.target.id))
        {
            activeTab = e.target.id;
        }
        methodsChart = updateMethodsChart(methodsChart, activeTab, dataDict);
    })
}

function updateMethodsChart(chart, activeTab, dataDict)
{
    chart.destroy();
    chart = makeMethodsChart(dataDict);
    if(activeTab == "methodsTabUsers")
    {
        chart.data.datasets[0].hidden = false;
    }
    if(activeTab == "methodsTabDatasets")
    {
        chart.data.datasets[1].hidden = false;
    }
    if(activeTab == "methodsTabAccesses")
    {
        chart.data.datasets[2].hidden = false;
    }
    if(activeTab == "methodsTabSize")
    {
        chart.data.datasets[3].hidden = false;
    }
    if(activeTab == "methodsTabActivitydays")
    {
        chart.data.datasets[4].hidden = false;
    }
    chart.update();
    return chart;
}

function makeMethodsChart(dataDict)
{
    var methodsChartElement = $("#methodsChart");
    var methodsChart = new Chart(methodsChartElement, {
        type: 'bar',
        data: {
            labels: dataDict.methods,
            datasets: [{
                label: '# of users',
                data: dataDict.users,
                hidden: true
            },
            {
                label: '# of datasets',
                data: dataDict.datasets,
                hidden: true
            },
            {
                label: '# of accesses',
                data: dataDict.accesses,
                hidden: true
            },
            {
                label: 'size',
                data: dataDict.size,
                hidden: true
            },
            {
                label: '# of activity days',
                data: dataDict.activitydays,
                hidden: true
            }
        ]
        },
        options: {
            responsive: true,
            legend: {
                display: false
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }],
                xAxes: [{
                    ticks: {
                      autoSkip: false
                    }
                  }]
            },
            plugins: {
                colorschemes: {
                    scheme: 'brewer.Pastel1-9'
                }
            }
        }
    });
    return methodsChart
}

function renderTimelinePage(data)
{
    var dataDict = {
        months: [],
        users: [],
        methods: [],
        datasets: [],
        accesses: [],
        size: [],
        activitydays: []
    }

    var html;
    for (var month in data.results)
    {
        dataDict.months.push(formatDate(month));
        dataDict.users.push(data.results[month].users);
        dataDict.methods.push(data.results[month].methods);
        dataDict.datasets.push(data.results[month].datasets);
        dataDict.accesses.push(data.results[month].accesses);
        dataDict.size.push(data.results[month].size);
        //dataDict.activitydays.push(data.results[month].activitydays);
        html += Mustache.render(templates.timelineTableBody, {month:formatDate(month),users:data.results[month].users,methods:data.results[month].methods,datasets:data.results[month].datasets,accesses:data.results[month].accesses,size:formatBytes(data.results[month].size),activitydays:data.results[month].activitydays});
    }
    $("#timelineTableBody").html(html);
    html = Mustache.render(templates.timelineTableFooter, {totals:"Totals",users:data.totals.users,methods:data.totals.methods,datasets:data.totals.datasets,accesses:data.totals.accesses,size:formatBytes(data.totals.size),activitydays:data.totals.activitydays});
    $("#timelineTableFooter").html(html);

    timelineChart = makeTimelineChart(dataDict);

    var activeTab = null;
    if (location.hash) 
    {
        if (location.hash.split(".")[0] != "#timeline")
        {
            activeTab = "timelineTabUsers";
        }
        else
        {
            activeTab = location.hash.split(".")[1];
        }
    }
    else
    {
        activeTab = "timelineTabUsers";
    }
    timelineChart = updateTimelineChart(timelineChart, activeTab, dataDict);


    timelineTabs = ["timelineTabUsers","timelineTabMethods","timelineTabDatasets","timelineTabAccesses","timelineTabSize","timelineTabActivitydays"]
    $('a[data-toggle="tab-sub"]').on('shown.bs.tab', function (e) {
        if (timelineTabs.includes(e.target.id))
        {
            activeTab = e.target.id;
        }
        timelineChart = updateTimelineChart(timelineChart, activeTab, dataDict);
    })
}

function updateTimelineChart(chart, activeTab, dataDict)
{
    chart.destroy();
    chart = makeTimelineChart(dataDict);
    if(activeTab == "timelineTabUsers")
    {
        chart.data.datasets[0].hidden = false;
    }
    if(activeTab == "timelineTabMethods")
    {
        chart.data.datasets[1].hidden = false;
    }
    if(activeTab == "timelineTabDatasets")
    {
        chart.data.datasets[2].hidden = false;
    }
    if(activeTab == "timelineTabAccesses")
    {
        chart.data.datasets[3].hidden = false;
    }
    if(activeTab == "timelineTabSize")
    {
        chart.data.datasets[4].hidden = false;
    }
    if(activeTab == "timelineTabActivitydays")
    {
        chart.data.datasets[5].hidden = false;
    }
    chart.update();
    return chart;
}

function makeTimelineChart(dataDict)
{
    var timelineChartElement = $("#timelineChart");
    var timelineChart = new Chart(timelineChartElement, {
        type: 'line',
        data: {
            labels: dataDict.months,
            datasets: [{
                label: '# of users',
                data: dataDict.users,
                fill: false,
                borderColor: "#00628d",
                backgroundColor: "#00628d",
                pointBackgroundColor: "#00628d",
                borderWidth: 1,
                hidden: true
            },
            {
                label: '# of methods',
                data: dataDict.methods,
                fill: false,
                borderColor: "#00628d",
                backgroundColor: "#00628d",
                pointBackgroundColor: "#00628d",
                borderWidth: 1,
                hidden: true
            },
            {
                label: '# of datasets',
                data: dataDict.datasets,
                fill: false,
                borderColor: "#00628d",
                backgroundColor: "#00628d",
                pointBackgroundColor: "#00628d",
                borderWidth: 1,
                hidden: true
            },
            {
                label: '# of accesses',
                data: dataDict.accesses,
                fill: false,
                borderColor: "#00628d",
                backgroundColor: "#00628d",
                pointBackgroundColor: "#00628d",
                borderWidth: 1,
                hidden: true
            },
            {
                label: 'size',
                data: dataDict.size,
                fill: false,
                borderColor: "#00628d",
                backgroundColor: "#00628d",
                pointBackgroundColor: "#00628d",
                borderWidth: 1,
                hidden: true
            },
            {
                label: '# of activity days',
                data: dataDict.activitydays,
                fill: false,
                borderColor: "#00628d",
                backgroundColor: "#00628d",
                pointBackgroundColor: "#00628d",
                borderWidth: 1,
                hidden: true
            }
        ]
        },
        options: {
            responsive: true,
            legend: {
                display: false
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
    return timelineChart
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
        //dataDict.activitydays.push(data.results[dataset].activitydays);
        html += Mustache.render(templates.datasetTableBody, {dataset:dataset,users:data.results[dataset].users,methods:data.results[dataset].methods,accesses:data.results[dataset].accesses,size:formatBytes(data.results[dataset].size),activitydays:data.results[dataset].activitydays});
    }
    $("#datasetTableBody").html(html);
    html = Mustache.render(templates.datasetTableFooter, {totals:"Totals",users:data.totals.users,methods:data.totals.methods,accesses:data.totals.accesses,size:formatBytes(data.totals.size),activitydays:data.totals.activitydays});
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

    datasetTabs = ["datasetTabUsers","datasetTabAccesses","datasetTabSize","datasetTabActivitydays"]
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
    var html = Mustache.render(templates.canvas,{id:"datasetChart"})
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

function renderUsersPage(data)
{
    var html;
    for (var user in data.results)
    {
        html += Mustache.render(templates.usersTableBody, {user:user,methods:data.results[user].methods,datasets:data.results[user].datasets,accesses:data.results[user].accesses,size:formatBytes(data.results[user].size)});
        //html += Mustache.render(templates.usersTableBody, {user:user,methods:data.results[user].methods,datasets:data.results[user].datasets,accesses:data.results[user].accesses,size:formatBytes(data.results[user].size),activitydays:data.results[user].activitydays});
    }
    $("#usersTableBody").html(html);
    html = Mustache.render(templates.usersTableFooter, {totals:"Totals",methods:data.totals.methods,datasets:data.totals.datasets,accesses:data.totals.accesses,size:formatBytes(data.totals.size),activitydays:data.totals.activitydays});
    $("#usersTableFooter").html(html);
}

function renderTracePage(data)
{
    var html = "";
    for (var i = 0; i < data.logs.length; i++)
    {
        html += Mustache.render(templates.traceTableBody, {log:data.logs[i]});
    }
    $("#traceTableBody").html(html);
}

function formatBytes(a,b){if(0==a)return"0 Bytes";var c=1024,d=b||2,e=["Bytes","KB","MB","GB","TB","PB","EB","ZB","YB"],f=Math.floor(Math.log(a)/Math.log(c));return parseFloat((a/Math.pow(c,f)).toFixed(d))+" "+e[f]}

// Needs to change if datetime format does:
function formatDate(a)
{
    var dated = new Date(a);
    return dated.toString("yyyy/MM");
}

if (location.hash) {
    $("a[href='" + location.hash.split(".")[0] + "']").tab('show');
    $("a[href='#" + location.hash.split(".")[1] + "']").tab('show');
}
var currentMethodsTab = null;
var currentTimelineTab = null;
var currentDatasetTab = null;

$('body').on('click', 'a[data-toggle=\'tab-main\']', function (e) {
    e.preventDefault();
    var tabName = this.getAttribute('href')
    if (tabName == "#methods") 
    {
        if (currentMethodsTab != null)
        {
            tabName = tabName + "." + currentMethodsTab;
        }
        else
        {
            tabName = tabName + ".methodsTabUsers";
        }
    }
    if (tabName == "#timeline") 
    {
        if (currentTimelineTab != null)
        {
            tabName = tabName + "." + currentTimelineTab;
        }
        else
        {
            tabName = tabName + ".timelineTabUsers";
        }
    }
    if (tabName == "#dataset") 
    {
        if (currentDatasetTab != null)
        {
            tabName = tabName + "." + currentDatasetTab;
        }
        else
        {
            tabName = tabName + ".datasetTabUsers";
        }
    }

    location.hash = tabName;
    $(this).tab('show');
    return false;
});
$('body').on('click', 'a[data-toggle=\'tab-sub\']', function (e) {
    e.preventDefault()
    var tabName = this.getAttribute('id')
    location.hash = location.hash.split(".")[0] + "." + tabName;
    if (location.hash.split(".")[0] == "#methods") 
    {
        currentMethodsTab = tabName;
    }
    if (location.hash.split(".")[0] == "#timeline") 
    {
        currentTimelineTab = tabName;
    }
    if (location.hash.split(".")[0] == "#dataset") 
    {
        currentDatasetTab = tabName;
    }

    $(this).tab('show');
    return false;
});
$(window).on('popstate', function () {
    var anchor = location.hash ||
        $('a[data-toggle=\'tab-main\']').first().attr('href');
    $('a[href=\'' + anchor + '\']').tab('show');
});
