function format(d) {
    return '<table class="table">' +
        '<tr>' +
            '<td><strong>Function Definition</strong></td>' +
            '<td><pre class="mypre" style="font-size:100%;">' +
            '<code class="python">' + d + '</code>' +
            '</pre></td>' +
        '</tr>' +
    '</table>';
}

$(document).ready(function() {
    var table = $("#func-all").DataTable({
        "columns": [
            null,null,null,null,null,null,null,
            {'visible': true},
            null,
        ],
        "order": [[ 1, "asec" ]],
    });

    $("#func-all tbody").on('click', 'td.details-control', function() {
        var tr = $(this).closest('tr');
        var row = table.row(tr);

        if (row.child.isShown()) {
            row.child.hide();
            tr.removeClass('shown');
        } else {
            row.child(format(row.data()[7])).show();
            tr.addClass('shown');

            $('pre code').each(function(i, block) {
                hljs.highlightBlock(block);
            });
        }
    });
});
