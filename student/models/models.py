# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import models, fields, api,exceptions


class Student(models.Model):
    _name = 'hr.student'


    _description = 'student'



    '''returns a list of (ID, name) tuples'''
    @api.multi
    def name_get(self):
        new_format = []
        for rec in self:
            new_info = " "
            new_info += rec.First_Name or " "
            new_info += " "
            new_info += rec.code or " "

            new_format.append((rec.id,new_info))
        return new_format






    '''override write method'''
    @api.multi
    def unlink(self):
        if self.state != 'draft':
            raise exceptions.ValidationError('cant delet')


        res = super(Student, self).unlink()
        '''Code after create
           Can use the new record created'''
        return res





    '''override create method'''
    @api.model
    def create(self,vals):

        vals['code']=self.env['ir.sequence'].next_by_code('hr.student')

        res = super(Student, self).create(vals)

        return res







    @api.multi
    @api.depends("birthdate")
    def _compute_age_studend (self):
        today = datetime.today().date()
        for record in self:
            if record.birthdate:
                birthdate= datetime.strptime(self.birthdate,"%Y-%m-%d")
                age_by_date =today-birthdate.date()
                record.age =age_by_date.days/365.25

    @api.multi
    @api.depends('degree_ids')
    def _total_degree(self):

        for record in self:
            sum=0
            for degree_obj in record.degree_ids:
                sum +=degree_obj.degree
            record.total=sum


    @api.multi
    def action_valid(self):
        for record in self:
            record.write({'state':'validated'})

    @api.multi
    def action_invalid(self):
        for record in self:
            record.write({'state': 'invaladated'})

    @api.multi
    def action_draft(self):
        for record in self:
            record.write({'state': 'draft'})

    @api.multi
    def action_gradute(self):
        for record in self:
            record.write({'state': 'graduated'})

    # raise exceptions.ValidationError(_('"Check Out" time cannot be earlier than "Check In" time.'))

    _sql_constraints = [
        ('uniqu n id','UNIQUE(nat_id)','Error erroe ! ')
    ]


    '''override write method'''
    @api.multi
    def write(self,vals):
        if 'nat_id'in vals:
           if vals['nat_id']and len(vals['nat_id'])!= 14 :
              raise exceptions.ValidationError('national id be 14')

        res=super(Student, self).write(vals)

        return res

    nat_id = fields.Char(string="National_id", required=False, )


    state = fields.Selection(string="State", selection=[('draft', 'Draft'), ('validated', 'Validated'),('invaladated','Invaldated'),('graduated','Graduted') ], default='draft',copy=False )
    First_Name = fields.Char(string="FirstName", required=True, )
    Last_Name = fields.Char(string="LastName", required=True, )
    birthdate = fields.Date(string="BIrthdate", required=True, )
    age = fields.Float(string="Age",  required=False,compute=_compute_age_studend )
    PhoneNum = fields.Char(string="PhoneNumber", required=False, )
    code = fields.Char(string="code", required=False, )

    Mail = fields.Char(string="Mail", required=False, )
    year = fields.Integer(string="year", required=True, )
    department_id = fields.Many2one(comodel_name="hr.department", string="department", required=False, )
    course_ids = fields.Many2many(comodel_name="hr.course", string="courses" )
    active = fields.Boolean(string="Active", default=True  )
    gender = fields.Selection(string="Gender", selection=[('male', 'Male'), ('female', 'Female'), ], required=False, default='male' )
    degree_ids = fields.One2many(comodel_name="student.degree", inverse_name="student_id", string="", required=False, )
    grade_id = fields.Many2one(comodel_name="student.grade", string="grade", required=False, )
    total = fields.Float(string="Total",  required=False, compute=_total_degree )
    start_age = fields.Float(string="start", required=False,related='grade_id.start_age' )
    end_grade = fields.Float(string="end",required=False,related='grade_id.start_age')
    pre_degree=fields.Float(string='pre degree',required=False)
    @api.onchange('grade_id')
    def _onchange_grade_id(self):
        if self.grade_id and self.grade_id.min_dgree:
            self.pre_degree=self.grade_id.min_dgree



class degree(models.Model):
    _name = 'student.degree'

    _description = 'Degree'

    course_name = fields.Char(string="course", required=False, )
    degree = fields.Float(string="degree",  required=False, )
    student_id = fields.Many2one(comodel_name="hr.student", string="student", required=False, )






class Department(models.Model):
    _name = 'hr.department'
    name = fields.Char(string="name", required=False, )
    year = fields.Integer(string="year", required=True, )



class course(models.Model):
    _name = 'hr.course'


    name = fields.Char(string='course')
    hours = fields.Float(string="Hours",  required=False, )

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        args = []
        if not (name == '' and operator == 'ilike'):
            args += ['|', ('name', operator, name),('hours', operator, name)]
        return super(course, self)._name_search(name='', args=args, operator='ilike', limit=limit,name_get_uid=name_get_uid)






class grade(models.Model):
    _name = 'student.grade'

    _description = 'New Description'

    name = fields.Char(string="gradename", required=False, )
    start_age = fields.Float(string="start",  required=False, )
    end_grade = fields.Float(string="end")
    min_dgree = fields.Float(string="min",  required=False, )





# class student(models.Model):
#     _name = 'student.student'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100