# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Visit'
        db.create_table(u'visits_visit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'visits', ['Visit'])

        # Adding model 'Provider'
        db.create_table(u'visits_provider', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'visits', ['Provider'])

        # Adding unique constraint on 'Provider', fields ['first_name', 'last_name']
        db.create_unique(u'visits_provider', ['first_name', 'last_name'])

        # Adding M2M table for field visits on 'Provider'
        m2m_table_name = db.shorten_name(u'visits_provider_visits')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('provider', models.ForeignKey(orm[u'visits.provider'], null=False)),
            ('visit', models.ForeignKey(orm[u'visits.visit'], null=False))
        ))
        db.create_unique(m2m_table_name, ['provider_id', 'visit_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Provider', fields ['first_name', 'last_name']
        db.delete_unique(u'visits_provider', ['first_name', 'last_name'])

        # Deleting model 'Visit'
        db.delete_table(u'visits_visit')

        # Deleting model 'Provider'
        db.delete_table(u'visits_provider')

        # Removing M2M table for field visits on 'Provider'
        db.delete_table(db.shorten_name(u'visits_provider_visits'))


    models = {
        u'visits.provider': {
            'Meta': {'unique_together': "(('first_name', 'last_name'),)", 'object_name': 'Provider'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'visits': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['visits.Visit']", 'symmetrical': 'False'})
        },
        u'visits.visit': {
            'Meta': {'ordering': "('-date',)", 'object_name': 'Visit'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['visits']