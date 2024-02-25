from odoo import models, fields, api
from odoo.exceptions import ValidationError

class TrainingClass(models.Model):
    _name = 'training.class'
    _inherit = ['training.class', 'mail.thread', 'mail.activity.mixin']
    _order = 'number'

    second_description = fields.Text('Second Description')
    description = fields.Text('First Description')
    class_type = fields.Selection(required=False)

    state = fields.Selection(tracking=True)

    number = fields.Char('Number')

    # method lihat member
    def action_view_member(self):
        action = self.env['ir.actions.act_window']._for_xml_id('training4.training_class_member_action')
        action["domain"] = [("training_id", "=", self.id)]
        return action

    # isi nomor TC ketika membuat data baru
    @api.model_create_multi
    def _create(self, values):

        res = super()._create(values)
        for record in res:
            # create sequence on save
            record['number'] = self.env['ir.sequence'].next_by_code('training.class')
        
        return res

    def action_confirm(self):
        # Validasi ada member saat konfirm
        if not self.member_ids:
            raise ValidationError('Member harus minimal 1')
        res = super().action_confirm()
        
        # isi second description saat konfirm
        self.second_description = 'Terkonfirmasi';

        # cek ada nomor TC atau tidak
        if not self.number: 
            self.number = self.env['ir.sequence'].next_by_code('training.class')

        return res


class TrainingClass(models.Model):
    _name = 'training.class.copy'
    _inherit = 'training.class'
    copy_description = fields.Text('Copy Description')