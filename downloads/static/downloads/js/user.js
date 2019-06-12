$("#user-message").html(loadingHTML);
$.get(
{
    url: window.location.origin + window.location.pathname + "json/" + "user" + window.location.search,
    success: function (data) {
        renderUserPage(data);
        $("#user-message").hide();
    }
})

function renderUserPage(data)
{
    var labelsDict = {
        field: [],
        country: [],
        instituteType: [],
        odaCountry: [],
        area: []
    }

    var dataDict = {
        field: [],
        country: [],
        instituteType: [],
        odaCountry: [],
        area: []
    }

    for (var field in data.results.group_by_field)
    {
        labelsDict.field.push(field);
        dataDict.field.push(data.results.group_by_field[field]);
    }

    for (var country in data.results.group_by_country)
    {
        labelsDict.country.push(country);
        dataDict.country.push(data.results.group_by_country[country]);
    }

    for (var instituteType in data.results.group_by_institute_type)
    {
        labelsDict.instituteType.push(instituteType);
        dataDict.instituteType.push(data.results.group_by_institute_type[instituteType]);
    }

    for (var odaCountry in data.results.group_by_oda_type)
    {
        labelsDict.odaCountry.push(odaCountry);
        dataDict.odaCountry.push(data.results.group_by_oda_type[odaCountry]);
    }

    for (var area in data.results.group_by_area)
    {
        labelsDict.area.push(area);
        dataDict.area.push(data.results.group_by_area[area]);
    }

    var activeTab = null;

    userChart = makeUserChart(activeTab, dataDict, labelsDict);

    
    if (location.hash) 
    {
        if (location.hash.split(".")[0] != "#user")
        {
            activeTab = "userTabField";
        }
        else
        {
            activeTab = location.hash.split(".")[1];
        }
    }
    else
    {
        activeTab = "userTabField";
    }
    userChart = updateUserChart(userChart, activeTab, dataDict, labelsDict);

    userTabs = ["userTabField", "userTabCountry", "userTabInstituteType", "userTabOdaCountry", "userTabArea"]
    $('a[data-toggle="tab-sub"]').on("shown.bs.tab", function (e) {
        if (userTabs.includes(e.target.id))
        {
            activeTab = e.target.id;
        }
        userChart = updateUserChart(userChart, activeTab, dataDict, labelsDict);
    })
}

function updateUserChart(chart, activeTab, dataDict, labelsDict)
{
    chart.destroy();
    chart = makeUserChart(activeTab, dataDict, labelsDict);
    chart.update();
    return chart;
}

function makeUserChart(activeTab, dataDict, labelsDict)
{
    if (activeTab == "userTabField" || !activeTab)
    {
        var activeLabels = labelsDict.field;
        var activeData = dataDict.field;
    }
    else if (activeTab == "userTabCountry")
    {
        var activeLabels = labelsDict.country;
        var activeData = dataDict.country;
    }
    else if (activeTab == "userTabInstituteType")
    {
        var activeLabels = labelsDict.instituteType;
        var activeData = dataDict.instituteType;
    }
    else if (activeTab == "userTabOdaCountry")
    {
        var activeLabels = labelsDict.odaCountry;
        var activeData = dataDict.odaCountry;
    }
    else if (activeTab == "userTabArea")
    {
        var activeLabels = labelsDict.area;
        var activeData = dataDict.area;
    }
    var html = Mustache.render(templates.canvas, {id:"userChart"})
    $("#userChartBox").html(html);
    var userChartElement = $("#userChart");
    var userChart = new Chart(userChartElement, {
        type: "doughnut",
        data: {
            labels: activeLabels,
            datasets: [{
                data: activeData,
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            plugins: {
                colorschemes: {
                    scheme: "brewer.Paired12"
                }
            },
            tooltips: {
                callbacks: {
                  label: function(tooltipItem, data) {
                    var dataset = data.datasets[tooltipItem.datasetIndex];
                    var meta = dataset._meta[Object.keys(dataset._meta)[0]];
                    var total = meta.total;
                    var currentValue = dataset.data[tooltipItem.index];
                    var percentage = parseFloat((currentValue/total*100).toFixed(1));
                    return currentValue + " (" + percentage + "%)";
                  },
                  title: function(tooltipItem, data) {
                    return data.labels[tooltipItem[0].index];
                  }
                }
              }
        }
    });
    return userChart
}
