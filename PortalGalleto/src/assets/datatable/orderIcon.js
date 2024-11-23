jQuery.fn.dataTable.ext.order['orderIcon'] = function(settings, col)
{
    let cols = this.api().column(col, {order:'index'}).nodes().map(function(td, i)
    {
        return $('i', td).hasClass('fa-check-square') ? 1 : 0;
    });
    return cols;
}
