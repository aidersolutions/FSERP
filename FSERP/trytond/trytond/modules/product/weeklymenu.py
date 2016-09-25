from trytond.model import ModelView, ModelSQL, fields

__all__ = ['WeeklyMenu']
DAYS = [ ('monday','MONDAY'),
		 ('tuesday','TUESDAY'),
		 ('wednesday','WEDNESDAY'),
		 ('thursday','THURSDAY'),
		 ('friday','FRIDAY'),
		 ('saturday','SATURDAY'),
		 ('sunday','SUNDAY') ]


class WeeklyMenu(ModelSQL, ModelView ):
	"Weekly Menu"
	
	__name__ = "weeklymenu.weeklymenu"
	
	# dish is the dish which is to be scheduled
	dish = fields.Many2One("product.product", "Dish", select=1)
	# on a given day, like monday, friday etc...
	day = fields.Selection(DAYS, 'day')
	# with a default_quantity
	default_quantity = fields.Integer('Default Quanity', required=True)
	#which can be overridden by estimated_quantity, estimated based on previous sales data! #FUTURE
	estimated_quantity = fields.Integer('Estimate Quanity')
	# only if use_estimated flag is set.
	use_estimated = fields.Boolean('Use Estimated')
	# On the other hand User can decide to set a custom value in special cases. which has maximum prioriy
	custom_quantity = fields.Integer('Custom Quanity')
	
	def get_quantity(self):
		'''
		custom_quantity has maximum priority.
		if custom_quantity is not set and if use_estimated flag is set the estimated_quantity will be used. else default one will be used!
		'''
		if self.custom_quantity or self.custom_quantity==0:
			quantity = self.custom_quantity
		elif self.use_estimated and ( self.estimated_quantity or self.estimated_quantity==0):
			quantity = self.custom_quantity
		else:
			quantity = self.default_quantity
		return quantity


