# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.model import ModelView, ModelSQL, fields
from trytond.wizard import Wizard, StateView, Button
from trytond.transaction import Transaction
from trytond.pyson import Eval
from trytond.pool import Pool


__all__ = ['BOM', 'BOMInput', 'BOMOutput', 'BOMTree', 'OpenBOMTreeStart',
    'OpenBOMTreeTree', 'OpenBOMTree']


class BOM(ModelSQL, ModelView):
    "Bill of Material"
    __name__ = 'production.bom'

    name = fields.Char('Name', required=True, translate=True)
    active = fields.Boolean('Active', select=1)
    inputs = fields.One2Many('production.bom.input', 'bom', 'Inputs')
    outputs = fields.One2Many('production.bom.output', 'bom', 'Outputs')
    output_products = fields.Many2Many('production.bom.output',
        'bom', 'product', 'Output Products')

    @staticmethod
    def default_active():
        return True

    def compute_factor(self, product, quantity, uom):
        '''
        Compute factor for an output product
        '''
        Uom = Pool().get('product.uom')
        for output in self.outputs:
            if output.product == product:
                if not output.quantity:
                    return 0.0
                quantity = Uom.compute_qty(uom, quantity,
                    output.uom, round=False)
                return quantity / output.quantity

    @classmethod
    def copy(cls, records, default=None):
        if default is None:
            default = {}
        else:
            default = default.copy()
        default['output_products'] = False
        return super(BOM, cls).copy(records, default=default)


class BOMInput(ModelSQL, ModelView):
    "Bill of Material Input"
    __name__ = 'production.bom.input'
    _rec_name = 'product'

    bom = fields.Many2One('production.bom', 'BOM', required=True,
        select=1, ondelete='CASCADE')
    product = fields.Many2One('product.product', 'Product',
        required=True, domain=[
            ('type', '!=', 'service'),
        ])
    uom_category = fields.Function(fields.Many2One(
        'product.uom.category', 'Uom Category'), 'on_change_with_uom_category')
    uom = fields.Many2One('product.uom', 'Uom', required=True,
        domain=[
            ('category', '=', Eval('uom_category')),
        ], depends=['uom_category'])
    unit_digits = fields.Function(fields.Integer('Unit Digits'),
        'on_change_with_unit_digits')
    quantity = fields.Float('Quantity', required=True,
        domain=[('quantity', '>=', 0)],
        digits=(16, Eval('unit_digits', 2)),
        depends=['unit_digits'])

    @classmethod
    def __setup__(cls):
        super(BOMInput, cls).__setup__()
        cls._sql_constraints = [
            ('product_bom_uniq', 'UNIQUE(product, bom)',
                'product_bom_uniq'),
            ]
        cls._error_messages.update({
                'product_bom_uniq': 'Product must be unique per BOM.',
                'recursive_bom': 'You can not create recursive BOMs.',
                })

    @fields.depends('product', 'uom')
    def on_change_product(self):
        if self.product:
            uoms = self.product.default_uom.category.uoms
            if (not self.uom or self.uom not in uoms):
                self.uom = self.product.default_uom
                self.unit_digits = self.product.default_uom.digits
        else:
            self.uom = None
            self.unit_digits = 2

    @fields.depends('product')
    def on_change_with_uom_category(self, name=None):
        if self.product:
            return self.product.default_uom.category.id

    @fields.depends('uom')
    def on_change_with_unit_digits(self, name=None):
        if self.uom:
            return self.uom.digits
        return 2

    @classmethod
    def validate(cls, boms):
        super(BOMInput, cls).validate(boms)
        for bom in boms:
            bom.check_bom_recursion()

    def check_bom_recursion(self):
        '''
        Check BOM recursion
        '''
        self.product.check_bom_recursion()

    def compute_quantity(self, factor):
        Uom = Pool().get('product.uom')
        return Uom.round(self.quantity * factor, self.uom.rounding)


class BOMOutput(BOMInput):
    "Bill of Material Output"
    __name__ = 'production.bom.output'
    _table = 'production_bom_output'  # Needed to override BOMInput._table


