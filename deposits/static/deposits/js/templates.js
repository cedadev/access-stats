var templates = {
    tableTotals: '<tr><th scope="row">{{totals}}</th><th>{{size}}</th><th>{{datasets}}</th><th>{{deposits}}</th><th>{{directories}}</th><th>{{symlinks}}</th><th>{{removedDirs}}</th><th>{{removedFiles}}</th></tr>',
    traceTableBody: '{{log}}\n',
    loadingMessage: '<div class="alert alert-light text-center text-dark">Loading...</div>',
    warningMessage: '<div class="alert alert-danger text-center">Too many {{analysis_method}}. Showing 500 of {{total}}. <a href="javascript:{{allFunction}}">Show All</a></div>',
    errorMessage: '<div class="alert alert-danger text-center">Error loading data</div>',
    canvas: '<canvas class="my-2" id={{id}} width="600" height="350"></canvas>'
}
