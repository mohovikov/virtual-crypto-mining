class InnoDBMixin:
    __table_args__ = {'mysql_engine': 'InnoDB'}