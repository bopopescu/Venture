# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, FormView, DetailView
from knowledge_center.models import *
from django.contrib.auth.models import User
from django.core.urlresolvers import resolve
from django.contrib.auth.mixins import LoginRequiredMixin
from actstream.models import user_stream
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, UpdateView, FormMixin
from django.core.paginator import Paginator
from itertools import chain


class IndexView(LoginRequiredMixin, ListView):
    """List All media Items"""
    template_name = "knowledge_index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView,
                        self).get_context_data(**kwargs)
        context['document_type'] = DocumentCategory.objects.filter(
            published=True)
        context['text_center'] = TextCenter.objects.filter(
            published=True).order_by('-date')[:5]
        context['videos'] = AudioVisual.objects.filter(
            published=True).order_by('-date')[:5]
        return context

    def get_queryset(self, **kwargs):
        queryset = TextCenter.objects.filter(
            sub_category__pk=self.kwargs.get("pk"), published=True).order_by('-date')
        return queryset


class HomeView(LoginRequiredMixin, ListView):
    """List all media items"""
    template_name = 'knowledge_text_index.html'
    paginate_by = 10
    queryset = TextCenter.objects.filter(published=True).order_by('-date')

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['document_type'] = DocumentCategory.objects.filter(
            published=True)
        return context


class TextMediaView(LoginRequiredMixin, DetailView):
    """Read a single Text Content"""
    model = TextCenter
    template_name = 'read_content.html'

    def get_context_data(self, **kwargs):
        """ Returns the Text Media selected"""
        context = super(TextMediaView, self).get_context_data(**kwargs)
        context['recommended'] = TextCenter.objects.filter(
            category__pk=1).order_by('date')[:6]
        context['content'] = TextCenter.objects.get(pk=self.kwargs.get("pk"))
        return context


class TextFilterView(LoginRequiredMixin, ListView):
    """List Text Content on Filter Category"""
    template_name = 'knowledge_text_index.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(TextFilterView, self).get_context_data(**kwargs)
        context['document_type'] = DocumentCategory.objects.filter(id=self.kwargs.get("pk"),
            published=True)
        return context

    def get_queryset(self, **kwargs):
        queryset = TextCenter.objects.filter(
            category__pk=self.kwargs.get("pk"), published=True).order_by('-date')
        return queryset


class SubCategoryTextFilterView(LoginRequiredMixin, ListView):
    """List Text Content on Filter Sub Category"""
    template_name = 'knowledge_text_index.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(SubCategoryTextFilterView,
                        self).get_context_data(**kwargs)
        context['document_type'] = DocumentCategory.objects.filter(
            published=True)
        return context

    def get_queryset(self, **kwargs):
        queryset = TextCenter.objects.filter(
            sub_category__pk=self.kwargs.get("pk"), published=True).order_by('-date')
        return queryset


class VideoFilterView(LoginRequiredMixin, ListView):
    """List Video Content on Filter Category"""
    template_name = 'all_video_content.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(VideoFilterView, self).get_context_data(**kwargs)
        context['video_type'] = VideoCategory.objects.filter(published=True)
        context['document_type'] = DocumentCategory.objects.filter(
            published=True)
        return context

    def get_queryset(self, **kwargs):
        queryset = AudioVisual.objects.filter(
            sub_category__pk=self.kwargs.get("pk"), published=True).order_by('-date')
        return queryset


class SingleVideoContentView(LoginRequiredMixin, DetailView):
    """Read a single Text Content"""
    model = AudioVisual
    template_name = 'video_content.html'

    def get_context_data(self, **kwargs):
        """ Returns the Text Media selected"""
        context = super(SingleVideoContentView,
                        self).get_context_data(**kwargs)
        context['recommended'] = AudioVisual.objects.filter(
            sub_category__pk=1).order_by('date')[:6]
        context['content'] = AudioVisual.objects.get(pk=self.kwargs.get("pk"))
        return context


class VideoContentView(LoginRequiredMixin, ListView):
    """Video Content"""
    template_name = 'all_video_content.html'
    paginator_by = 10
    queryset = AudioVisual.objects.filter(published=True)

    def get_context_data(self, **kwargs):
        context = super(VideoContentView, self).get_context_data(**kwargs)
        context['video_type'] = VideoCategory.objects.filter(published=True)
        return context
