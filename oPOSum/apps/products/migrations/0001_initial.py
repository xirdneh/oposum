# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ProviderDetail'
        db.create_table(u'products_providerdetail', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='detail name', max_length=255)),
            ('description', self.gf('django.db.models.fields.CharField')(default='detail description', max_length=255)),
        ))
        db.send_create_signal(u'products', ['ProviderDetail'])

        # Adding model 'Provider'
        db.create_table(u'products_provider', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sku', self.gf('django.db.models.fields.CharField')(unique=True, max_length=3)),
            ('name', self.gf('django.db.models.fields.CharField')(default='nombre', max_length=255)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('telephone1', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('telephone2', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'products', ['Provider'])

        # Adding M2M table for field details on 'Provider'
        m2m_table_name = db.shorten_name(u'products_provider_details')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('provider', models.ForeignKey(orm[u'products.provider'], null=False)),
            ('providerdetail', models.ForeignKey(orm[u'products.providerdetail'], null=False))
        ))
        db.create_unique(m2m_table_name, ['provider_id', 'providerdetail_id'])

        # Adding model 'ProductCategory'
        db.create_table(u'products_productcategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='child', null=True, to=orm['products.ProductCategory'])),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'products', ['ProductCategory'])

        # Adding model 'ProductPrice'
        db.create_table(u'products_productprice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, blank=True)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
        ))
        db.send_create_signal(u'products', ['ProductPrice'])

        # Adding model 'ProductDetail'
        db.create_table(u'products_productdetail', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='detail name', max_length=255)),
            ('description', self.gf('django.db.models.fields.CharField')(default='detail description', max_length=255)),
        ))
        db.send_create_signal(u'products', ['ProductDetail'])

        # Adding model 'Product'
        db.create_table(u'products_product', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('provider', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['products.Provider'])),
            ('price', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['products.ProductPrice'])),
            ('equivalency', self.gf('django.db.models.fields.DecimalField')(default='1.00', max_digits=10, decimal_places=2)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=512, blank=True)),
        ))
        db.send_create_signal(u'products', ['Product'])

        # Adding M2M table for field category on 'Product'
        m2m_table_name = db.shorten_name(u'products_product_category')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm[u'products.product'], null=False)),
            ('productcategory', models.ForeignKey(orm[u'products.productcategory'], null=False))
        ))
        db.create_unique(m2m_table_name, ['product_id', 'productcategory_id'])

        # Adding M2M table for field details on 'Product'
        m2m_table_name = db.shorten_name(u'products_product_details')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm[u'products.product'], null=False)),
            ('productdetail', models.ForeignKey(orm[u'products.productdetail'], null=False))
        ))
        db.create_unique(m2m_table_name, ['product_id', 'productdetail_id'])


    def backwards(self, orm):
        # Deleting model 'ProviderDetail'
        db.delete_table(u'products_providerdetail')

        # Deleting model 'Provider'
        db.delete_table(u'products_provider')

        # Removing M2M table for field details on 'Provider'
        db.delete_table(db.shorten_name(u'products_provider_details'))

        # Deleting model 'ProductCategory'
        db.delete_table(u'products_productcategory')

        # Deleting model 'ProductPrice'
        db.delete_table(u'products_productprice')

        # Deleting model 'ProductDetail'
        db.delete_table(u'products_productdetail')

        # Deleting model 'Product'
        db.delete_table(u'products_product')

        # Removing M2M table for field category on 'Product'
        db.delete_table(db.shorten_name(u'products_product_category'))

        # Removing M2M table for field details on 'Product'
        db.delete_table(db.shorten_name(u'products_product_details'))


    models = {
        u'products.product': {
            'Meta': {'object_name': 'Product'},
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'categories'", 'blank': 'True', 'to': u"orm['products.ProductCategory']"}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '512', 'blank': 'True'}),
            'details': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'extra_details'", 'symmetrical': 'False', 'to': u"orm['products.ProductDetail']"}),
            'equivalency': ('django.db.models.fields.DecimalField', [], {'default': "'1.00'", 'max_digits': '10', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'price': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['products.ProductPrice']"}),
            'provider': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['products.Provider']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'products.productcategory': {
            'Meta': {'object_name': 'ProductCategory'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'child'", 'null': 'True', 'to': u"orm['products.ProductCategory']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'})
        },
        u'products.productdetail': {
            'Meta': {'object_name': 'ProductDetail'},
            'description': ('django.db.models.fields.CharField', [], {'default': "'detail description'", 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'detail name'", 'max_length': '255'})
        },
        u'products.productprice': {
            'Meta': {'object_name': 'ProductPrice'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'})
        },
        u'products.provider': {
            'Meta': {'object_name': 'Provider'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'details': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'extra_details'", 'symmetrical': 'False', 'to': u"orm['products.ProviderDetail']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'nombre'", 'max_length': '255'}),
            'sku': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3'}),
            'telephone1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'telephone2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'products.providerdetail': {
            'Meta': {'object_name': 'ProviderDetail'},
            'description': ('django.db.models.fields.CharField', [], {'default': "'detail description'", 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'detail name'", 'max_length': '255'})
        }
    }

    complete_apps = ['products']