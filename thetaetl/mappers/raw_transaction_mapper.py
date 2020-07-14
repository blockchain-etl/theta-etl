# MIT License
#
# Copyright (c) 2018 Evgeny Medvedev, evge.medvedev@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from thetaetl.domain.raw_transaction import ThetaRawTransaction
from thetaetl.mappers.amount_mapper import ThetaAmountMapper
from thetaetl.mappers.amount_transfer_mapper import ThetaAmountTransferMapper

class ThetaRawTransactionMapper(object):
    def __init__(self, amount_mapper=None, amount_transfer_mapper=None):
        if amount_mapper is None:
            self.amount_mapper = ThetaAmountMapper()
        else:
            self.amount_mapper = amount_mapper

        if amount_transfer_mapper is None:
            self.amount_transfer_mapper = ThetaAmountTransferMapper()
        else:
            self.amount_transfer_mapper = amount_transfer_mapper

    def json_dict_to_raw_transaction(self, json_dict):
        raw_transaction = ThetaRawTransaction()

        if 'fee' in json_dict:
            raw_transaction.fee = self.amount_mapper.json_dict_to_amount(json_dict.get('fee'))

        if 'inputs' in json_dict:
            raw_transaction.inputs = [
                self.amount_transfer_mapper.json_dict_to_amount_transfer(transfer)
                for transfer in json_dict['inputs']
                if isinstance(transfer, dict)
            ]

        if 'outputs' in json_dict:
            raw_transaction.outputs = [
                self.amount_transfer_mapper.json_dict_to_amount_transfer(transfer)
                for transfer in json_dict['outputs']
                if isinstance(transfer, dict)
            ]

        return raw_transaction

    def raw_transaction_to_dict(self, raw_transaction):
        fee = None
        if raw_transaction.fee is not None:
            fee = self.amount_mapper.amount_to_dict(raw_transaction.fee)

        inputs = None
        if raw_transaction.inputs is not None:
            inputs = [
                self.amount_transfer_mapper.amount_transfer_to_dict(iput)
                    for iput in raw_transaction.inputs
            ]

        outputs = None
        if raw_transaction.outputs is not None:
            outputs = [
                self.amount_transfer_mapper.amount_transfer_to_dict(oput)
                    for oput in raw_transaction.outputs
        ]

        return {
            'type': 'raw_transaction',
            'fee': fee,
            'inputs': inputs,
            'outputs': outputs,
        }
