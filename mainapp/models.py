from django.db import models


# Create your models here.
class Staff(models.Model):
    user = models.OneToOneField('auth.User', null=False, blank=False, default='1', on_delete=models.CASCADE)
    name = models.CharField(max_length=10, null=False, blank=False)
    memo = models.TextField(null=True, blank=True)
    group_type = models.ManyToManyField('GroupType', through='RelStaffGroupType', blank=True,
                                        related_name='group_type_staff')

    class Meta:
        db_table = 'staff'


class Member(models.Model):
    name = models.CharField(max_length=10, null=False, blank=False)
    birth_date = models.DateField(null=True, blank=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    tel = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    postal = models.CharField(max_length=10, null=True, blank=True)
    bohoon_num = models.CharField(max_length=15, null=True, blank=True)
    yoo_gong_ja_name = models.CharField(max_length=10, null=True, blank=True)
    yoo_gong_ja_rel = models.CharField(max_length=10, null=True, blank=True)
    import_date = models.DateField(null=True, blank=True)
    export_date = models.DateField(null=True, blank=True)
    pre_deleted = models.BooleanField(null=True, blank=True)
    is_deleted = models.BooleanField(null=True, blank=True)
    deleted_date = models.DateField(null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)
    modified_date = models.DateField(auto_now=True)
    memo = models.TextField(null=True, blank=True)
    group_type = models.ForeignKey('GroupType', null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name='group_type_member')
    program = models.ManyToManyField('Program', through='RelMemberProgram', blank=True,
                                    related_name='program_member')

    class Meta:
        db_table = 'member'
        ordering = ['group_type', 'name']


class GroupType(models.Model):
    name = models.CharField(max_length=10, null=False, blank=False)
    full_name = models.CharField(max_length=30, null=True, blank=True)
    staff = models.ManyToManyField('Staff', through='RelStaffGroupType', blank=True,
                                        related_name='staff_group_type')

    def __str__(self):
        return self.full_name
    class Meta:
        db_table = 'group_type'
        ordering = ['pk']


class RelStaffGroupType(models.Model):
    staff = models.ForeignKey('Staff', null=True, blank=True, on_delete=models.SET_NULL, related_name='staff_staff_group_type')
    group_type = models.ForeignKey('GroupType', null=True, blank=True, on_delete=models.SET_NULL,
                              related_name='group_type_staff_group_type')

    class Meta:
        db_table = 'rel_staff_group_type'


class Program(models.Model):
    manager = models.CharField(max_length=20, null=True, blank=True)
    manager_tel = models.CharField(max_length=30, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    memo = models.TextField(null=True, blank=True)
    program_name = models.ForeignKey('ProgramName', null=True, blank=True, on_delete=models.SET_NULL, related_name='program_name_program')
    member = models.ManyToManyField('Member', through='RelMemberProgram', blank=True,
                                    related_name='member_program')
    class Meta:
        db_table = 'program'


class ProgramName(models.Model):
    name = models.CharField(max_length=10, null=False, blank=False)


    class Meta:
        db_table = 'program_name'


class RelMemberProgram(models.Model):
    member = models.ForeignKey('Member', null=True, blank=True, on_delete=models.SET_NULL,
                               related_name='member_member_program')
    program = models.ForeignKey('Program', null=True, blank=True, on_delete=models.SET_NULL,
                               related_name='program_member_program')
    way = models.CharField(max_length=2, null=True, blank=True, choices=[('전화', '전화'), ('방문', '방문')])

    class Meta:
        db_table = 'rel_member_program'


class Counseling(models.Model):
    created_date = models.DateField(auto_now_add=True)
    memo = models.TextField(null=True, blank=True)
    modified_date = models.DateField(auto_now=True)
    staff = models.ForeignKey('Staff', null=True, blank=True, on_delete=models.SET_NULL,
                               related_name='staff_counseling')
    member = models.ForeignKey('Member', null=True, blank=True, on_delete=models.SET_NULL,
                              related_name='member_counseling')

    class Meta:
        db_table = 'counseling'

class GroupEvent(models.Model):
    created_date = models.DateField(auto_now_add=True)
    event_created_date = models.CharField(max_length=4, null=True, blank=True)
    sul = models.BooleanField(null=True, blank=True)
    bohoon = models.BooleanField(null=True, blank=True)
    choosuk = models.BooleanField(null=True, blank=True)
    junjukji = models.BooleanField(null=True, blank=True)
    charun = models.BooleanField(null=True, blank=True)
    etc1 = models.BooleanField(null=True, blank=True)
    etc2 = models.BooleanField(null=True, blank=True)
    etc3 = models.BooleanField(null=True, blank=True)
    explain = models.TextField(null=True, blank=True, default="")
    member = models.ForeignKey('Member', null=True, blank=True, on_delete=models.SET_NULL,
                              related_name='member_group_event')


    class Meta:
        db_table = 'group_event'
        ordering = ['-event_created_date', 'member']
        unique_together = ["event_created_date", "member"]