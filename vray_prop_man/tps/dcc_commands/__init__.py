def load_dcc_commands(dcc=None):
    dcc = dcc or 'base'
    if dcc == 'base':
        from base_dcc_commands import BaseCommands
        return BaseCommands()
    else:
        raise RuntimeError('%s is not a supported dcc', dcc)
