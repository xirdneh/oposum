# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BranchDetail'
        db.create_table(u'branches_branchdetail', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'branches', ['BranchDetail'])

        # Adding model 'BranchType'
        db.create_table(u'branches_branchtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='branch type', unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.CharField')(default='type description', max_length=255)),
        ))
        db.send_create_signal(u'branches', ['BranchType'])

        # Adding model 'Branch'
        db.create_table(u'branches_branch', (
            ('slug', self.gf('django.db.models.fields.CharField')(default='branch', unique=True, max_length=50, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='branch name', max_length=50)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['branches.BranchType'])),
        ))
        db.send_create_signal(u'branches', ['Branch'])

        # Adding M2M table for field details on 'Branch'
        m2m_table_name = db.shorten_name(u'branches_branch_details')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('branch', models.ForeignKey(orm[u'branches.branch'], null=False)),
            ('branchdetail', models.ForeignKey(orm[u'branches.branchdetail'], null=False))
        ))
        db.create_unique(m2m_table_name, ['branch_id', 'branchdetail_id'])


    def backwards(self, orm):
        # Deleting model 'BranchDetail'
        db.delete_table(u'branches_branchdetail')

        # Deleting model 'BranchType'
        db.delete_table(u'branches_branchtype')

        # Deleting model 'Branch'
        db.delete_table(u'branches_branch')

        # Removing M2M table for field details on 'Branch'
        db.delete_table(db.shorten_name(u'branches_branch_details'))


    models = {
        u'branches.branch': {
            'Meta': {'object_name': 'Branch'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'details': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'extra_details'", 'symmetrical': 'False', 'to': u"orm['branches.BranchDetail']"}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'branch name'", 'max_length': '50'}),
            'slug': ('django.db.models.fields.CharField', [], {'default': "'branch'", 'unique': 'True', 'max_length': '50', 'primary_key': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['branches.BranchType']"})
        },
        u'branches.branchdetail': {
            'Meta': {'object_name': 'BranchDetail'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'branches.branchtype': {
            'Meta': {'object_name': 'BranchType'},
            'description': ('django.db.models.fields.CharField', [], {'default': "'type description'", 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'branch type'", 'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['branches']