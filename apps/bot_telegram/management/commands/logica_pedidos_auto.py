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