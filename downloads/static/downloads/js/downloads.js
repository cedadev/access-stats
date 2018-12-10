$.get(
{
    url: window.location.origin + window.location.pathname + "json/" + "methods" + window.location.search,
    success: function(data) 
    {
        renderMethodsPage(data)
    }
})

$.get(
{
    url: window.location.origin + window.location.pathname + "json/" + "timeline" + window.location.search,
    success: function (data) {
        renderTimelinePage(data)
    }
})

$.get(
{
    url: window.location.origin + window.location.pathname + "json/" + "dataset" + window.location.search,
    success: function (data) {
        renderDatasetPage(data)
    }
})

$.get(
{
    url: window.location.origin + window.location.pathname + "json/" + "users" + window.location.search,
    success: function (data) {
        renderUsersPage(data)
    }
})

$.get(
{
    url: window.location.origin + window.location.pathname + "json/" + "trace" + window.location.search,
    success: function (data) {
        renderTracePage(data)
    }
})

function renderMethodsPage(data)
{
    var html;
    for (var method in data.results)
    {
        html += Mustache.render(templates.methodsTableBody, {method:method,users:data.results[method].users,datasets:data.results[method].datasets,accesses:data.results[method].accesses,size:formatBytes(data.results[method].size),activitydays:data.results[method].activitydays});
    }
    $("#methodsTableBody").html(html);
    html = Mustache.render(templates.methodsTableFooter, {totals:"Totals",users:data.totals.users,datasets:data.totals.datasets,accesses:data.totals.accesses,size:formatBytes(data.totals.size),activitydays:data.totals.activitydays});
    $("#methodsTableFooter").html(html);
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
        dataDict.activitydays.push(data.results[month].activitydays);
        html += Mustache.render(templates.timelineTableBody, {month:formatDate(month),users:data.results[month].users,methods:data.results[month].methods,datasets:data.results[month].datasets,accesses:data.results[month].accesses,size:formatBytes(data.results[month].size),activitydays:data.results[month].activitydays});
    }
    $("#timelineTableBody").html(html);
    html = Mustache.render(templates.timelineTableFooter, {totals:"Totals",users:data.totals.users,methods:data.totals.methods,datasets:data.totals.datasets,accesses:data.totals.accesses,size:formatBytes(data.totals.size),activitydays:data.totals.activitydays});
    $("#timelineTableFooter").html(html);

    timelineChart = makeChart(dataDict);

    var activeTab = "timelineTabUsers";
    timelineTabs = ["timelineTabUsers","timelineTabMethods","timelineTabDatasets","timelineTabAccesses","timelineTabSize","timelineTabActivitydays"]
    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        if (timelineTabs.includes(e.target.id))
        {
            activeTab = e.target.id;
        }
        timelineChart = updateChart(timelineChart, activeTab, dataDict);
    })
}

function updateChart(chart, activeTab, dataDict)
{
    chart.destroy();
    chart = makeChart(dataDict);
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

function makeChart(dataDict)
{
    var timelineChartUsers = document.getElementById("timelineChart").getContext('2d');
    var timelineUsers = new Chart(timelineChartUsers, {
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
            responsive: false,
            legend: {
                display: false
            }
        }
    
    });
    return timelineUsers
}

function renderDatasetPage(data)
{
    var html;
    for (var dataset in data.results)
    {
        html += Mustache.render(templates.datasetTableBody, {dataset:dataset,users:data.results[dataset].users,methods:data.results[dataset].methods,accesses:data.results[dataset].accesses,size:formatBytes(data.results[dataset].size),activitydays:data.results[dataset].activitydays});
    }
    $("#datasetTableBody").html(html);
    html = Mustache.render(templates.datasetTableFooter, {totals:"Totals",users:data.totals.users,methods:data.totals.methods,accesses:data.totals.accesses,size:formatBytes(data.totals.size),activitydays:data.totals.activitydays});
    $("#datasetTableFooter").html(html);
}

function renderUsersPage(data)
{
    var html;
    for (var user in data.results)
    {
        html += Mustache.render(templates.usersTableBody, {user:user,methods:data.results[user].methods,datasets:data.results[user].datasets,accesses:data.results[user].accesses,size:formatBytes(data.results[user].size),activitydays:data.results[user].activitydays});
    }
    $("#usersTableBody").html(html);
    html = Mustache.render(templates.usersTableFooter, {totals:"Totals",methods:data.totals.methods,datasets:data.totals.datasets,accesses:data.totals.accesses,size:formatBytes(data.totals.size),activitydays:data.totals.activitydays});
    $("#usersTableFooter").html(html);
}

function renderTracePage(data)
{
    var html;
    for (var i = 0; i < data.logs.length; i++)
    {
        html += Mustache.render(templates.traceTableBody, {log:data.logs[i]});
    }
    $("#traceTableBody").html(html);
}

function formatBytes(a,b){if(0==a)return"0 Bytes";var c=1024,d=b||2,e=["Bytes","KB","MB","GB","TB","PB","EB","ZB","YB"],f=Math.floor(Math.log(a)/Math.log(c));return parseFloat((a/Math.pow(c,f)).toFixed(d))+" "+e[f]}

function formatDate(a){return a.split("-")[0]}