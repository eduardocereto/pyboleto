def get_class_for_codigo(codigo):
    mod = __import__('pyboleto.bank.bradesco', globals(), locals(), ['BoletoBradesco'])
    return getattr(mod, 'BoletoBradesco')
