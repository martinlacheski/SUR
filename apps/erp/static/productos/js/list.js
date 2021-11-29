var cantProductos = 0;
//Creamos una variable para cargar el SELECT de Categoría, SubCategoria, Producto
var select_categoria = $('select[name="selectCategoria"]');
var select_subcategoria = $('select[name="selectSubcategoria"]');
var select_producto = $('select[name="selectProducto"]');
//Creamos variables auxiliares para el reporte
var checkSinStock = false;
//Creamos una estructura para el Reporte
var reporte = {
    items: {
        //Filtros
        categoria: '',
        subcategoria: '',
        producto: '',
        sinStock: '',
        //detalle de productos
        productos: [],
    },
};
$(function () {
    var tablaProductos = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        paging: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "subcategoria.categoria.nombre"},
            {"data": "subcategoria.nombre"},
            {"data": "descripcion"},
            {"data": "codigo"},
            {"data": "imagen"},
            {"data": "stockReal"},
            {"data": "precioVenta"},
            {"data": "precioVenta"}, //va duplicado algun campo por la botonera
        ],
        columnDefs: [
            {
                targets: [-4],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<img src="' + data + '" class="img-fluid d-block mx-auto" style="width: 30px; height: 30px;">';
                }
            },
            {
                targets: [-3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    if (row.stockReal > 0) {
                        return '<span class="badge badge-success">' + data + '</span>'
                    }
                    return '<span class="badge badge-danger">' + data + '</span>'
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '$' + parseFloat(data).toFixed(2);
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/productos/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/productos/delete/' + row.id + '/" id="' + row.id + '" onclick="btnEliminar(this.id, this.href)" class="btn btn-danger btn-xs btn-flat" data-toggle="modal" data-target="#deleteModal"><i class="fas fa-trash-alt"></i>';

                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {
            //Agregamos al Select2 las categorias que tenemos en el listado
            this.api().columns(0).every(function () {
                var column = this;
                var select = $('<select><option value=""></option></select>')
                    .appendTo($(column.footer()).empty())
                    .on('change', function () {
                        var val = $.fn.dataTable.util.escapeRegex(
                            $(this).val()
                        );
                        column
                            .search(val ? '^' + val + '$' : '', true, false)
                            .draw();
                    });
                column.data().unique().sort().each(function (d, j) {
                    var newOption = new Option(d.toString(), d.toString(), false, false);
                    $('.selectCategoria').append(newOption).trigger('change');
                });
            });
            //Asignamos Verdadero a la variable auxiliar del reporte
            checkSinStock = true;
            //Extendemos la busqueda del datatables
            $.fn.dataTable.ext.search.push(
                function (settings, data, dataIndex) {
                    // Asignamos el estado por cada renglon
                    var stock = (data[5]);
                    //Comparamos contra el renglon
                    if (stock > 0) {
                        return true;
                    }
                    return false;
                }
            );
            //Actualizamos la tabla
            tablaProductos.draw();
        }
    });