class BOMTree(ModelView):
    'BOM Tree'
    __name__ = 'production.bom.tree'

    product = fields.Many2One('product.product', 'Product')
    quantity = fields.Float('Quantity', digits=(16, Eval('unit_digits', 2)),
        depends=['unit_digits'])
    uom = fields.Many2One('product.uom', 'Uom')
    unit_digits = fields.Integer('Unit Digits')
    childs = fields.One2Many('production.bom.tree', None, 'Childs')

    @classmethod
    def tree(cls, product, quantity, uom, bom=None):
        Input = Pool().get('production.bom.input')

        result = []
        if bom is None:
            if not product.boms:
                return result
            bom = product.boms[0].bom

        factor = bom.compute_factor(product, quantity, uom)
        for input_ in bom.inputs:
            quantity = Input.compute_quantity(input_, factor)
            childs = cls.tree(input_.product, quantity, input_.uom)
            values = {
                'product': input_.product.id,
                'quantity': quantity,
                'uom': input_.uom.id,
                'unit_digits': input_.uom.digits,
                'childs': childs,
            }
            result.append(values)
        return result


class OpenBOMTreeStart(ModelView):
    'Open BOM Tree'
    __name__ = 'production.bom.tree.open.start'

    quantity = fields.Float('Quantity', required=True,
        digits=(16, Eval('unit_digits', 2)), depends=['unit_digits'])
    uom = fields.Many2One('product.uom', 'Unit', required=True,
        domain=[
            ('category', '=', Eval('category')),
        ], depends=['category'])
    unit_digits = fields.Integer('Unit Digits', readonly=True)
    category = fields.Many2One('product.uom.category', 'Category',
        readonly=True)
    bom = fields.Many2One('product.product-production.bom',
        'BOM', required=True, domain=[
            ('product', '=', Eval('product')),
        ], depends=['product'])
    product = fields.Many2One('product.product', 'Product', readonly=True)

    @fields.depends('uom')
    def on_change_with_unit_digits(self):
        if self.uom:
            return self.uom.digits
        return 2


class OpenBOMTreeTree(ModelView):
    'Open BOM Tree'
    __name__ = 'production.bom.tree.open.tree'

    bom_tree = fields.One2Many('production.bom.tree', None, 'BOM Tree')

    @classmethod
    def tree(cls, bom, product, quantity, uom):
        pool = Pool()
        Tree = pool.get('production.bom.tree')

        childs = Tree.tree(product, quantity, uom, bom=bom)
        bom_tree = [{
                'product': product.id,
                'quantity': quantity,
                'uom': uom.id,
                'unit_digits': uom.digits,
                'childs': childs,
                }]
        return {
            'bom_tree': bom_tree,
            }


class OpenBOMTree(Wizard):
    'Open BOM Tree'
    __name__ = 'production.bom.tree.open'

    start = StateView('production.bom.tree.open.start',
        'production.bom_tree_open_start_view_form', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('OK', 'tree', 'tryton-ok', True),
            ])
    tree = StateView('production.bom.tree.open.tree',
        'production.bom_tree_open_tree_view_form', [
            Button('Change', 'start', 'tryton-go-previous'),
            Button('Close', 'end', 'tryton-close'),
            ])

    def default_start(self, fields):
        Product = Pool().get('product.product')
        defaults = {}
        product = Product(Transaction().context['active_id'])
        defaults['category'] = product.default_uom.category.id
        if getattr(self.start, 'uom', None):
            defaults['uom'] = self.start.uom.id
            defaults['unit_digits'] = self.start.unit_digits
        else:
            defaults['uom'] = product.default_uom.id
            defaults['unit_digits'] = product.default_uom.digits
        defaults['product'] = product.id
        if getattr(self.start, 'bom', None):
            defaults['bom'] = self.start.bom.id
        elif product.boms:
            defaults['bom'] = product.boms[0].id
        defaults['quantity'] = getattr(self.start, 'quantity', None)
        return defaults

    def default_tree(self, fields):
        pool = Pool()
        BomTree = pool.get('production.bom.tree.open.tree')
        return BomTree.tree(self.start.bom.bom, self.start.product,
            self.start.quantity, self.start.uom)
