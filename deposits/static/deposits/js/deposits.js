// On default page load, get values in filters and add them to query in url
// TODO: Convert date safely
if (!window.location.search)
{
    var start = $("#id_start").val()
    var end = $("#id_end").val()
    window.history.replaceState('default', 'Title', window.location.pathname + "?start=" + start + "&end=" + end + "&dataset=");
}

// Sets up template for loading bar
var loadingHTML = Mustache.render(templates.loadingMessage)

function formatBytes(a, b){if(0==a)return"0 Bytes";var c=1000, d=b||2, e=["Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"], f=Math.floor(Math.log(a)/Math.log(c));return parseFloat((a/Math.pow(c, f)).toFixed(d))+" "+e[f]}

function formatDate(a)
{
    var dated = new Date(a);
    return dated.toString("yyyy/MM/dd");
}

//Code to make sure upon refresh the correct tab is shown
if (location.hash) {
    $("a[href='" + location.hash.split(".")[0] + "']").tab('show');
    $("a[href='#" + location.hash.split(".")[1] + "']").tab('show');
}
var currentDatasetTab = null;

$('body').on('click', 'a[data-toggle=\'tab-main\']', function (e) {
    e.preventDefault();
    var tabName = this.getAttribute('href')
    if (tabName == "#dataset") 
    {
        if (currentDatasetTab != null)
        {
            tabName = tabName + "." + currentDatasetTab;
        }
        else
        {
            tabName = tabName + ".datasetTabSize";
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
