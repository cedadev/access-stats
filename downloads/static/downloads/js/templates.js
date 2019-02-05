var templates = {
    methodsTableBody: '<tr><th scope="row">{{method}}</th><td>{{users}}</td><td>{{datasets}}</td><td>{{accesses}}</td><td>{{size}}</td><td>{{activitydays}}</td></tr>',
    methodsTableFooter: '<tr><th scope="row">{{totals}}</th><th>{{users}}</th><th>{{datasets}}</th><th>{{accesses}}</th><th>{{size}}</th><th>{{activitydays}}</th></tr>',
    timelineTableBody: '<tr><th scope="row">{{month}}</th><td>{{users}}</td><td>{{methods}}</td><td>{{datasets}}</td><td>{{accesses}}</td><td>{{size}}</td><td>{{activitydays}}</td></tr>',
    timelineTableFooter: '<tr><th scope="row">{{totals}}</th><th>{{users}}</th><th>{{methods}}</th><th>{{datasets}}</th><th>{{accesses}}</th><th>{{size}}</th><th>{{activitydays}}</th></tr>',
    datasetTableBody: '<tr><th scope="row">{{dataset}}</th><td>{{users}}</td><td>{{methods}}</td><td>{{accesses}}</td><td>{{size}}</td><td>{{activitydays}}</td></tr>',
    datasetTableFooter: '<tr><th scope="row">{{totals}}</th><th>{{users}}</th><th>{{methods}}</th><th>{{accesses}}</th><th>{{size}}</th><th>{{activitydays}}</th></tr>',
    usersTableBody: '<tr><th scope="row">{{user}}</th><td>{{methods}}</td><td>{{datasets}}</td><td>{{accesses}}</td><td>{{size}}</td><td>{{activitydays}}</td></tr>',
    usersTableFooter: '<tr><th scope="row">{{totals}}</th><th>{{methods}}</th><th>{{datasets}}</th><th>{{accesses}}</th><th>{{size}}</th><th>{{activitydays}}</th></tr>',
    traceTableBody: '{{log}}\n',
    loadingMessage: '<div class="alert alert-light text-center text-dark">Loading...</div>',
    warningMessage: '<div class="alert alert-danger text-center">Too many {{analysis_method}}. Showing 500 of {{total}}. <a href="#" onclick={{allFunction}}>Show All</a></div>',
    errorMessage: '<div class="alert alert-danger text-center">Error loading data</div>',
    canvas: '<canvas class="my-2" id={{id}} width="600" height="350"></canvas>'
}
