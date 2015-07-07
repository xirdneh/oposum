# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Client.id_number'
        db.alter_column(u'client_client', 'id_number', self.gf('django.db.models.fields.CharField')(max_length=255))

    def backwards(self, orm):

        # Changing field 'Client.id_number'
        db.alter_column(u'client_client', 'id_number', self.gf('django.db.models.fields.TextField')(max_length=255))

    models = {
        u'client.client': {
            'Meta': {'unique_together': "(('first_name', 'last_name'),)", 'object_name': 'Client'},
            'address': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id_type': ('django.db.models.fields.CharField', [], {'default': "'IFE'", 'max_length': '50', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'phonenumber': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '512'})
        }
    }

    complete_apps = ['client']