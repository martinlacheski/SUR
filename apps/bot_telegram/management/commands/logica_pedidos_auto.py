def ver_detalle(prod_det):
    print("_________DETALLE DE PRODUTO_____")
    for d in prod_det:
        print("PROVEEDOR: " + str(d['proveedor']))
        print("CANT_PRODUCTOS: " + str(d['cant_prod']))
        print("PRODUCTOS: ")
        for prod in d['productos']:
            print(str(prod.id) + " - " + str(prod.abreviatura))
        print("---------------")
    return True

def ver_detalle_obj(prod_det):
    print("_________DETALLE DE PRODUTO_____")
    for d in prod_det:
        print("PROVEEDOR: " + str(d['proveedor']))
        print("CANT_PRODUCTOS: " + str(d['cant_prod']))
        print("PRODUCTOS: ")
        for prod in d['productos']:
            print(str(prod.producto.id) + str(prod.producto.abreviatura) + " - " + str(prod.costo) + "--" + str(prod.cantidad))
        print("---------------")
    return True


def ver_cand(prod_cand):
    for p in prod_cand:
        print("Producto " + str(p.producto.id) + " " + str(p.producto.descripcion) + "\nProveedor: " + str(p.pedidoSolicitudProveedor.proveedor) + "\nCantidad:" + str(p.cantidad))
    print("---------------")

# Funcion usada para ordenamiento
def costo(objDetalle):
    return objDetalle.costo