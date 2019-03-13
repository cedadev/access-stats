var templates = {
    methodsTableTotals: '<tr><th scope="row">{{totals}}</th><th>{{users}}</th><th>{{datasets}}</th><th>{{accesses}}</th><th>{{size}}</th><th>{{activitydays}}</th></tr>',
    timelineTableTotals: '<tr><th scope="row">{{totals}}</th><th>{{users}}</th><th>{{methods}}</th><th>{{datasets}}</th><th>{{accesses}}</th><th>{{size}}</th><th>{{activitydays}}</th></tr>',
    datasetTableTotals: '<tr><th scope="row">{{totals}}</th><th>{{users}}</th><th>{{methods}}</th><th>{{accesses}}</th><th>{{size}}</th><th>{{activitydays}}</th></tr>',
    usersTableTotals: '<tr><th scope="row">{{totals}}</th><th>{{country}}</th><th>{{institute}}</th><th>{{field}}</th><th>{{methods}}</th><th>{{datasets}}</th><th>{{accesses}}</th><th>{{size}}</th><th>{{activitydays}}</th></tr>',
    traceTableBody: '{{log}}\n',
    loadingMessage: '<div class="alert alert-light text-center text-dark">Loading...</div>',
    warningMessage: '<div class="alert alert-danger text-center">Too many {{analysis_method}}. Showing 500 of {{total}}. <a href="javascript:{{allFunction}}">Show All</a></div>',
    errorMessage: '<div class="alert alert-danger text-center">Error loading data</div>',
    canvas: '<canvas class="my-2" id={{id}} width="600" height="350"></canvas>'
}
