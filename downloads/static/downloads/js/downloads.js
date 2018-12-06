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
    var html;
    for (var month in data.results)
    {
        html += Mustache.render(templates.timelineTableBody, {month:formatDate(month),users:data.results[month].users,methods:data.results[month].methods,datasets:data.results[month].datasets,accesses:data.results[month].accesses,size:formatBytes(data.results[month].size),activitydays:data.results[month].activitydays});
    }
    $("#timelineTableBody").html(html);
    html = Mustache.render(templates.timelineTableFooter, {totals:"Totals",users:data.totals.users,methods:data.totals.methods,datasets:data.totals.datasets,accesses:data.totals.accesses,size:formatBytes(data.totals.size),activitydays:data.totals.activitydays});
    $("#timelineTableFooter").html(html);
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