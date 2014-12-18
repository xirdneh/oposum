# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Branch.address'
        db.alter_column(u'branches_branch', 'address', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Branch.address'
        raise RuntimeError("Cannot reverse this migration. 'Branch.address' and its values cannot be restored.")

    models = {
        u'branches.branch': {
            'Meta': {'object_name': 'Branch'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'details': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'extra_details'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['branches.BranchDetail']"}),
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