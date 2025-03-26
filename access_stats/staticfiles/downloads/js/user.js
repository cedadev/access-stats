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
        country: [],
    }

    var dataDict = {
        country: [],
    }

    for (var country in data.results.group_by_country)
    {
        labelsDict.country.push(country);
        dataDict.country.push(data.results.group_by_country[country]);
    }

    userChart = makeUserChart(dataDict, labelsDict);
}

function makeUserChart(dataDict, labelsDict)
{
    var activeLabels = labelsDict.country;
    var activeData = dataDict.country;

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
