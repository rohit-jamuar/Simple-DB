#!/usr/bin/python

class SimpleDatabase(object):
    '''
    Redis-ish v0.1
    '''
    def __init__(self):
        self._transactions = [dict()]
        self._action = {'SET' : self._set_value, \
        'UNSET': self._unset_value, 'GET': self._get_value, \
        'NUMEQUALTO' : self._num_equal_to, 'END' : self._end, \
        'BEGIN' : self._begin, 'ROLLBACK' : self._rollback, \
        'COMMIT' : self._commit}

    def _set_value(self, key, value):
        '''
        Sets the value of variable with name 'key' to 'value' - the value is
        set in the currently active transaction or at the base index of
        underlying data-structure (i.e. self._transactions), i.e. if no
        transactions are currently live.
        '''
        self._transactions[-1][key] = value

    def _unset_value(self, key):
        '''
        Un-sets the value of the variable 'key' in the currently active
        transaction - if no transactions are open, it un-sets the value at the
        base index.
        '''
        self._transactions[-1][key] = None

    def _get_value(self, var_name):
        '''
        If there is an open transaction, this method tries to get the associated
        value from the most recently opened transaction. If it is unable to find
        the var_name in that transaction, it tries to locate it in the already
        committed transaction (i.e. the one at index 0). If the variable is
        found and it's value has not been unset by a previous command, the
        method prints the associated value.
        '''
        if len(self._transactions) > 1:
            for key, value in self._transactions[-1].items():
                if key == var_name:
                    print 'NULL' if not value else value
                    return
        for key, value in self._transactions[0].items():
            if key == var_name:
                print 'NULL' if not value else value
                return
        print 'NULL'

    def _num_equal_to(self, val):
        '''
        This method primarily starts counting variable's values (which
        equal the value provided as an argument to this method) from the
        currently active transaction. While doing so, it also tracks all
        the variables which have been un-set at this level. Then, this method
        moves on to counting values in the committed transaction - the only
        difference is that it only considers those variable's values which
        have not been un-set by the most recently opened transaction.
        '''
        count, nulled_in_cur_tx = 0, set()
        if len(self._transactions) > 1:
            for key, value in self._transactions[-1].items():
                if value == val:
                    count += 1
                if not value:
                    nulled_in_cur_tx.add(key)
        for key, value in self._transactions[0].items():
            if value == val and key not in nulled_in_cur_tx:
                count += 1
        print count

    def _end(self, *_):
        '''
        This method terminates the dialog with database.
        '''
        exit(0)

    def _begin(self):
        '''
        This method starts a new transaction.
        '''
        self._transactions.append(dict())

    def _rollback(self):
        '''
        This method rolls back the changes made during the most recent
        transaction.
        '''
        if len(self._transactions) > 1:
            self._transactions.pop()
        else:
            print 'NO TRANSACTION'

    def _commit(self):
        '''
        This method commits all the changes made during different
        transactions into the base transaction (i.e. the one at index 0).
        '''
        if len(self._transactions) == 1:
            print 'NO TRANSACTION'
        while len(self._transactions) > 1:
            self._transactions[-2].update(self._transactions[-1])
            self._transactions.pop()

    def apply_action(self, act):
        '''
        This method is the main interaction point with this database. It returns
        appropriate methods which the user expects to execute. If the user
        ends up passing a command which is unsupported by this database, the
        database exits the current dialog.
        '''
        return self._action.get(act, self._action['END'])

if __name__ == '__main__':
    SIMPLE_DB = SimpleDatabase()
    try:
        while True:
            ARGS = [elem.strip() for elem in raw_input().strip().split()]
            if len(ARGS) == 1:
                SIMPLE_DB.apply_action(ARGS[0].upper())()
            elif len(ARGS) == 2:
                SIMPLE_DB.apply_action(ARGS[0].upper())(ARGS[1])
            elif len(ARGS) == 3:
                SIMPLE_DB.apply_action(ARGS[0].upper())(ARGS[1], ARGS[2])
            else:
                SIMPLE_DB.apply_action('END')()
    except EOFError:
        SIMPLE_DB.apply_action('END')())
