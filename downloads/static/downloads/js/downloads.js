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

function renderMethodsPage(data)
{
    console.log(data);
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
    console.log(data);
    var html;
    for (var month in data.results)
    {
        html += Mustache.render(templates.timelineTableBody, {month:formatDate(month),users:data.results[month].users,methods:data.results[month].methods,datasets:data.results[month].datasets,accesses:data.results[month].accesses,size:formatBytes(data.results[month].size),activitydays:data.results[month].activitydays});
    }
    $("#timelineTableBody").html(html);
    html = Mustache.render(templates.timelineTableFooter, {totals:"Totals",users:data.totals.users,methods:data.results[month].methods,datasets:data.totals.datasets,accesses:data.totals.accesses,size:formatBytes(data.totals.size),activitydays:data.totals.activitydays});
    $("#timelineTableFooter").html(html);
}

function formatBytes(a,b){if(0==a)return"0 Bytes";var c=1024,d=b||2,e=["Bytes","KB","MB","GB","TB","PB","EB","ZB","YB"],f=Math.floor(Math.log(a)/Math.log(c));return parseFloat((a/Math.pow(c,f)).toFixed(d))+" "+e[f]}

function formatDate(a){return a.split("-")[0]}