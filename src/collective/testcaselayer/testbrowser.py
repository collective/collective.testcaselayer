def setATDateWidget(control, datetime, field, form='form'):
    name = form + '_' + field

    setATDateControl(control, datetime, name, 'year', zfill=4)
    setATDateControl(control, datetime, name, 'month')
    setATDateControl(control, datetime, name, 'day')
    setATDateControl(control, datetime, name, 'hour')
    setATDateControl(control, datetime, name, 'minute')

    ctl = control.getControl(name=name)
    ctl.value = str(datetime)
    return ctl


def setATDateControl(control, datetime, name, unit, zfill=2):
    value = getattr(datetime, unit)
    if callable(value):
        value = value()
    value = str(value)

    ctl = control.getControl(name=name + '_' + unit)

    if ctl.type == 'text':
        ctl = ctl
        ctl.value = value
    elif ctl.type == 'select':
        try:
            ctl = ctl.getControl(value=value.zfill(zfill))
        except LookupError:
            ctl = ctl.getControl(value=value)
        else:
            ctl.selected = True

    return ctl
