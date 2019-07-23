// On default page load, get values in filters and add them to query in url
// TODO: Convert date safely
if (!window.location.search)
{
    var start = $("#id_start").val()
    var end = $("#id_end").val()
    window.history.replaceState("default", "Title", window.location.pathname + "?start=" + start + "&end=" + end + "&user=&dataset=&method=&anon=all");
}

// Sets up template for loading bar
var loadingHTML = Mustache.render(templates.loadingMessage)

function formatBytes(a, b){if(0==a)return"0 Bytes";var c=1000, d=b||2, e=["Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"], f=Math.floor(Math.log(a)/Math.log(c));return parseFloat((a/Math.pow(c, f)).toFixed(d))+" "+e[f]}

function formatDate(a)
{
    var dated = new Date(a);
    return dated.toString("yyyy/MM");
}

//Code to make sure upon refresh the correct tab is shown
if (location.hash) {
    $("a[href='" + location.hash.split(".")[0] + "']").tab("show");
    $("a[href='#" + location.hash.split(".")[1] + "']").tab("show");
}
var currentMethodsTab = null;
var currentTimelineTab = null;
var currentDatasetTab = null;
var currentUserTab = null;

$("body").on("click", "a[data-toggle='tab-main']", function (e) {
    e.preventDefault();
    var tabName = this.getAttribute("href")
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
    if (tabName == "#user") 
    {
        if (currentUserTab != null)
        {
            tabName = tabName + "." + currentUserTab;
        }
        else
        {
            tabName = tabName + ".userTabField";
        }
    }

    location.hash = tabName;
    $(this).tab("show");
    return false;
});
$("body").on("click", "a[data-toggle='tab-sub']", function (e) {
    e.preventDefault()
    var tabName = this.getAttribute("id")
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
    if (location.hash.split(".")[0] == "#user") 
    {
        currentUserTab = tabName;
    }

    $(this).tab("show");
    return false;
});
$(window).on("popstate", function () {
    var anchor = location.hash ||
        $("a[data-toggle='tab-main']").first().attr("href");
    $("a[href='" + anchor + "']").tab("show");
});
