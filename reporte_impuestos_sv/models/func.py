# -*- coding: utf-8 -*-


################################################
# comprueba la longitud del numero de la factura
# devuelve el prefijo y la longitud
def numeracion(num):
    res = {}
    i = 0
    n = "0123456789"
    for l in num:
        i += 1
        ## print l,'Letra'
        if l not in n:
            # print l,"l"
            longitud = i
            # print longitud,'Longitud'
    res['longitud'] = longitud
    res['pre'] = num[:longitud]
    res['num'] = num[longitud:]
    return res


def limpieza(self):
    # borramos tod0 para que cada actualizacion se escriba en limpio
    self.env.cr.execute(
        'DELETE FROM libro_line WHERE libro_iva_id=' + str(self.id))
    self.env.cr.execute(
        'DELETE FROM resumen_line WHERE libro_iva_id=' + str(self.id))
    return True
