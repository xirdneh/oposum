# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Client'
        db.create_table(u'client_client', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('phonenumber', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('address', self.gf('django.db.models.fields.TextField')(max_length=1024, blank=True)),
            ('id_type', self.gf('django.db.models.fields.CharField')(default='IFE', max_length=50, blank=True)),
            ('id_number', self.gf('django.db.models.fields.TextField')(max_length=255, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'client', ['Client'])


    def backwards(self, orm):
        # Deleting model 'Client'
        db.delete_table(u'client_client')


    models = {
        u'client.client': {
            'Meta': {'object_name': 'Client'},
            'address': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_number': ('django.db.models.fields.TextField', [], {'max_length': '255', 'blank': 'True'}),
            'id_type': ('django.db.models.fields.CharField', [], {'default': "'IFE'", 'max_length': '50', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'phonenumber': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        }
    }

    complete_apps = ['client']