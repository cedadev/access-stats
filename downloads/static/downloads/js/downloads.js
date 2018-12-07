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
    var months = [];
    var users = [];
    var methods = [];
    var datasets = [];
    var accesses = [];
    var size = [];
    var activitydays = [];

    var html;
    for (var month in data.results)
    {
        months.push(formatDate(month));
        users.push(data.results[month].users);
        methods.push(data.results[month].methods);
        datasets.push(data.results[month].datasets);
        accesses.push(data.results[month].accesses);
        size.push(data.results[month].size);
        activitydays.push(data.results[month].activitydays);
        html += Mustache.render(templates.timelineTableBody, {month:formatDate(month),users:data.results[month].users,methods:data.results[month].methods,datasets:data.results[month].datasets,accesses:data.results[month].accesses,size:formatBytes(data.results[month].size),activitydays:data.results[month].activitydays});
    }
    $("#timelineTableBody").html(html);
    html = Mustache.render(templates.timelineTableFooter, {totals:"Totals",users:data.totals.users,methods:data.totals.methods,datasets:data.totals.datasets,accesses:data.totals.accesses,size:formatBytes(data.totals.size),activitydays:data.totals.activitydays});
    $("#timelineTableFooter").html(html);

    timelineUsers = makeTableUsers(months, users);

    var timelineChartMethods = document.getElementById("timelineChartMethods").getContext('2d');
    var timelineMethods = new Chart(timelineChartMethods, {
        type: 'line',
        data: {
            labels: months,
            datasets: [{
                label: '# of methods',
                data: methods,
                fill: false,
                borderColor: "#00628d",
                backgroundColor: "#00628d",
                pointBackgroundColor: "#00628d",
                borderWidth: 1
            }]
        },
        options: {
            responsive: false,
            legend: {
                display: false
            }
        }
    
    });
    var timelineChartDatasets = document.getElementById("timelineChartDatasets").getContext('2d');
    var timelineDatasets = new Chart(timelineChartDatasets, {
        type: 'line',
        data: {
            labels: months,
            datasets: [{
                label: '# of datasets',
                data: datasets,
                fill: false,
                borderColor: "#00628d",
                backgroundColor: "#00628d",
                pointBackgroundColor: "#00628d",
                borderWidth: 1
            }]
        },
        options: {
            responsive: false,
            legend: {
                display: false
            }
        }
    
    });
    var timelineChartAccesses = document.getElementById("timelineChartAccesses").getContext('2d');
    var timelineAccesses = new Chart(timelineChartAccesses, {
        type: 'line',
        data: {
            labels: months,
            datasets: [{
                label: '# of accesses',
                data: accesses,
                fill: false,
                borderColor: "#00628d",
                backgroundColor: "#00628d",
                pointBackgroundColor: "#00628d",
                borderWidth: 1
            }]
        },
        options: {
            responsive: false,
            legend: {
                display: false
            }
        }
    
    });
    var timelineChartSize = document.getElementById("timelineChartSize").getContext('2d');
    var timelineSize = new Chart(timelineChartSize, {
        type: 'line',
        data: {
            labels: months,
            datasets: [{
                label: 'size',
                data: size,
                fill: false,
                borderColor: "#00628d",
                backgroundColor: "#00628d",
                pointBackgroundColor: "#00628d",
                borderWidth: 1
            }]
        },
        options: {
            responsive: false,
            legend: {
                display: false
            }
        }
    
    });
    var timelineChartActivitydays = document.getElementById("timelineChartActivitydays").getContext('2d');
    var timelineActivityDays = new Chart(timelineChartActivitydays, {
        type: 'line',
        data: {
            labels: months,
            datasets: [{
                label: 'activity days',
                data: activitydays,
                fill: false,
                borderColor: "#00628d",
                backgroundColor: "#00628d",
                pointBackgroundColor: "#00628d",
                borderWidth: 1
            }]
        },
        options: {
            responsive: false,
            legend: {
                display: false
            }
        }
    
    });

    $('.nav-tabs a').on('shown.bs.tab', function(event){
        var x = $(event.target).text();         
        if(x == "Users")
        {
            timelineUsers.destroy();
            makeTableUsers(months, users);
        }
        console.log($(event.target));
    }); 


}

function makeTableUsers(months, users)
{
    var timelineChartUsers = document.getElementById("timelineChartUsers").getContext('2d');
    var timelineUsers = new Chart(timelineChartUsers, {
        type: 'line',
        data: {
            labels: months,
            datasets: [{
                label: '# of users',
                data: users,
                fill: false,
                borderColor: "#00628d",
                backgroundColor: "#00628d",
                pointBackgroundColor: "#00628d",
                borderWidth: 1
            }]
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