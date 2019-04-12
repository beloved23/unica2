def get_attr(obj, fld_name):
    '''
    Utility to recursively lookup attributes on obj

    fld_name is a possibly dot-separated attribute name
    '''
    bits = fld_name.split('.')
    if len(bits) == 1:
        #maybe a field or a method
        field_names = obj._meta.get_all_field_names()
        if not bits[0] in field_names:#a method?
            try:
                meth = getattr(obj, bits[0])
            except AttributeError:
                return None
            else:
                if callable(meth):
                    return meth()
                else:
                    return None
        fld = obj._meta.get_field(bits[0])
        if fld.choices:
            attr = getattr(obj, bits[0])
            if attr:
                return dict(fld.choices)[attr]
            else:
                return None
            #return dict(fld.choices)[getattr(obj, bits[0])]
    for bit in bits:
        obj = getattr(obj, bit)
        if callable(obj):
            obj = obj()
        elif not obj:
            return None
    return obj

#def get_fld_attr(obj, fld):
#    if fld.choices:
#        return dict(fld.choices)[getattr(obj, fld.name)]