//------------------------------------FILTROS----------------------------------------//
    //Mostramos los Filtros
    $('.showFilters').on('click', function () {
        var filtros = $('#filters');

        if (filtros.css('display') === 'none') {
            document.getElementById("filters").style.display = "";
        } else {
            document.getElementById("filters").style.display = "none";
        }

    });

    //Aplicamos Filtro de Categorias
    $('.selectCategoria').on('change', function () {
        //Asignamos a una variabla la Categoria del Select
        var categoria = $(this).val();
        if (categoria !== null && categoria !== '' && categoria !== undefined) {
            //Extendemos la busqueda del datatables
            $.fn.dataTable.ext.search.push(
                function (settings, data, dataIndex) {
                    // Asignamos la Categoria por cada renglon
                    var categoriaTabla = (data[0].toString());
                    //Comparamos contra el renglon
                    if (categoria === categoriaTabla) {
                        return true;
                    }
                    return false;
                }
            );
            //Actualizamos la tabla
            tablaProductos.draw();
            //Select Anidado (Seleccionamos CATEGORIA y cargamos las SUBCATEGORIAS y los productos de dicha CATEGORIA
            var select_subcategorias = $('select[name="selectSubcategoria"]');
            var select_productos = $('select[name="selectProducto"]');
            var id = $(this).val();
            var options = '<option value="">---------</option>';
            if (id === '') {
                select_subcategorias.html(options);
                select_productos.html(options);
                return false;
            }
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': csrftoken,
                    'action': 'search_subcategorias',
                    'pk': id
                },
                dataType: 'json',
                success: function (data) {
                    if (!data.hasOwnProperty('error')) {
                        //Volvemos a cargar los datos del Select2 solo que los datos (data) ingresados vienen por AJAX
                        select_subcategorias.html('').select2({
                            theme: "bootstrap4",
                            language: 'es',
                            data: data
                        });
                    }
                }
            });
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': csrftoken,
                    'action': 'search_subcategorias_productos',
                    'pk': id
                },
                dataType: 'json',
                success: function (data) {
                    if (!data.hasOwnProperty('error')) {
                        //Volvemos a cargar los datos del Select2 solo que los datos (data) ingresados vienen por AJAX
                        select_productos.html('').select2({
                            theme: "bootstrap4",
                            language: 'es',
                            data: data
                        });
                    }
                }
            });
        }
    });

    //Aplicamos Filtro de Subcategorias
    $('.selectSubcategoria').on('change', function () {
        //Asignamos a una variabla la Subcategoria del Select
        var subcategoria = $(this).val();
        if (subcategoria !== null && subcategoria !== '' && subcategoria !== undefined) {
            //Extendemos la busqueda del datatables
            $.fn.dataTable.ext.search.push(
                function (settings, data, dataIndex) {
                    // Asignamos la Subcategoria por cada renglon
                    var subcategoriaTabla = (data[1].toString());
                    //Comparamos contra el renglon
                    if (subcategoria === subcategoriaTabla) {
                        return true;
                    }
                    return false;
                }
            );
            //Actualizamos la tabla
            tablaProductos.draw();
        }
        var select_productos = $('select[name="selectProducto"]');
        var id = $(this).val();
        var options = '<option value="">---------</option>';
        if (id === '') {
            select_productos.html(options);
            return false;
        }
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'action': 'search_productos',
                'pk': id
            },
            dataType: 'json',
            success: function (data) {
                if (!data.hasOwnProperty('error')) {
                    //Volvemos a cargar los datos del Select2 solo que los datos (data) ingresados vienen por AJAX
                    select_productos.html('').select2({
                        theme: "bootstrap4",
                        language: 'es',
                        data: data
                    });
                }
            }
        });
    });

    //Aplicamos Filtro de Productos
    $('.selectProducto').on('change', function () {
        //Asignamos a una variabla el producto del Select
        var producto = $(this).val();
        if (producto !== null && producto !== '' && producto !== undefined) {
            //Extendemos la busqueda del datatables
            $.fn.dataTable.ext.search.push(
                function (settings, data, dataIndex) {
                    // Asignamos el producto por cada renglon
                    var productoTabla = (data[2].toString());
                    //Comparamos contra el renglon
                    if (producto === productoTabla) {
                        return true;
                    }
                    return false;
                }
            );
            //Actualizamos la tabla
            tablaProductos.draw();
        }
    });
    //Filtrar Sin Stock
    $('#excluirSinStock').on('click', function () {
        if (this.checked) {
            //Asignamos Verdadero a la variable auxiliar del reporte
            checkSinStock = true;
            //Extendemos la busqueda del datatables
            $.fn.dataTable.ext.search.push(
                function (settings, data, dataIndex) {
                    // Asignamos el estado por cada renglon
                    var stock = (data[5]);
                    //Comparamos contra el renglon
                    if (stock > 0) {
                        return true;
                    }
                    return false;
                }
            );
            //Actualizamos la tabla
            tablaProductos.draw();
        } else {
            //Asignamos Falso a la variable auxiliar del reporte
            checkSinStock = false;
            //Reseteamos los filtros
            $.fn.dataTable.ext.search = [];
            $.fn.dataTable.ext.search.pop();
            tablaProductos.draw();
            document.getElementById("excluirSinStock").checked = false;
            $('.selectCategoria').val(null).trigger('change');
            $('.selectSubcategoria').val(null).trigger('change');
            $('.selectProducto').val(null).trigger('change');
        }
    });

    //Boton Resetear Filtros
    $('.btnResetFilters').on('click', function () {
        $.fn.dataTable.ext.search = [];
        $.fn.dataTable.ext.search.pop();
        tablaProductos.draw();
        $('.selectCategoria').val(null).trigger('change');
        $('.selectSubcategoria').val(null).trigger('change');
        $('.selectProducto').val(null).trigger('change');
        $('#excluirSinStock').prop('checked', false);
    });
//------------------------------------GENERAR REPORTE----------------------------------------//
    //Boton Generar Reporte
    $('#reporteForm').on('submit', function (e) {
        e.preventDefault();
        var dataProductos = [];
        //Recorremos el listado del Datatables para pasar el detalle con LOS FILTROS APLICADOS
        $('#data').DataTable().rows({filter: 'applied'}).every(function (rowIdx, tableLoop, rowLoop) {
            var data = this.data();
            dataProductos.push(data);
        });
        //Asignamos las variables a la estructura
        reporte.items.categoria = $('select[name="selectCategoria"]').val();
        reporte.items.subcategoria = $('select[name="selectSubcategoria"]').val();
        reporte.items.producto = $('select[name="selectProducto"]').val();
        reporte.items.checkSinStock = checkSinStock;
        reporte.items.productos = dataProductos;
        var parameters = new FormData();
        //Pasamos la accion
        parameters.append('action', 'create_reporte');
        parameters.append('reporte', JSON.stringify(reporte.items));
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: parameters,
            dataType: 'json',
            headers: {
                'X-CSRFToken': csrftoken,
            },
            processData: false,
            contentType: false,
            success: function (data) {
                if (!data.hasOwnProperty('error')) {
                    //Abrimos el PDF en una nueva pestaña
                    window.open(data.url, '_blank');
                    location.reload();
                } else {
                    console.log(data.error);
                }
            }
        });
    });
});
//------------------------------------Inicializar COMPONENTES----------------------------------------//
$(document).ready(function () {
    //Ocultamos los Filtros
    document.getElementById("filters").style.display = "none";
    //Inicializamos SELECT2
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });
    document.getElementById("excluirSinStock").checked = true;
});